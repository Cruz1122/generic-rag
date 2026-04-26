# Compatibility Policy

This document defines the versioning and compatibility commitments for `generic-rag` starting from version 1.0.0.

## Semantic Versioning (SemVer)

`generic-rag` adheres to [Semantic Versioning 2.0.0](https://semver.org/).

- **Major releases (vX.0.0)**: May include breaking changes to the Stable Public API.
- **Minor releases (v1.X.0)**: Include new features, new optional integrations, or backward-compatible changes to the Stable Public API.
- **Patch releases (v1.0.X)**: Include backward-compatible bug fixes and documentation updates.

## API Classification

To provide clarity on what is safe to depend on, the codebase is classified into three tiers:

### 1. Stable Public API
We commit to maintaining backward compatibility for these modules and classes across minor and patch releases. Breaking changes will only occur in major versions.

- **Core Schemas (`generic_rag.core.schemas`)**: All primary models (`Document`, `Chunk`, `ScoredChunk`, `LLMRequest`, `LLMResponse`, `Citation`, etc.).
- **Exceptions (`generic_rag.core.exceptions`)**: All public exception classes.
- **Configuration**: `ProviderConfig` and its primary fields.
- **Base Interfaces (ABCs)**:
  - `BaseLLMProvider`
  - `BaseLLMDispatcher`
  - `BaseEmbeddingProvider`
  - `BaseDocumentLoader`
  - `BaseChunker`
  - `BaseVectorStore`
  - `BaseRetriever`
  - `BaseReranker`
  - `BaseContextBuilder`
- **Core Implementations**:
  - `DefaultQAPipeline`
  - `SimpleRetriever`
  - `InMemoryVectorStore`
  - `CharacterChunker`
  - `DeterministicEmbeddingProvider`
  - `XMLContextBuilder`
- **Evaluation**:
  - Metric names and mathematical definitions.
  - `EvaluationExample`, `EvaluationDataset`, `RetrievedItem`, `EvaluationReport`.
  - Functions: `evaluate_retrieval`, `load_evaluation_dataset`, `load_predictions`.
- **CLI Commands**:
  - `generic-rag doctor`
  - `generic-rag demo offline`
  - `generic-rag inspect file`
  - `generic-rag provider check-env`
  - `generic-rag eval retrieval`
  - Standard exit codes (0 for success, 1 for general error, 2 for CLI usage error).

### 2. Provisional Public API
These parts are functional and public but may receive minor signature adjustments or behavior refinements in minor releases based on community feedback.

- **Concrete Provider Internals**: The exact mapping of HTTP payloads for OpenAI, Ollama, and Gemini.
- **Optional Integration Details**:
  - `QdrantVectorStore` implementation specifics.
  - `CrossEncoderReranker` implementation specifics.
  - Exact text extraction strategies for `PyMuPDF` and `BeautifulSoup`.
- **CLI Output Formatting**: The exact human-readable text printed to `stdout` (unless a machine-readable flag like `--json` is used).
- **Adapter Examples**: Code in `examples/adapters/`.

### 3. Internal API
No compatibility guarantees are provided for these parts. They may change in patch releases.

- Any module, function, or class prefixed with an underscore (`_`).
- `generic_rag.cli.commands.*` internal implementation logic.
- Retry loop internal state and backoff calculation details.
- Test fakes and internal helpers not exported in package `__init__.py` files.

## Breaking Changes

A breaking change includes:
- Removing or renaming a class/function in the Stable Public API.
- Adding a mandatory parameter to an existing function/method in the Stable Public API.
- Changing the return type of a function in the Stable Public API.
- Raising the minimum supported Python version.

## Deprecation Policy

When we plan to remove or change a Stable Public API, we will:
1. Mark it as deprecated in a minor release using `DeprecationWarning`.
2. Keep the old API functional for at least one full minor release cycle.
3. Remove the API in the next major release.

## Optional Integrations

`generic-rag` uses "extras" for heavy or specific dependencies (e.g., `[qdrant]`, `[pdf]`). Compatibility for these depends on the underlying third-party library. If a third-party library introduces a breaking change, we may be forced to release a minor version of `generic-rag` with updated integration code.
