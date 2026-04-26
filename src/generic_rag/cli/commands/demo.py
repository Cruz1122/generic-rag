import asyncio

from generic_rag.core.schemas import (
    Document, SourceRef, LLMResponse, PipelineRequest, RetrievalRequest, LLMRequest, ChatMessage,
    ProviderInfo, TokenUsage
)
from generic_rag.ingestion.chunkers import CharacterChunker
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.context.xml import XMLContextBuilder
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.llm.base import BaseLLMDispatcher, BaseLLMProvider

class FakeLLMProvider(BaseLLMProvider):
    @property
    def name(self) -> str:
        return "fake"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            text="This is a simulated answer from generic-rag offline demo. I can see the provided context in XML format.",
            usage=TokenUsage(total_tokens=100),
            provider_info=ProviderInfo(name="fake", model=request.model)
        )

    async def stream(self, request: LLMRequest):
        yield "This is a simulated answer"

class FakeLLMDispatcher(BaseLLMDispatcher):
    def register_provider(self, provider: BaseLLMProvider) -> None:
        pass

    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            text="This is a simulated answer from generic-rag offline demo. I can see the provided context in XML format.",
            usage=TokenUsage(total_tokens=100),
            provider_info=ProviderInfo(name="fake", model=request.model)
        )

async def run_offline_demo():
    # 1. Documents in memory
    docs = [
        Document(
            id="1",
            content="generic-rag is a Python library for building RAG pipelines that are provider-agnostic.",
            source=SourceRef(source_id="doc1", source_type="other", title="Demo Doc 1")
        ),
        Document(
            id="2",
            content="It supports multiple LLM providers like OpenAI, Ollama, and Gemini.",
            source=SourceRef(source_id="doc2", source_type="other", title="Demo Doc 2")
        )
    ]

    # 2. Chunker
    chunker = CharacterChunker(chunk_size=100, chunk_overlap=0)
    chunks = chunker.split_documents(docs)

    # 3. Embeddings & Vector Store
    embedder = DeterministicEmbeddingProvider()
    embeddings = await embedder.embed_documents([c.content for c in chunks])
    
    vector_store = InMemoryVectorStore()
    await vector_store.index_chunks(chunks, embeddings)

    # 4. Retriever & Context Builder
    retriever = SimpleRetriever(embedder, vector_store)
    context_builder = XMLContextBuilder()

    # 5. Fake LLM & Pipeline
    dispatcher = FakeLLMDispatcher()
    pipeline = DefaultQAPipeline(
        retriever=retriever,
        context_builder=context_builder,
        dispatcher=dispatcher
    )

    # 6. Run
    question = "What is generic-rag?"
    print("[Demo Offline]")
    print(f"Question: {question}")
    
    request = PipelineRequest(
        query=question,
        retrieval=RetrievalRequest(query=question, top_k=2),
        llm=LLMRequest(model="fake-model", messages=[ChatMessage(role="user", content=question)])
    )
    
    result = await pipeline.run(request)
    
    print(f"Retrieved chunks: {len(result.retrieved_chunks)}")
    print(f"Answer: {result.answer.text}")
    print(f"Citations: {len(result.citations)}")
    
    return 0

def demo_handler(args) -> int:
    try:
        return asyncio.run(run_offline_demo())
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in demo: {e}")
        return 2
