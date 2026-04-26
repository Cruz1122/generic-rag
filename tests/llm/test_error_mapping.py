import pytest
import httpx
from unittest.mock import AsyncMock, patch
from generic_rag.core.schemas import LLMRequest, ChatMessage
from generic_rag.core.exceptions import (
    ProviderAuthError, ProviderRateLimitError, ProviderTimeoutError, InvalidResponseError, ProviderError
)
from generic_rag.llm.providers.openai_compatible import OpenAICompatibleProvider
from generic_rag.config import ProviderConfig

@pytest.fixture
def provider():
    config = ProviderConfig(name="test", default_model="test-model")
    return OpenAICompatibleProvider(config)

@pytest.fixture
def request_obj():
    return LLMRequest(
        provider="test",
        model="test-model",
        messages=[ChatMessage(role="user", content="Hi")]
    )

@pytest.mark.asyncio
async def test_auth_error_mapping(provider, request_obj):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = httpx.Response(401, request=httpx.Request("POST", "http://test"))
        mock_post.side_effect = httpx.HTTPStatusError("Auth", request=mock_response.request, response=mock_response)
        
        with pytest.raises(ProviderAuthError) as exc_info:
            await provider.generate(request_obj)
        assert exc_info.value.status_code == 401
        assert exc_info.value.provider == "test"

@pytest.mark.asyncio
async def test_timeout_mapping(provider, request_obj):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.side_effect = httpx.TimeoutException("Timeout")
        
        with pytest.raises(ProviderTimeoutError) as exc_info:
            await provider.generate(request_obj)
        assert exc_info.value.provider == "test"

@pytest.mark.asyncio
async def test_rate_limit_mapping(provider, request_obj):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = httpx.Response(429, request=httpx.Request("POST", "http://test"))
        mock_post.side_effect = httpx.HTTPStatusError("Rate Limit", request=mock_response.request, response=mock_response)
        
        with pytest.raises(ProviderRateLimitError) as exc_info:
            await provider.generate(request_obj)
        assert exc_info.value.status_code == 429

@pytest.mark.asyncio
async def test_invalid_json_response(provider, request_obj):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = httpx.Response(200, request=httpx.Request("POST", "http://test"), content=b"invalid json {")
        mock_post.return_value = mock_response
        
        with pytest.raises(InvalidResponseError) as exc_info:
            await provider.generate(request_obj)
        assert "Invalid JSON" in str(exc_info.value)
