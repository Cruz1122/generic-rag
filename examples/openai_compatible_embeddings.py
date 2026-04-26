import asyncio
import os
import sys

from generic_rag.embeddings.openai_compatible import OpenAICompatibleEmbeddingProvider
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.core.schemas import Document, SourceRef
from generic_rag.ingestion.chunkers import CharacterChunker

async def main():
    api_key = os.getenv("GENERIC_RAG_EMBEDDINGS_API_KEY")
    base_url = os.getenv("GENERIC_RAG_EMBEDDINGS_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("GENERIC_RAG_EMBEDDINGS_MODEL", "text-embedding-3-small")
    
    if not api_key:
        print("Error: Please set GENERIC_RAG_EMBEDDINGS_API_KEY to run this example.")
        print("Example (Windows): $env:GENERIC_RAG_EMBEDDINGS_API_KEY=\"sk-...\" ; python examples/openai_compatible_embeddings.py")
        print("Example (Linux/Mac): export GENERIC_RAG_EMBEDDINGS_API_KEY=\"sk-...\" && python examples/openai_compatible_embeddings.py")
        sys.exit(1)
        
    print(f"Initializing provider with model: {model} at {base_url}")
    provider = OpenAICompatibleEmbeddingProvider(
        api_key=api_key,
        base_url=base_url,
        model=model
    )
    
    # 1. Embed a single query
    print("\n--- Testing embed_query ---")
    try:
        query_vector = await provider.embed_query("What is the capital of France?")
        print(f"Query embedded successfully! Vector dimensions: {len(query_vector)}")
        print(f"Sample values: {query_vector[:3]}...")
    except Exception as e:
        print(f"Error embedding query: {e}")
        return
        
    # 2. Integration with InMemoryVectorStore
    print("\n--- Testing integration with InMemoryVectorStore ---")
    store = InMemoryVectorStore(embedding_provider=provider)
    
    documents = [
        Document(
            content="Paris is the capital and most populous city of France.",
            source=SourceRef(source_id="doc1", source_type="text", uri="memory://doc1")
        ),
        Document(
            content="Berlin is the capital and largest city of Germany by both area and population.",
            source=SourceRef(source_id="doc2", source_type="text", uri="memory://doc2")
        ),
        Document(
            content="Madrid is the capital and most populous city of Spain.",
            source=SourceRef(source_id="doc3", source_type="text", uri="memory://doc3")
        )
    ]
    
    chunker = CharacterChunker(chunk_size=1000, chunk_overlap=0)
    chunks = []
    for doc in documents:
        chunks.extend(chunker.chunk(doc))
        
    print(f"Indexing {len(chunks)} chunks into vector store...")
    await store.index_chunks(chunks)
    
    query = "Tell me about the capital of France."
    print(f"\nSearching for: '{query}'")
    results = await store.search(query, top_k=1)
    
    if results:
        print(f"Top result: {results[0].content}")
        print(f"Score: {results[0].score:.4f}")
    else:
        print("No results found.")

if __name__ == "__main__":
    asyncio.run(main())
