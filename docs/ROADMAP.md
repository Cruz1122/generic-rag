# Roadmap

`generic-rag` evolves through small, focused releases. The project prioritizes a lightweight core, strict typing, offline tests, optional integrations, and clear boundaries between reusable RAG infrastructure and application-specific adapters.

## Completed

### v0.1.0 — Core Contracts & In-Memory Pipeline

- Pydantic v2 schemas and exception hierarchy.
- Base interfaces for LLMs, embeddings, document loaders, chunkers, vector stores, retrievers, context builders, and pipelines.
- TXT/MD loaders.
- Character-based chunking.
- Deterministic embedding provider for tests and demos.
- In-memory vector store.
- Simple retriever.
- XML context builder.
- Default QA pipeline.
- Offline demo and initial documentation.

### v0.2.0 — LLM Provider Hardening

- OpenAI-compatible provider.
- Ollama provider.
- Gemini REST provider.
- Provider configuration hardening.
- HTTP error mapping.
- Retry handling.
- Structured output support.
- Provider examples and configuration docs.

### v0.3.0 — OpenAI-Compatible Embeddings

- Optional OpenAI-compatible embedding provider.
- Safe environment-based configuration.
- Offline tests with mocked HTTP calls.
- Embeddings guide.
- Deterministic embeddings preserved for tests and demos.

### v0.4.0 — Optional Qdrant Vector Store

- Optional `qdrant` extra.
- `QdrantVectorStore`.
- Deterministic UUIDv5 point IDs.
- Chunk payload preservation.
- Simple exact-match filters.
- Offline unit tests with mocks.
- Qdrant documentation and example.

### v0.5.0 — Optional PDF and HTML Loaders

- Optional `pdf` extra with `PyMuPDFDocumentLoader`.
- Optional `html` extra with `HTMLDocumentLoader`.
- PDF page-level documents.
- HTML text extraction without remote fetching.
- Explicit no-OCR and no-crawling scope.
- Document loader docs and examples.

### v0.6.0 — Adapter Examples & Integration Patterns

- Simple adapter example.
- Service-layer adapter example.
- Optional FastAPI adapter example.
- `fastapi` extra without `uvicorn`.
- Offline tests for adapter examples.
- Adapter architecture guide.

### v0.7.0 — Lightweight CLI

- `generic-rag` console entry point.
- `doctor` command.
- `demo offline` command.
- `inspect file` command.
- `provider check-env` command.
- No Typer, Click, or Rich dependency.
- Offline CLI tests.
- CLI documentation.

### v0.8.0 — Optional Reranking Support

- `BaseReranker`.
- `DeterministicReranker`.
- Optional `CrossEncoderReranker`.
- Optional `rerankers` extra with `sentence-transformers`.
- `DefaultQAPipeline` support for optional reranker injection.
- Retrieval and rerank score preservation.
- Offline tests with mocked CrossEncoder.
- Reranking guide and examples.

## Planned
### v0.9.0 — Evaluation & Quality Harness

- Deterministic, offline evaluation tools for retrieval, reranking, citations, and context quality.
- JSON/JSONL dataset formats for small benchmark datasets.
- Retrieval metrics (Recall@k, Precision@k, MRR).
- Reranking metrics (nDCG@k, MRR).
- Citation and Context coverage checks.
- Materialized predictions support.
- CLI command: `generic-rag eval retrieval`.
- Example evaluation demo and `docs/EVALUATION.md`.

## Planned

### v1.0.0 — API Stabilization

Goal: freeze the public contracts enough for real consumers.

Candidate scope:

- Review public schemas.
- Review base interfaces.
- Review pipeline constructor signatures.
- Review exception hierarchy.
- Review optional extras naming.
- Review import paths.
- Review CLI command stability.
- Add `CHANGELOG.md`.
- Add `CONTRIBUTING.md`.
- Add compatibility policy.
- Add GitHub Actions CI.
- Audit README and docs for outdated claims.
- Define what counts as a breaking change.

Explicitly out of scope:

- New vector stores.
- New model providers.
- New document formats.
- Major pipeline rewrites.

### v1.1.0 — Additional Optional Vector Stores

Goal: expand backend support only after public APIs and evaluation tools are stable.

Candidates:

- `ChromaVectorStore` via optional `chroma` extra.
- `FAISSVectorStore` via optional `faiss` extra.

Rules:

- No vector store dependency in base install.
- Each backend must implement existing vector store contracts.
- Tests must not require external services by default.
- Integration tests must be explicitly marked.
- Documentation must compare tradeoffs against `InMemoryVectorStore` and `QdrantVectorStore`.

### v1.2.0 — Advanced Retrieval Patterns

Candidate scope:

- Hybrid retrieval composition.
- Multi-retriever fusion.
- Score normalization utilities.
- Query expansion hooks.
- Optional BM25 sparse retrieval.

Explicitly out of scope until then:

- Agentic RAG.
- Autonomous planning.
- Multi-step web research.
