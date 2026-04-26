import pytest
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider

@pytest.mark.asyncio
async def test_deterministic_embedding():
    provider = DeterministicEmbeddingProvider(dimensions=4)
    v1 = await provider.embed_query("hello")
    v2 = await provider.embed_query("hello")
    v3 = await provider.embed_query("world")
    
    assert len(v1) == 4
    assert v1 == v2
    assert v1 != v3

@pytest.mark.asyncio
async def test_embed_documents():
    provider = DeterministicEmbeddingProvider(dimensions=4)
    vectors = await provider.embed_documents(["a", "b"])
    assert len(vectors) == 2
    assert len(vectors[0]) == 4
