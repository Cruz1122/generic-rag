import httpx
from typing import AsyncIterator, Any, Dict
from generic_rag.core.schemas import LLMRequest, LLMResponse, TokenUsage, ProviderInfo
from generic_rag.core.exceptions import (
    ProviderError, ProviderAuthError, ProviderRateLimitError, ProviderTimeoutError, InvalidResponseError
)
from generic_rag.llm.base import BaseLLMProvider
from generic_rag.config import ProviderConfig

class OpenAICompatibleProvider(BaseLLMProvider):
    """Provider for OpenAI, Groq, LMStudio, etc."""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self._name = config.name
        self.base_url = (config.base_url or "https://api.openai.com/v1").rstrip("/")
        # Algunos providers locales como LMStudio no exigen API key
        self.api_key = config.api_key.get_secret_value() if config.api_key else "lm-studio"

    @property
    def name(self) -> str:
        return self._name

    def _map_error(self, exc: httpx.HTTPStatusError) -> Exception:
        status = exc.response.status_code
        if status in (401, 403):
            return ProviderAuthError(f"Auth error ({status}): {exc}")
        elif status == 429:
            return ProviderRateLimitError(f"Rate limit exceeded ({status}): {exc}")
        elif status >= 500:
            return ProviderError(f"Server error ({status}): {exc}")
        return ProviderError(f"HTTP error ({status}): {exc}")

    def _prepare_payload(self, request: LLMRequest) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream,
        }
        if request.response_format == "json_object":
            if request.json_schema:
                # Standard Structured Outputs parameter
                payload["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "response_schema",
                        "schema": request.json_schema,
                        "strict": True
                    }
                }
            else:
                payload["response_format"] = {"type": "json_object"}
        return payload

    async def generate(self, request: LLMRequest) -> LLMResponse:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = self._prepare_payload(request)
        
        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as e:
            raise self._map_error(e)
        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise ProviderError(f"Request failed: {e}")
        except ValueError as e:
            raise InvalidResponseError(f"Invalid JSON response: {e}")

        choices = data.get("choices", [])
        if not choices:
            raise InvalidResponseError("No choices returned in response")
        
        message = choices[0].get("message", {})
        text = message.get("content", "") or ""
        
        usage_data = data.get("usage", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0)
        )
        
        provider_info = ProviderInfo(
            name=self.name,
            model=request.model
        )
        
        return LLMResponse(
            text=text,
            usage=usage,
            provider_info=provider_info,
            finish_reason=choices[0].get("finish_reason")
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        raise NotImplementedError("Streaming is not yet implemented")
