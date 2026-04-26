import asyncio
from typing import List

from generic_rag.core.schemas import (
    PipelineRequest, 
    LLMRequest, 
    ChatMessage, 
    LLMResponse, 
    ProviderInfo,
    RetrievalRequest
)
from generic_rag.llm.base import BaseLLMDispatcher
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.ingestion.chunkers import CharacterChunker
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.context.xml import XMLContextBuilder
from generic_rag.pipelines.qa import DefaultQAPipeline


class FakeLLMDispatcher(BaseLLMDispatcher):
    """
    A fake dispatcher for offline examples and testing.
    In a real application, you would use DefaultLLMDispatcher with a real provider.
    """
    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        # Simple fake logic: if context is present, pretend to use it.
        # DefaultQAPipeline injects context into the last message.
        last_message = request.messages[-1].content
        
        if "Retrieved context:" in last_message:
            text = "Based on the internal project notes, the product launch is scheduled for Q4."
        else:
            text = "I don't have enough information to answer that."
            
        return LLMResponse(
            text=text,
            provider_info=ProviderInfo(name="fake-provider", model="fake-model")
        )

    def register_provider(self, provider):
        pass

    async def stream(self, request: LLMRequest):
        raise NotImplementedError("Streaming not implemented in fake dispatcher")


async def run_simple_adapter_demo():
    print("--- Running Simple Domain Adapter Demo ---")

    # 1. Setup Components (In-Memory/Offline)
    vector_store = InMemoryVectorStore()
    embedding_provider = DeterministicEmbeddingProvider()
    chunker = CharacterChunker(chunk_size=100, chunk_overlap=20)
    
    # 2. Populate Knowledge Base
    documents = [
        "Internal Project Notes: The product launch is scheduled for Q4 2024.",
        "Internal Project Notes: Team Alpha is responsible for the core engine.",
        "Generic Product Handbook: Our support hours are 9 AM to 5 PM EST."
    ]
    
    print("Ingesting documents...")
    from generic_rag.core.schemas import Document, SourceRef
    for i, doc_text in enumerate(documents):
        doc = Document(
            id=f"doc_{i}",
            content=doc_text, 
            source=SourceRef(
                source_id=f"doc_{i}", 
                source_type="txt",
                metadata={"source": "internal_notes"}
            )
        )
        chunks = chunker.split_documents([doc])
        # In a real app, you'd use an IngestionPipeline, but we do it manually here for simplicity
        for chunk in chunks:
            vector = await embedding_provider.embed_query(chunk.content)
            await vector_store.index_chunks([chunk], [vector])

    # 3. Initialize Pipeline
    retriever = SimpleRetriever(embedding_provider, vector_store)
    context_builder = XMLContextBuilder()
    dispatcher = FakeLLMDispatcher()
    
    pipeline = DefaultQAPipeline(
        retriever=retriever,
        context_builder=context_builder,
        dispatcher=dispatcher
    )

    # 4. Define Domain Wrapper
    async def answer_query(query: str) -> dict:
        """
        Application-level wrapper that encapsulates generic-rag usage.
        """
        request = PipelineRequest(
            query=query,
            retrieval=RetrievalRequest(query=query, top_k=2),
            llm=LLMRequest(
                model="fake-model", 
                messages=[ChatMessage(role="user", content=query)]
            )
        )
        
        response = await pipeline.run(request)
        
        # Transform PipelineResponse into an application-friendly dictionary
        return {
            "answer": response.answer.text,
            "sources": [
                {
                    "content": citation.snippet,
                    "metadata": citation.source.metadata
                } for citation in response.citations
            ]
        }

    # 5. Execute Queries
    queries = [
        "When is the product launch?",
        "What are the support hours?"
    ]

    for q in queries:
        print(f"\nQuery: {q}")
        result = await answer_query(q)
        print(f"Answer: {result['answer']}")
        print(f"Sources found: {len(result['sources'])}")


if __name__ == "__main__":
    asyncio.run(run_simple_adapter_demo())
