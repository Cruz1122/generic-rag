# Release Notes

## v0.6.0 (2026-04-26)

**Focus: Integration Adapters and Application Patterns**

- **Added Integration Examples**: New `examples/adapters/` directory showing how to use `generic-rag` in real-world scenarios without core contamination.
    - `simple_domain_adapter.py`: Basic functional wrapper.
    - `service_layer_adapter.py`: Service Layer pattern with custom DTOs.
    - `fastapi_adapter_example.py`: Web API integration using dependency injection.
- **FastAPI Support**: Added optional extra `fastapi` to `pyproject.toml`.
- **New Documentation**: Created `docs/ADAPTERS.md` explaining integration best practices and anti-patterns.
- **Tests**: Added comprehensive offline tests for all new adapter examples.
- **Metadata Handling**: Examples demonstrate using metadata to pass domain-specific information through the pipeline.

## v0.5.0 (2026-04-20)

- Added Gemini REST provider.
- Added support for structured output (JSON schema/object).
- Added `OpenAICompatibleEmbeddingProvider`.
- Added Qdrant vector store support as optional extra.
- Added PDF and HTML loaders as optional extras.
- Hardened LLM dispatcher with retry logic.
