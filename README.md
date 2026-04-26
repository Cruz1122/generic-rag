# generic-rag

**Agnostic framework for RAG (Retrieval-Augmented Generation) and LLM orchestration.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Async](https://img.shields.io/badge/AsyncIO-ready-009688)
![HTTPX](https://img.shields.io/badge/HTTPX-enabled-0B5FFF)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![Typing](https://img.shields.io/badge/typing-py.typed-blue)
![Status](https://img.shields.io/badge/status-v0.2-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## What is generic-rag?

`generic-rag` is a pure library of interfaces, Pydantic models, and contracts designed to build RAG pipelines and consume Large Language Models (OpenAI, Gemini, Groq, Ollama, etc.) **without coupling** to business rules, domain logic, or web frameworks (like FastAPI). It solves the problem of having LLM logic, specific prompts, and vector retrieval tightly coupled, allowing you to reuse the core infrastructure across multiple projects.

## What it is NOT

- It does not include heavy, production-ready VectorStores (ChromaDB, FAISS, Qdrant) by default (planned for future optional extensions).
- It does not include heavy document loaders (PyMuPDF, OCR) by default.
- It does not use heavy semantic embeddings (like Sentence Transformers) out of the box.
- It does not rely on bloated SDKs (LangChain, LlamaIndex).
- It is not a web API or a ready-to-deploy web application.

## Features

- Strict Pydantic (v2) contracts for LLMs, Embeddings, Documents, and Chunks.
- Abstract base interfaces for Providers, Dispatchers, Retrievers, ContextBuilders, and VectorStores.
- **LLM Providers**: Asynchronous implementations based on `httpx` for OpenAI-compatible (Groq, LMStudio, vLLM), Ollama, and Gemini REST API.
- **Dispatcher**: Built-in lightweight retry logic and error mapping.
- **Structured Output**: Native support for JSON modes and schema enforcement across providers.
- **Ingestion**: Pure `TextDocumentLoader` and `MarkdownDocumentLoader`.
- **Chunking**: `CharacterChunker` with overlap support.
- **Storage & Retrieval**: `InMemoryVectorStore` with pure Python cosine similarity, and an agnostic `SimpleRetriever`.
- **Pipeline**: `DefaultQAPipeline` orchestrating retrieval, context injection, and LLM dispatching.

## Current status: v0.2

We are currently at version **0.2**, which includes:
- Hardened LLM provider layer with `max_retries` and strict HTTP error mapping.
- Support for structured output (JSON schema/object).
- Configurable `ProviderConfig` supporting secure `SecretStr` management.
- Full suite of passing offline tests (37/37).
- Real-world provider examples (Ollama, OpenAI-compatible).

## Installation

See our [Getting Started Guide](docs/GETTING_STARTED.md) for detailed instructions.

```bash
# Clone the repository
git clone https://github.com/your-org/generic-rag.git
cd generic-rag

# Install in editable mode with development dependencies
pip install -e .[dev]
```

## Quickstart: offline demo

You can run a functional demo that runs entirely in memory without network requirements:

```bash
python examples/basic_qa_demo.py
```

*Note: The offline demo uses `DeterministicEmbeddingProvider` which generates pseudo-random vectors based on the text hash. **It is not semantic** and is only useful for structural tests and demos.*

## Quickstart: use your own TXT/MD corpus

You can easily ingest your own text or markdown files using the built-in loaders and test the pipeline structurally. Read the [Using Your Own Corpus](docs/USING_YOUR_OWN_CORPUS.md) guide.

## Provider setup

`generic-rag` supports multiple providers. Read the detailed [Providers Guide](docs/PROVIDERS.md) for full configuration details.

### Ollama local
Requires Ollama running locally:
```powershell
$env:GENERIC_RAG_BASE_URL="http://localhost:11434"
$env:GENERIC_RAG_MODEL="llama3"
python examples/ollama_chat.py
```

### OpenAI-compatible provider
Works for OpenAI, Groq, LM Studio, etc.:
```powershell
$env:GENERIC_RAG_BASE_URL="https://api.openai.com/v1"
$env:GENERIC_RAG_API_KEY="sk-..."
$env:GENERIC_RAG_MODEL="gpt-4o"
python examples/openai_compatible_chat.py
```

### Gemini REST provider
Uses the Google Gemini REST API. Set `$env:GENERIC_RAG_API_KEY` and construct a `GeminiProvider`.

## Structured output support

`generic-rag` natively supports requesting structured JSON output from LLMs via the `response_format` and `json_schema` fields in `LLMRequest`. Read the [Structured Output Guide](docs/STRUCTURED_OUTPUT.md) for capabilities and limitations per provider.

## Error handling and retries

The library maps raw HTTP errors into a clean, contextual hierarchy (`ProviderAuthError`, `ProviderTimeoutError`, `ProviderRateLimitError`, `InvalidResponseError`). The `DefaultLLMDispatcher` automatically retries transient errors based on the provider's `ProviderConfig`.

## Project architecture

Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for a comprehensive overview of the design, interfaces, and separation of concerns.

## Examples

Explore the `examples/` directory for ready-to-run scripts demonstrating chat and RAG capabilities with various providers.

## Testing

Tests are written using `pytest`. They do not make real network calls.
```bash
python -m pytest
```

## Roadmap

Check out [ROADMAP.md](docs/ROADMAP.md) to see what is planned for future versions (e.g., real semantic embeddings, ChromaDB integrations).

## Repository layout

- `src/generic_rag/`: Core library code.
- `tests/`: Offline test suite.
- `examples/`: Runnable demo scripts.
- `docs/`: Detailed documentation and guides.

## Troubleshooting

Having issues? See our [Troubleshooting Guide](docs/TROUBLESHOOTING.md) for common problems and solutions.

## License

MIT License
Placeholder)
