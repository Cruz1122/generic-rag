import pytest
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.core.schemas import Chunk, RetrievalRequest, SourceRef

def get_dummy_source():
    return SourceRef(source_id="1", source_type="txt")

@pytest.mark.asyncio
async def test_simple_retriever():
    embedder = DeterministicEmbeddingProvider(dimensions=4)
    store = InMemoryVectorStore()
    
    # index some chunks
    query = "test query"
    target_emb = await embedder.embed_query(query)
    
    chunk1 = Chunk(id="1", document_id="d1", chunk_index=0, content="match", start_char=0, end_char=5, source=get_dummy_source())
    chunk2 = Chunk(id="2", document_id="d2", chunk_index=0, content="no match", start_char=0, end_char=8, source=get_dummy_source())
    
    # chunk1 will have exactly the same embedding as the query (score 1.0)
    # chunk2 will have a random embedding
    other_emb = [0.0, 0.0, 0.0, 0.0] # zero vector, score will be 0.0
    
    await store.index_chunks([chunk1, chunk2], [target_emb, other_emb])
    
    retriever = SimpleRetriever(embedder, store)
    
    request = RetrievalRequest(query=query, top_k=2, score_threshold=0.5)
    response = await retriever.retrieve(request)
    
    assert response.query == query
    assert len(response.chunks) == 1 # only chunk1 passes threshold
    assert response.chunks[0].id == "1"
    assert response.chunks[0].score > 0.99
