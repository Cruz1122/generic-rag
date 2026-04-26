import asyncio
import os
from tempfile import NamedTemporaryFile
from generic_rag.core.schemas import (
    PipelineRequest, RetrievalRequest, LLMRequest, ChatMessage, LLMResponse, ProviderInfo
)
from generic_rag.ingestion.loaders import TextDocumentLoader
from generic_rag.ingestion.chunkers import CharacterChunker
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.context.xml import XMLContextBuilder
from generic_rag.pipelines.qa import DefaultQAPipeline
from generic_rag.llm.base import BaseLLMDispatcher, BaseLLMProvider
from generic_rag.core.exceptions import ConfigurationError

class FakeProvider(BaseLLMProvider):
    @property
    def name(self) -> str:
        return "fake_llm"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        # Just return a controlled response
        last_msg = request.messages[-1].content
        return LLMResponse(
            text="This is a controlled fake answer based on the provided context.",
            provider_info=ProviderInfo(name=self.name, model=request.model)
        )

    async def stream(self, request: LLMRequest):
        raise NotImplementedError()

class FakeDispatcher(BaseLLMDispatcher):
    def __init__(self):
        self.provider = FakeProvider()

    def register_provider(self, provider: BaseLLMProvider) -> None:
        pass

    async def dispatch(self, request: LLMRequest) -> LLMResponse:
        return await self.provider.generate(request)

async def main():
    print("--- Starting generic-rag Demo ---")
    
    # 1. Create a temporary text file with some content
    content = (
        "The quick brown fox jumps over the lazy dog. "
        "Artificial Intelligence is transforming the world. "
        "Python is a versatile retrieval with text generation."
    )
    with NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
        f.write(content)
        temp_path = f.name

    try:
        # 2. Load document
        print("1. Loading document...")
        loader = TextDocumentLoader()
        docs = await loader.load(temp_path, title="Demo Document")
        
        # 3. Chunking
        print("2. Chunking document...")
        chunker = CharacterChunker(chunk_size=50, chunk_overlap=10)
        chunks = chunker.split_documents(docs)
        print(f"   Created {len(chunks)} chunks.")

        # 4. Embeddings (Deterministic for demo)
        print("3. Generating embeddings...")
        embedder = DeterministicEmbeddingProvider(dimensions=8)
        embeddings = await embedder.embed_documents([c.content for c in chunks])

        # 5. Indexing in Vector Store
        print("4. Indexing chunks in MemoryVectorStore...")
        store = InMemoryVectorStore()
        await store.index_chunks(chunks, embeddings)

        # 6. Setup Retriever, Context Builder, and Dispatcher
        retriever = SimpleRetriever(embedder, store)
        context_builder = XMLContextBuilder()
        dispatcher = FakeDispatcher()

        # 7. Setup QA Pipeline
        pipeline = DefaultQAPipeline(
            retriever=retriever,
            context_builder=context_builder,
            dispatcher=dispatcher
        )

        # 8. Execute Pipeline
        print("5. Executing QA Pipeline...")
        request = PipelineRequest(
            query="What does RAG stand for?",
            retrieval=RetrievalRequest(
                query="What does RAG stand for?",
                top_k=2
            ),
            llm=LLMRequest(
                model="fake-model",
                messages=[ChatMessage(role="user", content="What does RAG stand for?")]
            )
        )

        response = await pipeline.run(request)

        # 9. Print Results
        print("\n=== RESULTS ===")
        print(f"Answer: {response.answer.text}")
        
        print("\nRetrieved Chunks:")
        for i, chunk in enumerate(response.retrieved_chunks):
            print(f"  {i+1}. [Score: {chunk.score:.4f}] {chunk.content}")

        print("\nCitations:")
        for c in response.citations:
            print(f"  [{c.citation_id}] Doc: {c.source.title if c.source.title else c.document_id} - Snippet: {c.snippet}")
            
    finally:
        os.unlink(temp_path)
        print("\n--- Demo finished ---")

if __name__ == "__main__":
    asyncio.run(main())
