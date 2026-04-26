import pytest
from typing import List
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.core.schemas import (
    PipelineRequest, RetrievalRequest, LLMRequest, ChatMessage,
    ScoredChunk, SourceRef, RetrievalResponse, LLMResponse, ProviderInfo
)
from generic_rag.retrieval.base import BaseRetriever
from generic_rag.context.builder import BaseContextBuilder
from generic_rag.llm.base import BaseLLMDispatcher

class MockRetriever(BaseRetriever):
    async def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        source = SourceRef(source_id="s1", source_type="txt")
        chunk = ScoredChunk(id="c1", document_id="d1", chunk_index=0, content="test content", start_char=0, end_char=12, source=source, score=0.9)
        return RetrievalResponse(query=request.query, chunks=[chunk])

class MockContextBuilder(BaseContextBuilder):
    def build_context(self, chunks: List[ScoredChunk], options) -> str:
        return "MOCKED CONTEXT"

class MockDispatcher(BaseLLMDispatcher):
    def register_provider(self, provider) -> None:
        pass
        
    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        # Check that context was injected
        assert request.messages[-1].content.endswith("User query:\ntest query")
        assert "MOCKED CONTEXT" in request.messages[-1].content
        return LLMResponse(
            text="MOCKED ANSWER",
            provider_info=ProviderInfo(name="mock", model=request.model)
        )

@pytest.mark.asyncio
async def test_default_qa_pipeline():
    pipeline = DefaultQAPipeline(
        retriever=MockRetriever(),
        context_builder=MockContextBuilder(),
        dispatcher=MockDispatcher()
    )
    
    request = PipelineRequest(
        query="test query",
        retrieval=RetrievalRequest(query="test query"),
        llm=LLMRequest(
            model="test-model",
            messages=[ChatMessage(role="user", content="original message")]
        )
    )
    
    response = await pipeline.run(request)
    
    assert response.answer.text == "MOCKED ANSWER"
    assert len(response.retrieved_chunks) == 1
    assert response.retrieved_chunks[0].id == "c1"
    assert len(response.citations) == 1
    assert response.citations[0].chunk_id == "c1"
    
    # Check that original LLM request wasn't mutated
    assert len(request.llm.messages) == 1
