import pytest
from examples.adapters.service_layer_adapter import (
    RagAssistantService, 
    AppAnswer, 
    FakeLLMDispatcher
)
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.context.xml import XMLContextBuilder

import pytest_asyncio

@pytest_asyncio.fixture
async def service():
    vector_store = InMemoryVectorStore()
    embedding_provider = DeterministicEmbeddingProvider()
    
    # Pre-populate
    from generic_rag.core.schemas import Chunk, SourceRef
    source = SourceRef(
        source_id="test_src", 
        source_type="txt",
        metadata={"source": "test_src"}
    )
    chunk = Chunk(
        id="test_chunk",
        document_id="test_doc",
        chunk_index=0,
        content="Test data content",
        start_char=0,
        end_char=17,
        source=source,
        metadata={}
    )
    vector = await embedding_provider.embed_query(chunk.content)
    await vector_store.index_chunks([chunk], [vector])

    pipeline = DefaultQAPipeline(
        retriever=SimpleRetriever(embedding_provider, vector_store),
        context_builder=XMLContextBuilder(),
        dispatcher=FakeLLMDispatcher()
    )
    return RagAssistantService(pipeline)

@pytest.mark.asyncio
async def test_service_layer_returns_app_answer(service):
    response = await service.answer("test query")
    assert isinstance(response, AppAnswer)
    assert "Service Layer says" in response.answer
    assert len(response.sources) > 0
    assert response.sources[0].source_name == "test_src"

@pytest.mark.asyncio
async def test_service_layer_validation(service):
    with pytest.raises(ValueError, match="Query cannot be empty"):
        await service.answer("  ")
