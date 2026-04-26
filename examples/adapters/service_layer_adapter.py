import asyncio
from dataclasses import dataclass
from typing import List, Optional

from generic_rag.core.schemas import (
    PipelineRequest, 
    LLMRequest, 
    LLMResponse, 
    ProviderInfo,
    RetrievalRequest
)
from generic_rag.llm.base import BaseLLMDispatcher
from generic_rag.pipelines.qa import BaseQAPipeline, DefaultQAPipeline
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.context.xml import XMLContextBuilder


# --- Application Domain DTOs ---
@dataclass
class SourceDTO:
    content: str
    source_name: str


@dataclass
class AppAnswer:
    answer: str
    sources: List[SourceDTO]
    confidence_score: float = 1.0


# --- Service Layer ---
class RagAssistantService:
    """
    Service layer that isolates the application from generic-rag internals.
    """
    def __init__(self, pipeline: BaseQAPipeline):
        self.pipeline = pipeline

    async def answer(self, query: str) -> AppAnswer:
        # 1. Validation
        if not query.strip():
            raise ValueError("Query cannot be empty")

        # 2. Map domain query to generic-rag request
        from generic_rag.core.schemas import ChatMessage
        request = PipelineRequest(
            query=query,
            retrieval=RetrievalRequest(query=query, top_k=3),
            llm=LLMRequest(
                model="gpt-4o", # Domain choice
                messages=[ChatMessage(role="user", content=query)],
                temperature=0.0
            )
        )

        # 3. Call generic-rag
        response = await self.pipeline.run(request)

        # 4. Map generic-rag response back to Domain DTOs
        sources = [
            SourceDTO(
                content=cit.snippet, 
                source_name=cit.source.metadata.get("source", "unknown")
            ) 
            for cit in response.citations
        ]

        return AppAnswer(
            answer=response.answer.text,
            sources=sources
        )


# --- Mock/Fake Implementation for Demo ---
class FakeLLMDispatcher(BaseLLMDispatcher):
    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            text="Service Layer says: The internal project notes confirm Q4.",
            provider_info=ProviderInfo(name="mock", model=request.model)
        )

    def register_provider(self, provider):
        pass

    async def stream(self, request: LLMRequest):
        pass


async def run_service_layer_demo():
    print("--- Running Service Layer Adapter Demo ---")

    # Setup core components
    vector_store = InMemoryVectorStore()
    embedding_provider = DeterministicEmbeddingProvider()
    
    # Pre-populate with some data
    from generic_rag.core.schemas import Chunk, SourceRef
    source = SourceRef(
        source_id="docs.v1", 
        source_type="txt", 
        metadata={"source": "docs.v1"}
    )
    chunk = Chunk(
        id="chunk_1",
        document_id="doc_1",
        chunk_index=0,
        content="Internal project notes: Launch Q4",
        start_char=0,
        end_char=31,
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

    # Initialize Service
    service = RagAssistantService(pipeline)

    # Use Service
    try:
        print("\nSending query: 'launch date'")
        app_res = await service.answer("launch date")
        print(f"App Answer: {app_res.answer}")
        for s in app_res.sources:
            print(f" Source [{s.source_name}]: {s.content}")
            
        print("\nSending empty query...")
        await service.answer("")
    except ValueError as e:
        print(f"Caught expected validation error: {e}")


if __name__ == "__main__":
    asyncio.run(run_service_layer_demo())
