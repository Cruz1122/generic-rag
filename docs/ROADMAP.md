# Roadmap for generic-rag

### v0.1: Core Contracts & In-Memory Pipeline (Completed)
- Pydantic v2 models and exception hierarchy.
- Base interfaces for the entire ecosystem.
- Lightweight async LLM providers (OpenAI-compatible, Ollama, Gemini).
- Basic ingestion (TXT, MD) and character chunking.
- In-memory storage with cosine similarity.
- Deterministic embedding for testing.
- QA Pipeline with XML Context Builder.
- Extensive test suite and examples without heavy dependencies.

### v0.2: LLM Provider Hardening (Completed)
- Robust error mapping (Auth, Timeout, RateLimit, InvalidResponse).
- Lightweight retry logic with exponential backoff at the Dispatcher level.
- Structured output support (`json_object` and `json_schema` formatting).
- Offline provider documentation, setup guides, and practical examples.

### v0.3: Real Embeddings & CLI Prototype (Completed)
- Support for real embeddings as optional extras (e.g., OpenAI embeddings API via `OpenAICompatibleEmbeddingProvider`).
- `sentence-transformers` deferred to future sub-phase.

### v0.4: Production Vector Stores (Completed)
- [x] `generic-rag[qdrant]`: Integration with Qdrant.

### v0.5: Advanced Loaders (Completed)
- [x] `generic-rag[pdf]`: PyMuPDFLoader.
- [x] `generic-rag[html]`: BeautifulSoup HTML Loader.

### v0.6: More Vector Stores (Planned)
- [ ] `generic-rag[chroma]`: Integration with ChromaDB.
- [ ] `generic-rag[faiss]`: Integration with FAISS.

### v0.7: Adapter Examples (Planned)
- More examples demonstrating integration into larger domains (Adapters).
- Rerankers (CrossEncoders) integration for better retrieval scoring.
