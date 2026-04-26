import pytest
from generic_rag.storage.in_memory import InMemoryVectorStore, cosine_similarity
from generic_rag.core.schemas import Chunk
from generic_rag.core.exceptions import StorageError

def test_cosine_similarity():
    assert cosine_similarity([1, 0], [1, 0]) == 1.0
    assert cosine_similarity([1, 0], [0, 1]) == 0.0
    assert round(cosine_similarity([1, 1], [1, 1]), 5) == 1.0

@pytest.mark.asyncio
async def test_vector_store_basic():
    store = InMemoryVectorStore()
    chunk1 = Chunk(id="1", document_id="d1", chunk_index=0, content="a", start_char=0, end_char=1, metadata={"type": "a"})
    chunk2 = Chunk(id="2", document_id="d1", chunk_index=1, content="b", start_char=1, end_char=2, metadata={"type": "b"})
    
    await store.index_chunks([chunk1, chunk2], [[1.0, 0.0], [0.0, 1.0]])
    
    # search close to chunk1
    results = await store.search([0.9, 0.1], top_k=1)
    assert len(results) == 1
    assert results[0].id == "1"

    # search close to chunk2 with filter
    results = await store.search([0.1, 0.9], top_k=1, filters={"type": "b"})
    assert len(results) == 1
    assert results[0].id == "2"

@pytest.mark.asyncio
async def test_vector_store_delete():
    store = InMemoryVectorStore()
    chunk1 = Chunk(id="1", document_id="d1", chunk_index=0, content="a", start_char=0, end_char=1)
    chunk2 = Chunk(id="2", document_id="d2", chunk_index=0, content="b", start_char=0, end_char=1)
    
    await store.index_chunks([chunk1, chunk2], [[1.0, 0.0], [0.0, 1.0]])
    await store.delete_chunks(["d1"])
    
    assert len(store._chunks) == 1
    assert store._chunks[0].id == "2"

@pytest.mark.asyncio
async def test_vector_store_validation():
    store = InMemoryVectorStore()
    with pytest.raises(StorageError):
        await store.index_chunks([], [[1.0]])
