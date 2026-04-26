import pytest
import httpx
from generic_rag.llm.providers.ollama import OllamaProvider
from generic_rag.config import ProviderConfig
from generic_rag.core.schemas import LLMRequest, ChatMessage
from generic_rag.core.exceptions import ProviderError

@pytest.fixture
def provider():
    config = ProviderConfig(
        name="ollama_local",
        base_url="http://localhost:11434",
        default_model="llama3"
    )
    return OllamaProvider(config)

@pytest.mark.asyncio
async def test_ollama_generate_success(provider, mocker):
    mock_response = mocker.Mock(spec=httpx.Response)
    mock_response.json.return_value = {
        "model": "llama3",
        "message": {"role": "assistant", "content": "Hello from Ollama"},
        "done_reason": "stop",
        "prompt_eval_count": 5,
        "eval_count": 10
    }
    mock_response.raise_for_status.return_value = None

    mock_client_instance = mocker.AsyncMock()
    mock_client_instance.post.return_value = mock_response
    mocker.patch("httpx.AsyncClient.__aenter__", return_value=mock_client_instance)
    
    req = LLMRequest(model="llama3", messages=[ChatMessage(role="user", content="hi")])
    res = await provider.generate(req)
    
    assert res.text == "Hello from Ollama"
    assert res.usage.total_tokens == 15
    assert res.finish_reason == "stop"
    
    mock_client_instance.post.assert_called_once()
    args, kwargs = mock_client_instance.post.call_args
    assert "options" in kwargs["json"]
