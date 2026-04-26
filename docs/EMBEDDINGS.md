# Embeddings in generic-rag

Semantic embeddings are the core of any Retrieval-Augmented Generation (RAG) system, allowing you to convert text into mathematical vectors to perform similarity searches.

`generic-rag` provides an abstraction `BaseEmbeddingProvider` to cleanly separate the generation of these vectors from the storage and retrieval mechanisms.

## Available Providers

### 1. `DeterministicEmbeddingProvider` (Offline / Testing)
This is a lightweight, pseudo-random embedding provider. It uses hashing to generate vectors that are always the same for the exact same text, but **it has zero semantic meaning**.
- **When to use it:** For offline unit tests, structural tests, and fast CI/CD pipelines where you don't want to make real API calls or download heavy local models.
- **Dependencies:** None.

### 2. `OpenAICompatibleEmbeddingProvider` (Real Semantics)
This provider uses an HTTP client (`httpx`) to call any embedding API that complies with the standard OpenAI format (e.g., OpenAI's own API, vLLM, LM Studio, Ollama).
- **When to use it:** When you need real semantic search in production or for functional testing, but you want to keep your application lightweight without installing heavy deep learning dependencies like `torch` or `sentence-transformers` locally.
- **Dependencies:** None beyond the base `httpx` already used for LLMs.

## Configuring `OpenAICompatibleEmbeddingProvider`

You can configure the provider using environment variables or directly in code.

### Example

```python
import os
import asyncio
from generic_rag.embeddings.openai_compatible import OpenAICompatibleEmbeddingProvider
from generic_rag.storage.in_memory import InMemoryVectorStore

async def main():
    provider = OpenAICompatibleEmbeddingProvider(
        api_key=os.getenv("GENERIC_RAG_EMBEDDINGS_API_KEY"),
        base_url=os.getenv("GENERIC_RAG_EMBEDDINGS_BASE_URL", "https://api.openai.com/v1"),
        model=os.getenv("GENERIC_RAG_EMBEDDINGS_MODEL", "text-embedding-3-small")
    )
    
    # Generate an embedding for a query
    vector = await provider.embed_query("What is generic-rag?")
    
    # Use it with a vector store
    store = InMemoryVectorStore(embedding_provider=provider)
    # await store.index_chunks(...)

asyncio.run(main())
```

To run the example from the repository:
```bash
export GENERIC_RAG_EMBEDDINGS_API_KEY="sk-your-key"
python examples/openai_compatible_embeddings.py
```

## Limitations
- The `OpenAICompatibleEmbeddingProvider` expects the JSON response to have a specific structure (`{"data": [{"embedding": [...]}]}`). If your local server deviates from this format, it will raise an `InvalidResponseError`.
- It does not automatically chunk documents; you must use a `CharacterChunker` (or similar) before sending massive texts to the embedding provider to avoid token limits.

## Roadmap
In future versions, we plan to add optional extras for heavy local embeddings, such as `sentence-transformers`, which will run entirely locally without HTTP calls. This will be an optional installation (`pip install generic-rag[sentence-transformers]`) to prevent bloating the base library.
