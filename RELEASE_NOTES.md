# v0.5.0 release notes

Added optional advanced loaders for PDF and HTML, maintaining the core lightweight and free of heavy dependencies.

Includes:
- `PyMuPDFDocumentLoader` (via `pip install ".[pdf]"`)
- `HTMLDocumentLoader` (via `pip install ".[html]"`)
- Added `"html"` type to `SourceRef.source_type` schema.
- Added `docs/DOCUMENT_LOADERS.md` documentation.
- Examples for both PDF and HTML loaders.

# v0.1.0 release notes

Initial generic RAG MVP.

Includes:
- Pydantic v2 schemas
- base interfaces
- LLM providers and dispatcher
- TXT/MD loaders
- CharacterChunker
- DeterministicEmbeddingProvider
- InMemoryVectorStore
- SimpleRetriever
- XMLContextBuilder
- citation builder
- DefaultQAPipeline
- offline demo
- architecture and roadmap docs

Does not include:
- AALIE-specific logic
- FastAPI
- ChromaDB
- FAISS
- sentence-transformers
- PDF/OCR loaders
- LangChain

Validation:
- pytest passing
- compileall passing
