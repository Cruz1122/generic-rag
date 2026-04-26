import httpx
from typing import List, Optional, Dict

from generic_rag.embeddings.base import BaseEmbeddingProvider
from generic_rag.core.exceptions import (
    ProviderAuthError,
    ProviderTimeoutError,
    ProviderRateLimitError,
    EmbeddingError,
    InvalidResponseError,
    ProviderError
)

class OpenAICompatibleEmbeddingProvider(BaseEmbeddingProvider):
    """
    HTTP provider for semantic embeddings using the OpenAI-compatible API format.
    Works with OpenAI, vLLM, LMStudio, Ollama (with openai compatibility), etc.
    """
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        model: str = "text-embedding-3-small",
        timeout_seconds: float = 30.0,
        batch_size: int = 100,
        extra_headers: Optional[Dict[str, str]] = None
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.batch_size = batch_size
        self.extra_headers = extra_headers or {}

    async def _make_request(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        headers = {
            "Content-Type": "application/json",
            **self.extra_headers
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "input": texts,
            "model": self.model
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=payload
                )
        except httpx.TimeoutException:
            raise ProviderTimeoutError(
                "Request to embedding provider timed out.", 
                provider="OpenAI-compatible"
            )
        except httpx.RequestError as e:
            raise ProviderError(
                f"Network error: {str(e)}", 
                provider="OpenAI-compatible"
            )

        if response.status_code in (401, 403):
            raise ProviderAuthError(
                "Authentication failed. Check your API key.", 
                provider="OpenAI-compatible", 
                status_code=response.status_code
            )
        elif response.status_code == 429:
            raise ProviderRateLimitError(
                "Rate limit exceeded.", 
                provider="OpenAI-compatible", 
                status_code=response.status_code
            )
        elif not response.is_success:
            raise ProviderError(
                f"HTTP error {response.status_code}", 
                provider="OpenAI-compatible", 
                status_code=response.status_code
            )

        try:
            data = response.json()
        except ValueError:
            raise InvalidResponseError(
                "Invalid JSON response from provider.", 
                provider="OpenAI-compatible", 
                raw_content=response.text
            )

        if "data" not in data or not isinstance(data["data"], list):
            raise InvalidResponseError(
                "Response missing 'data' list.", 
                provider="OpenAI-compatible", 
                raw_content=response.text
            )

        embeddings: List[List[float]] = []
        for item in data["data"]:
            if "embedding" not in item or not isinstance(item["embedding"], list):
                raise InvalidResponseError(
                    "Item missing 'embedding' list.", 
                    provider="OpenAI-compatible", 
                    raw_content=response.text
                )
            embeddings.append(item["embedding"])

        if len(embeddings) != len(texts):
            raise EmbeddingError(
                f"Expected {len(texts)} embeddings, got {len(embeddings)}"
            )

        return embeddings

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
            
        all_embeddings: List[List[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            batch_embeddings = await self._make_request(batch)
            all_embeddings.extend(batch_embeddings)
            
        return all_embeddings

    async def embed_query(self, text: str) -> List[float]:
        embeddings = await self._make_request([text])
        if not embeddings:
            raise EmbeddingError(
                "Failed to get embedding for query."
            )
        return embeddings[0]
