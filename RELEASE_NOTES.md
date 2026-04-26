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
