import pytest
from unittest.mock import AsyncMock, MagicMock
from generic_rag.core.schemas import (
    PipelineRequest, RetrievalRequest, LLMRequest, ScoredChunk, SourceRef,
    RetrievalResponse, LLMResponse, ProviderInfo, TokenUsage, ChatMessage
)
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.reranking.deterministic import DeterministicReranker

@pytest.fixture
def mock_components():
    retriever = MagicMock()
    context_builder = MagicMock()
    dispatcher = MagicMock()
    
    retriever.retrieve = AsyncMock()
    dispatcher.dispatch = AsyncMock()
    
    return retriever, context_builder, dispatcher

@pytest.mark.asyncio
async def test_pipeline_with_reranker(mock_components):
    retriever, context_builder, dispatcher = mock_components
    reranker = DeterministicReranker()
    pipeline = DefaultQAPipeline(retriever, context_builder, dispatcher, reranker=reranker)
    
    source = SourceRef(source_id="doc1", source_type="txt")
    chunks = [
        ScoredChunk(id="c1", document_id="doc1", chunk_index=0, content="Apple", start_char=0, end_char=5, source=source, score=0.9),
        ScoredChunk(id="c2", document_id="doc1", chunk_index=1, content="Banana", start_char=6, end_char=12, source=source, score=0.8)
    ]
    
    retriever.retrieve.return_value = RetrievalResponse(query="Banana", chunks=chunks)
    context_builder.build_context.return_value = "Context"
    dispatcher.dispatch.return_value = LLMResponse(
        text="Answer", 
        usage=TokenUsage(), 
        provider_info=ProviderInfo(name="test", model="test")
    )
    
    request = PipelineRequest(
        query="Banana",
        retrieval=RetrievalRequest(query="Banana", top_k=2),
        llm=LLMRequest(model="test", messages=[ChatMessage(role="user", content="Hi")])
    )
    
    response = await pipeline.run(request)
    
    # Check that reranker was used (Banana should be first)
    assert response.retrieved_chunks[0].id == "c2"
    assert response.retrieved_chunks[0].score == 1.0 # overlap for "Banana"
    
    # Check context builder was called with reranked chunks
    context_builder.build_context.assert_called_once()
    called_chunks = context_builder.build_context.call_args[1]["chunks"]
    assert called_chunks[0].id == "c2"

@pytest.mark.asyncio
async def test_pipeline_without_reranker(mock_components):
    retriever, context_builder, dispatcher = mock_components
    pipeline = DefaultQAPipeline(retriever, context_builder, dispatcher)
    
    source = SourceRef(source_id="doc1", source_type="txt")
    chunks = [
        ScoredChunk(id="c1", document_id="doc1", chunk_index=0, content="Apple", start_char=0, end_char=5, source=source, score=0.9),
        ScoredChunk(id="c2", document_id="doc1", chunk_index=1, content="Banana", start_char=6, end_char=12, source=source, score=0.8)
    ]
    
    retriever.retrieve.return_value = RetrievalResponse(query="Banana", chunks=chunks)
    context_builder.build_context.return_value = "Context"
    dispatcher.dispatch.return_value = LLMResponse(
        text="Answer", 
        usage=TokenUsage(), 
        provider_info=ProviderInfo(name="test", model="test")
    )
    
    request = PipelineRequest(
        query="Banana",
        retrieval=RetrievalRequest(query="Banana", top_k=2),
        llm=LLMRequest(model="test", messages=[ChatMessage(role="user", content="Hi")])
    )
    
    response = await pipeline.run(request)
    
    # No reranker, order preserved
    assert response.retrieved_chunks[0].id == "c1"
    
    context_builder.build_context.assert_called_once()
    called_chunks = context_builder.build_context.call_args[1]["chunks"]
    assert called_chunks[0].id == "c1"
