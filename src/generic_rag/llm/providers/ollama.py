import httpx
from typing import AsyncIterator, Any, Dict
from generic_rag.core.schemas import LLMRequest, LLMResponse, TokenUsage, ProviderInfo
from generic_rag.core.exceptions import (
    ProviderError, ProviderTimeoutError, InvalidResponseError
)
from generic_rag.llm.base import BaseLLMProvider
from generic_rag.config import ProviderConfig

class OllamaProvider(BaseLLMProvider):
    """Provider for Ollama API."""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self._name = config.name
        self.base_url = (config.base_url or "http://localhost:11434").rstrip("/")

    @property
    def name(self) -> str:
        return self._name

    def _prepare_payload(self, request: LLMRequest) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": request.model,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
            "stream": request.stream,
        }
        if request.response_format == "json_object":
            if request.json_schema:
                payload["format"] = request.json_schema
            else:
                payload["format"] = "json"
        return payload

    async def generate(self, request: LLMRequest) -> LLMResponse:
        payload = self._prepare_payload(request)
        
        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status in (401, 403):
                raise ProviderAuthError(f"Auth error ({status}): {e}", provider=self.name, status_code=status)
            elif status in (408, 504):
                raise ProviderTimeoutError(f"Timeout error ({status}): {e}", provider=self.name, status_code=status)
            elif status == 429:
                raise ProviderRateLimitError(f"Rate limit exceeded ({status}): {e}", provider=self.name, status_code=status)
            elif status in (400, 422):
                raise InvalidResponseError(f"Client error ({status}): {e}", provider=self.name, raw_content=e.response.text)
            raise ProviderError(f"HTTP error ({status}): {e}", provider=self.name, status_code=status)
        except httpx.TimeoutException as e:
            raise ProviderTimeoutError(f"Request timed out: {e}", provider=self.name)
        except httpx.RequestError as e:
            raise ProviderError(f"Request failed: {e}", provider=self.name)
        except ValueError as e:
            raise InvalidResponseError(f"Invalid JSON response: {e}", provider=self.name)

        message = data.get("message", {})
        text = message.get("content", "") or ""
        
        usage = TokenUsage(
            prompt_tokens=data.get("prompt_eval_count", 0),
            completion_tokens=data.get("eval_count", 0),
            total_tokens=data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
        )
        
        provider_info = ProviderInfo(
            name=self.name,
            model=request.model
        )
        
        return LLMResponse(
            text=text,
            usage=usage,
            provider_info=provider_info,
            finish_reason=data.get("done_reason")
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        raise NotImplementedError("Streaming is not yet implemented")
