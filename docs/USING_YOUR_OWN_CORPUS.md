# Using Your Own Corpus

While `generic-rag` v0.2 does not yet include heavy integrations like PyMuPDF or production vector stores (ChromaDB), it does provide pure Python implementations for text ingestion and in-memory retrieval.

You can easily test the structural pipeline of `generic-rag` using your own `.txt` or `.md` files.

## Warning: Deterministic Embeddings

**Important:** The `DeterministicEmbeddingProvider` included in this version uses SHA-256 hashing to generate vector arrays. **It is not semantic**. Words with similar meanings will not have similar vectors. 

This provider is designed strictly for:
- Smoke tests.
- Offline pipeline validation.
- Structural RAG demonstrations without API dependencies.

For production, you will need to swap this out for a real embedding provider (e.g., integrating `sentence-transformers` or calling an OpenAI embeddings endpoint) in future versions.

## Suggested Directory Structure

Create a folder in your project root to hold your documents:

```text
corpus/
  intro.txt
  notes.md
  architecture.md
```

## Example Script

Create a file named `test_my_corpus.py` in the root of the project with the following code. This script demonstrates the full ingestion, chunking, storage, and retrieval flow.

```python
import os
import asyncio
from generic_rag.ingestion.loaders import TextDocumentLoader, MarkdownDocumentLoader
from generic_rag.ingestion.chunkers import CharacterChunker
from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
from generic_rag.storage.in_memory import InMemoryVectorStore
from generic_rag.retrieval.simple import SimpleRetriever
from generic_rag.core.schemas import RetrievalRequest

async def main():
    print("--- 1. Loading Documents ---")
    documents = []
    corpus_dir = "corpus"
    
    if not os.path.exists(corpus_dir):
        print(f"Directory '{corpus_dir}' not found. Please create it and add some .txt or .md files.")
        return

    for filename in os.listdir(corpus_dir):
        filepath = os.path.join(corpus_dir, filename)
        if filename.endswith(".txt"):
            loader = TextDocumentLoader(filepath)
            documents.extend(await loader.load())
        elif filename.endswith(".md"):
            loader = MarkdownDocumentLoader(filepath)
            documents.extend(await loader.load())

    print(f"Loaded {len(documents)} documents.")

    print("--- 2. Chunking ---")
    chunker = CharacterChunker(chunk_size=500, chunk_overlap=50)
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunker.chunk(doc))
    print(f"Created {len(all_chunks)} chunks.")

    print("--- 3. Embedding and Storage ---")
    embedding_provider = DeterministicEmbeddingProvider(dimensions=64)
    vector_store = InMemoryVectorStore(embedding_provider)
    
    await vector_store.index_chunks(all_chunks)
    print("Indexed chunks in InMemoryVectorStore.")

    print("--- 4. Retrieval ---")
    retriever = SimpleRetriever(vector_store)
    
    query = "What is the main topic of these documents?"
    print(f"Querying: '{query}'")
    
    request = RetrievalRequest(query=query, top_k=3)
    response = await retriever.retrieve(request)
    
    print(f"\nRetrieved {len(response.chunks)} chunks:")
    for i, chunk in enumerate(response.chunks):
        print(f"\n[Result {i+1} | Score: {chunk.score:.4f} | Source: {chunk.source.uri}]")
        print(f"{chunk.content[:150]}...")

if __name__ == "__main__":
    asyncio.run(main())
```

Run the script:

```powershell
python test_my_corpus.py
```

This workflow validates your ingestion pipeline and ensures that your documents are correctly parsed, chunked, and retrievable by the framework's interfaces.
