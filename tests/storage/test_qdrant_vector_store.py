import pytest
import sys
import importlib
from unittest.mock import AsyncMock, MagicMock, patch

# Mock the entire qdrant_client module before anything else
mock_models = MagicMock()
mock_http = MagicMock()
mock_http.models = mock_models
mock_qdrant = MagicMock()
mock_qdrant.http = mock_http

sys.modules["qdrant_client"] = mock_qdrant
sys.modules["qdrant_client.http"] = mock_http
sys.modules["qdrant_client.http.models"] = mock_models

# Force reload of the qdrant module if it was already imported
if "generic_rag.storage.qdrant" in sys.modules:
    importlib.reload(sys.modules["generic_rag.storage.qdrant"])

from generic_rag.storage.qdrant import QdrantVectorStore
from generic_rag.core.schemas import Chunk, SourceRef, ScoredChunk
from generic_rag.core.exceptions import StorageError, ConfigurationError, InvalidResponseError

@pytest.fixture(autouse=True)
def mock_optional_dependency():
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=True):
        yield

@pytest.fixture
def models_ref():
    return mock_models

@pytest.fixture
def mock_qdrant_client():
    client = AsyncMock()
    return client

@pytest.fixture
def qdrant_store(mock_qdrant_client, models_ref):
    # Ensure distance models are mocked for __init__
    models_ref.Distance.COSINE = "Cosine"
    models_ref.Distance.DOT = "Dot"
    models_ref.Distance.EUCLID = "Euclid"
    
    return QdrantVectorStore(
        client=mock_qdrant_client,
        collection_name="test_collection",
        vector_size=1536
    )

@pytest.mark.asyncio
async def test_ensure_collection_creates_when_missing(qdrant_store, mock_qdrant_client, models_ref):
    mock_qdrant_client.collection_exists.return_value = False
    
    await qdrant_store.ensure_collection()
    
    mock_qdrant_client.collection_exists.assert_called_once_with("test_collection")
    mock_qdrant_client.create_collection.assert_called_once()
    mock_qdrant_client.delete_collection.assert_not_called()

@pytest.mark.asyncio
async def test_ensure_collection_skips_when_exists(qdrant_store, mock_qdrant_client):
    mock_qdrant_client.collection_exists.return_value = True
    
    await qdrant_store.ensure_collection()
    
    mock_qdrant_client.create_collection.assert_not_called()

@pytest.mark.asyncio
async def test_ensure_collection_recreates_when_forced(qdrant_store, mock_qdrant_client):
    mock_qdrant_client.collection_exists.return_value = True
    
    await qdrant_store.ensure_collection(recreate=True)
    
    mock_qdrant_client.delete_collection.assert_called_once_with("test_collection")
    mock_qdrant_client.create_collection.assert_called_once()

@pytest.mark.asyncio
async def test_index_chunks_validates_counts(qdrant_store):
    chunks = [MagicMock(spec=Chunk)]
    embeddings = [] # mismatch
    
    with pytest.raises(ConfigurationError, match="Mismatch"):
        await qdrant_store.index_chunks(chunks, embeddings)

@pytest.mark.asyncio
async def test_index_chunks_validates_dimensions(qdrant_store):
    chunk = Chunk(
        id="c1", document_id="d1", chunk_index=0, content="test",
        start_char=0, end_char=4, source=SourceRef(source_id="s1", source_type="txt")
    )
    embeddings = [[1.0] * 10] # mismatch with 1536
    
    with pytest.raises(ConfigurationError, match="expected 1536"):
        await qdrant_store.index_chunks([chunk], embeddings)

@pytest.mark.asyncio
async def test_index_chunks_returns_early_on_empty_inputs(qdrant_store, mock_qdrant_client):
    await qdrant_store.index_chunks([], [])
    mock_qdrant_client.upsert.assert_not_called()

