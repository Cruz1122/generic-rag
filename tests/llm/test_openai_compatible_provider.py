import pytest
import httpx
from generic_rag.llm.providers.openai_compatible import OpenAICompatibleProvider
from generic_rag.config import ProviderConfig
from pydantic import SecretStr
from generic_rag.core.schemas import LLMRequest, ChatMessage
from generic_rag.core.exceptions import ProviderAuthError, ProviderRateLimitError

@pytest.fixture
def provider():
    config = ProviderConfig(
        name="groq",
        api_key=SecretStr("test-key"),
        base_url="https://api.groq.com/openai/v1",
        default_model="llama-3"
    )
    return OpenAICompatibleProvider(config)

@pytest.mark.asyncio
async def test_openai_generate_success(provider, mocker):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello world"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
    }
    mock_response.raise_for_status.return_value = None

    mock_client_instance = mocker.AsyncMock()
    mock_client_instance.post.return_value = mock_response
    mocker.patch("httpx.AsyncClient.__aenter__", return_value=mock_client_instance)
    
    req = LLMRequest(model="llama-3", messages=[ChatMessage(role="user", content="hi")])
    res = await provider.generate(req)
    
    assert res.text == "Hello world"
    assert res.usage.total_tokens == 15
    assert res.finish_reason == "stop"
    
    mock_client_instance.post.assert_called_once()
    args, kwargs = mock_client_instance.post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer test-key"
    assert kwargs["json"]["model"] == "llama-3"

@pytest.mark.asyncio
async def test_openai_auth_error(provider, mocker):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.status_code = 401
    
    mock_client_instance = mocker.AsyncMock()
    mock_client_instance.post.side_effect = httpx.HTTPStatusError("Auth error", request=mocker.Mock(), response=mock_response)
    mocker.patch("httpx.AsyncClient.__aenter__", return_value=mock_client_instance)

    req = LLMRequest(model="llama-3", messages=[ChatMessage(role="user", content="hi")])
    with pytest.raises(ProviderAuthError):
        await provider.generate(req)

@pytest.mark.asyncio
async def test_openai_rate_limit_error(provider, mocker):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.status_code = 429
    
    mock_client_instance = mocker.AsyncMock()
    mock_client_instance.post.side_effect = httpx.HTTPStatusError("Rate limit", request=mocker.Mock(), response=mock_response)
    mocker.patch("httpx.AsyncClient.__aenter__", return_value=mock_client_instance)

    req = LLMRequest(model="llama-3", messages=[ChatMessage(role="user", content="hi")])
    with pytest.raises(ProviderRateLimitError):
        await provider.generate(req)
