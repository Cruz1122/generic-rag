import httpx
from typing import AsyncIterator, Any, Dict
from generic_rag.core.schemas import LLMRequest, LLMResponse, TokenUsage, ProviderInfo
from generic_rag.core.exceptions import (
    ProviderError, ProviderAuthError, ProviderRateLimitError, ProviderTimeoutError, InvalidResponseError
)
from generic_rag.llm.base import BaseLLMProvider
from generic_rag.config import ProviderConfig

class GeminiProvider(BaseLLMProvider):
    """Provider for Google Gemini via REST API."""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self._name = config.name
        self.base_url = (config.base_url or "https://generativelanguage.googleapis.com/v1beta/models").rstrip("/")
        self.api_key = config.api_key.get_secret_value() if config.api_key else ""

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
        contents = []
        system_instruction = None
        for msg in request.messages:
            if msg.role == "system":
                system_instruction = {"parts": [{"text": msg.content}]}
            else:
                role = "model" if msg.role == "assistant" else "user"
                contents.append({
                    "role": role,
                    "parts": [{"text": msg.content}]
                })

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": request.temperature,
                "maxOutputTokens": request.max_tokens,
            }
        }
        if system_instruction:
            payload["systemInstruction"] = system_instruction

        if request.response_format == "json_object":
            payload["generationConfig"]["responseMimeType"] = "application/json"
            if request.json_schema:
                payload["generationConfig"]["responseSchema"] = request.json_schema

        return payload

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise ProviderAuthError("Gemini API key is required")

        payload = self._prepare_payload(request)
        url = f"{self.base_url}/{request.model}:generateContent?key={self.api_key}"
        
        try:
            async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
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

        candidates = data.get("candidates", [])
        if not candidates:
            raise InvalidResponseError("No candidates returned in response")
        
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        text = parts[0].get("text", "") if parts else ""
        
        usage_data = data.get("usageMetadata", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("promptTokenCount", 0),
            completion_tokens=usage_data.get("candidatesTokenCount", 0),
            total_tokens=usage_data.get("totalTokenCount", 0)
        )
        
        provider_info = ProviderInfo(
            name=self.name,
            model=request.model
        )
        
        return LLMResponse(
            text=text,
            usage=usage,
            provider_info=provider_info,
            finish_reason=candidates[0].get("finishReason")
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        raise NotImplementedError("Streaming is not yet implemented")
