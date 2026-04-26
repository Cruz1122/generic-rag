# Contributing to generic-rag

Thank you for your interest in contributing to `generic-rag`!

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Cruz1122/generic-rag.git
   cd generic-rag
   ```

2. Install in editable mode with development dependencies:
   ```bash
   python -m pip install -e ".[dev]"
   ```

## Testing Guidelines

- **Run all tests**:
  ```bash
  python -m pytest
  ```
- **Verify syntax and compilation**:
  ```bash
  python -m compileall src examples
  ```
- **No Real API Calls**: Unit tests must NEVER make real network requests. Use mocks, fakes, or the built-in `DeterministicEmbeddingProvider`.
- **Offline First**: All core tests must be able to run in an airplane mode environment.

## Design Principles

- **Agnostic Core**: The core library (`src/generic_rag/core`) must not depend on any specific LLM provider, vector store, or web framework.
- **Optional Integrations**: New providers, loaders, or vector stores must be added as optional dependencies (extras) in `pyproject.toml`.
- **Pydantic v2**: All data models must use Pydantic v2 and adhere to existing naming conventions.
- **Type Hints**: Type annotations are mandatory. The project uses `py.typed` to support type checking for consumers.
- **Minimal Dependencies**: Do not add new mandatory dependencies to the `dependencies` section of `pyproject.toml` without a strong justification and approval.

## How to Add New Features

### Adding a New Provider
1. Inherit from `BaseLLMProvider`.
2. Implement the async `generate` method.
3. Add any necessary extra dependencies to `pyproject.toml`.
4. Add comprehensive offline tests using mocks.
5. Update `docs/PROVIDERS.md` and `docs/API_REFERENCE.md`.

### Adding a New Document Loader
1. Inherit from `BaseDocumentLoader`.
2. Implement the `load` method.
3. Add the integration to `src/generic_rag/ingestion/loaders.py`.
4. Document the new loader in `docs/DOCUMENT_LOADERS.md`.

## Documentation

- If you add an extra dependency, update the "Installation" section in `README.md` and relevant guides.
- Ensure all public classes and methods have clear docstrings.

## Commit Style

While we don't enforce a strict format, we prefer clear, descriptive commit messages. Example:
`feat: add support for ChromaDB vector store` or `fix: handle edge case in character chunker`.