@pytest.mark.asyncio
async def test_index_chunks_calls_upsert_with_point_structs(qdrant_store, mock_qdrant_client, models_ref):
    chunk = Chunk(
        id="c1", document_id="d1", chunk_index=0, content="test",
        start_char=0, end_char=4, source=SourceRef(source_id="s1", source_type="txt")
    )
    embeddings = [[0.1] * 1536]
    
    await qdrant_store.index_chunks([chunk], embeddings)
    
    mock_qdrant_client.upsert.assert_called_once()
    kwargs = mock_qdrant_client.upsert.call_args.kwargs
    assert kwargs["collection_name"] == "test_collection"
    assert len(kwargs["points"]) == 1
    # PointStruct is called by the store
    models_ref.PointStruct.assert_called_once()

@pytest.mark.asyncio
async def test_search_builds_exact_match_filters(qdrant_store, mock_qdrant_client, models_ref):
    mock_qdrant_client.search.return_value = []
    
    filters = {"metadata.category": "test", "source.source_type": "pdf"}
    await qdrant_store.search([0.1]*1536, top_k=5, filters=filters)
    
    mock_qdrant_client.search.assert_called_once()
    kwargs = mock_qdrant_client.search.call_args.kwargs
    assert kwargs["query_filter"] is not None
    models_ref.Filter.assert_called()

@pytest.mark.asyncio
async def test_search_rejects_complex_filters(qdrant_store):
    filters = {"key": {"complex": "value"}}
    with pytest.raises(ConfigurationError, match="Unsupported complex filter"):
        await qdrant_store.search([0.1]*1536, top_k=5, filters=filters)

@pytest.mark.asyncio
async def test_search_reconstructs_scored_chunk_successfully(qdrant_store, mock_qdrant_client):
    mock_point = MagicMock()
    mock_point.score = 0.95
    mock_point.payload = {
        "chunk_id": "c1", "document_id": "d1", "chunk_index": 0, "content": "test",
        "start_char": 0, "end_char": 4, "source": {"source_id": "s1", "source_type": "txt"},
        "metadata": {"key": "val"}
    }
    mock_qdrant_client.search.return_value = [mock_point]
    
    results = await qdrant_store.search([0.1]*1536, top_k=1)
    
    assert len(results) == 1
    assert results[0].id == "c1"
    assert results[0].score == 0.95
    assert results[0].metadata["key"] == "val"

@pytest.mark.asyncio
async def test_search_raises_invalid_response_on_corrupt_payload(qdrant_store, mock_qdrant_client):
    mock_point = MagicMock()
    mock_point.payload = {"wrong": "keys"}
    mock_qdrant_client.search.return_value = [mock_point]
    
    with pytest.raises(InvalidResponseError):
        await qdrant_store.search([0.1]*1536, top_k=1)

@pytest.mark.asyncio
async def test_delete_chunks_uses_match_any(qdrant_store, mock_qdrant_client, models_ref):
    await qdrant_store.delete_chunks(["d1", "d2"])
    
    mock_qdrant_client.delete.assert_called_once()
    models_ref.MatchAny.assert_called_once_with(any=["d1", "d2"])

@pytest.mark.asyncio
async def test_qdrant_client_errors_are_wrapped_in_storage_error(qdrant_store, mock_qdrant_client):
    mock_qdrant_client.upsert.side_effect = Exception("Network error")
    
    chunk = Chunk(
        id="c1", document_id="d1", chunk_index=0, content="test",
        start_char=0, end_char=4, source=SourceRef(source_id="s1", source_type="txt")
    )
    
    with pytest.raises(StorageError, match="Failed to index chunks"):
        await qdrant_store.index_chunks([chunk], [[0.1]*1536])

def test_qdrant_point_id_is_deterministic_uuid(qdrant_store):
    id1 = qdrant_store._qdrant_point_id("chunk-1")
    id2 = qdrant_store._qdrant_point_id("chunk-1")
    id3 = qdrant_store._qdrant_point_id("chunk-2")
    
    assert id1 == id2
    assert id1 != id3
    # Check it is a valid UUID
    import uuid
    uuid.UUID(id1)
