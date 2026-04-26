# Roadmap for generic-rag

### v0.1.0: Core Contracts & In-Memory Pipeline (Completed)
- Pydantic v2 models and exception hierarchy.
- Base interfaces for the entire ecosystem.
- Lightweight async LLM providers (OpenAI-compatible, Ollama, Gemini).
- Basic ingestion (TXT, MD) and character chunking.
- In-memory storage with cosine similarity.
- Deterministic embedding for testing.
- QA Pipeline with XML Context Builder.
- Extensive test suite and examples without heavy dependencies.

### v0.2.0: LLM Provider Hardening (Completed)
- Robust error mapping (Auth, Timeout, RateLimit, InvalidResponse).
- Lightweight retry logic with exponential backoff at the Dispatcher level.
- Structured output support (`json_object` and `json_schema` formatting).
- Offline provider documentation, setup guides, and practical examples.

### v0.3.0: OpenAI-Compatible Embeddings (Completed)
- Support for real embeddings as optional extras (OpenAI embeddings API).
- `OpenAICompatibleEmbeddingProvider` implementation.

### v0.4.0: Optional Qdrant Vector Store (Completed)
- `generic-rag[qdrant]`: Integration with Qdrant vector database.
- Production-ready storage interface.

### v0.5.0: Optional PDF and HTML Loaders (Completed)
- `generic-rag[pdf]`: PyMuPDF-based Document Loader.
- `generic-rag[html]`: BeautifulSoup4-based HTML Loader.

### v0.6.0: Adapter Examples & Integration Patterns (Completed)
- **Adapter Examples**: Formalized patterns for connecting generic-rag to applications (FastAPI, Service Layer).
- **FastAPI Support**: Optional extra `[fastapi]` for easy web API integration.
- **Integration Guide**: `docs/ADAPTERS.md`.

### v0.7.0: Optional CLI (Planned)
- Lightweight CLI for testing pipelines.
- Configuration management via ENV and YAML.

### v0.8.0: Optional Rerankers (Planned)
- Rerankers (CrossEncoders) integration for better retrieval scoring.
- Hybrid search (BM25 + Vector) support.

### v0.9.0: Additional Optional Vector Stores (Planned)
- `generic-rag[chroma]`: Integration with ChromaDB.
- `generic-rag[faiss]`: Integration with FAISS.

### v1.0.0: API Stabilization (Planned)
- Final contract review.
- Comprehensive API documentation.
- Long-term support (LTS) release.
