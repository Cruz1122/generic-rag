import pytest
from httpx import Response, TimeoutException
from generic_rag.embeddings.openai_compatible import OpenAICompatibleEmbeddingProvider
from generic_rag.core.exceptions import (
    ProviderAuthError,
    ProviderTimeoutError,
    ProviderRateLimitError,
    EmbeddingError,
    InvalidResponseError
)

@pytest.fixture
def provider():
    return OpenAICompatibleEmbeddingProvider(
        api_key="test-key",
        base_url="https://fake-api.com/v1",
        model="fake-model"
    )

@pytest.mark.asyncio
async def test_embed_query_success(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value = Response(
        status_code=200,
        json={"data": [{"embedding": [0.1, 0.2, 0.3]}]}
    )
    
    result = await provider.embed_query("test query")
    assert result == [0.1, 0.2, 0.3]
    mock_post.assert_called_once()
    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {"input": ["test query"], "model": "fake-model"}
    assert kwargs["headers"]["Authorization"] == "Bearer test-key"

@pytest.mark.asyncio
async def test_embed_documents_success(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value = Response(
        status_code=200,
        json={"data": [{"embedding": [0.1]}, {"embedding": [0.2]}]}
    )
    
    result = await provider.embed_documents(["doc1", "doc2"])
    assert result == [[0.1], [0.2]]
    mock_post.assert_called_once()
    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {"input": ["doc1", "doc2"], "model": "fake-model"}

@pytest.mark.asyncio
async def test_empty_list(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    result = await provider.embed_documents([])
    assert result == []
    mock_post.assert_not_called()

@pytest.mark.asyncio
async def test_auth_error(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value = Response(status_code=401)
    
    with pytest.raises(ProviderAuthError):
        await provider.embed_query("test")

@pytest.mark.asyncio
async def test_rate_limit_error(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value = Response(status_code=429)
    
    with pytest.raises(ProviderRateLimitError):
        await provider.embed_query("test")

@pytest.mark.asyncio
async def test_timeout_error(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.side_effect = TimeoutException("Timeout")
    
    with pytest.raises(ProviderTimeoutError):
        await provider.embed_query("test")

@pytest.mark.asyncio
async def test_invalid_json_response(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value = Response(status_code=200, content="Not JSON")
    
    with pytest.raises(InvalidResponseError):
        await provider.embed_query("test")

@pytest.mark.asyncio
async def test_inconsistent_dimensions(mocker, provider):
    mock_post = mocker.patch("httpx.AsyncClient.post")
    mock_post.return_value = Response(
        status_code=200,
        json={"data": [{"embedding": [0.1]}]}
    )
    
    with pytest.raises(EmbeddingError, match="Expected 2 embeddings, got 1"):
        await provider.embed_documents(["doc1", "doc2"])
