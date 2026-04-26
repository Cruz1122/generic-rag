"""
Example of using QdrantVectorStore with generic-rag.
Requires: pip install generic-rag[qdrant]
"""
import asyncio
from qdrant_client import AsyncQdrantClient
from generic_rag.storage.qdrant import QdrantVectorStore
from generic_rag.core.schemas import Chunk, SourceRef

async def main():
    # 1. Initialize Async Qdrant Client (in-memory for demo)
    client = AsyncQdrantClient(":memory:")
    
    # 2. Initialize the Store
    # vector_size=3 (for demo purposes)
    store = QdrantVectorStore(
        client=client,
        collection_name="demo_collection",
        vector_size=3,
        distance="Cosine"
    )
    
    # 3. Ensure collection exists (recreate=True will clear previous data)
    print("Setting up collection...")
    await store.ensure_collection(recreate=True)
    
    # 4. Prepare some chunks
    source = SourceRef(source_id="doc-123", source_type="txt", title="Demo Doc")
    chunks = [
        Chunk(
            id="chunk-1",
            document_id="doc-123",
            chunk_index=0,
            content="Qdrant is a vector database.",
            start_char=0,
            end_char=28,
            source=source,
            metadata={"category": "tech"}
        ),
        Chunk(
            id="chunk-2",
            document_id="doc-123",
            chunk_index=1,
            content="Generic-rag is agnostic.",
            start_char=29,
            end_char=52,
            source=source,
            metadata={"category": "tech"}
        )
    ]
    
    # 5. Indexing (with mock embeddings)
    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]
    
    print("Indexing chunks...")
    await store.index_chunks(chunks, embeddings)
    
    # 6. Search
    print("Searching for similar chunks...")
    query_vector = [0.9, 0.1, 0.0]
    results = await store.search(query_vector, top_k=2, filters={"metadata.category": "tech"})
    
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Score: {res.score:.4f}):")
        print(f"Content: {res.content}")
        print(f"Metadata: {res.metadata}")

    # 7. Cleanup (Optional, since it's in-memory)
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
