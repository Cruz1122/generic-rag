"""
FastAPI Adapter Example for generic-rag.

This example demonstrates how to integrate generic-rag into a FastAPI application
using dependency injection and a service layer.

Requires: pip install -e ".[fastapi]"
To run with uvicorn: uvicorn examples.adapters.fastapi_adapter_example:app --reload
"""

from typing import List, Optional
from pydantic import BaseModel

# generic-rag imports
from generic_rag.core.schemas import (
    PipelineRequest, LLMRequest, LLMResponse, ProviderInfo, RetrievalRequest
)
from generic_rag.llm.base import BaseLLMDispatcher
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.context.xml import XMLContextBuilder

# FastAPI imports (handled within the example)
try:
    from fastapi import FastAPI, Depends, HTTPException
except ImportError:
    # This allows the file to be parsed even if FastAPI is not installed,
    # though it won't be functional.
    FastAPI = object 
    Depends = lambda x: x
    HTTPException = Exception


# --- Fake Components for Offline Demo ---
class FakeLLMDispatcher(BaseLLMDispatcher):
    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            text="FastAPI Example: The API documentation says we are online.",
            provider_info=ProviderInfo(name="fastapi-mock", model=request.model)
        )

    def register_provider(self, provider):
        pass

    async def stream(self, request: LLMRequest):
        pass


# --- API Schemas ---
class AnswerRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


class CitationDTO(BaseModel):
    content: str
    metadata: dict


class AnswerResponse(BaseModel):
    answer: str
    citations: List[CitationDTO]


# --- Dependency Injection Setup ---
def get_pipeline():
    """
    Factory function to create and configure the RAG pipeline.
    In a real app, you might use a singleton or a more complex DI container.
    """
    vector_store = InMemoryVectorStore()
    embedding_provider = DeterministicEmbeddingProvider()
    
    # Pre-populate with dummy data
    # Note: in a real FastAPI app, you'd probably do this async during startup
    # For this simplified example, we use a trick to run async in sync factory
    import asyncio
    from generic_rag.core.schemas import Chunk, SourceRef
    doc_content = "API Documentation: The generic-rag FastAPI adapter is now online."
    loop = asyncio.new_event_loop()
    vector = loop.run_until_complete(embedding_provider.embed_query(doc_content))
    loop.close()
    
    source = SourceRef(
        source_id="api_docs", 
        source_type="txt",
        metadata={"source": "api_docs"}
    )
    chunk = Chunk(
        id="api_chunk_1",
        document_id="api_doc_1",
        chunk_index=0,
        content=doc_content,
        start_char=0,
        end_char=len(doc_content),
        source=source,
        metadata={}
    )
    
    # We use another trick for indexing
    loop = asyncio.new_event_loop()
    loop.run_until_complete(vector_store.index_chunks([chunk], [vector]))
    loop.close()

    return DefaultQAPipeline(
        retriever=SimpleRetriever(embedding_provider, vector_store),
        context_builder=XMLContextBuilder(),
        dispatcher=FakeLLMDispatcher()
    )


# --- FastAPI App ---
app = FastAPI(title="generic-rag Adapter API")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.6.0"}


@app.post("/answer", response_model=AnswerResponse)
async def answer(
    request: AnswerRequest, 
    pipeline: DefaultQAPipeline = Depends(get_pipeline)
):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Map to generic-rag request
    from generic_rag.core.schemas import ChatMessage
    rag_request = PipelineRequest(
        query=request.query,
        retrieval=RetrievalRequest(query=request.query, top_k=request.top_k),
        llm=LLMRequest(
            model="api-model", 
            messages=[ChatMessage(role="user", content=request.query)]
        )
    )

    # Execute pipeline
    response = await pipeline.run(rag_request)

    # Map to API response
    return AnswerResponse(
        answer=response.answer.text,
        citations=[
            CitationDTO(content=c.snippet, metadata=c.source.metadata) 
            for c in response.citations
        ]
    )


if __name__ == "__main__":
    print("FastAPI adapter example loaded. Use uvicorn to run it.")
