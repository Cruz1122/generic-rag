# generic-rag

**Agnostic framework for RAG (Retrieval-Augmented Generation) and LLM orchestration.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![Async](https://img.shields.io/badge/AsyncIO-ready-009688)
![HTTPX](https://img.shields.io/badge/HTTPX-enabled-0B5FFF)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![Typing](https://img.shields.io/badge/typing-py.typed-blue)
![Status](https://img.shields.io/badge/status-v1.0.0-green)
![License](https://img.shields.io/badge/License-MIT-green)

## What is generic-rag?

`generic-rag` is a pure library of interfaces, Pydantic models, and contracts designed to build RAG pipelines and consume Large Language Models (OpenAI, Gemini, Groq, Ollama, etc.) **without coupling** to business rules, domain logic, or web frameworks (like FastAPI). It includes a lightweight **CLI** for diagnostics, local testing and evaluation.

## Stable API

As of version **1.0.0**, `generic-rag` adheres to strict **Semantic Versioning (SemVer)**. We have defined a [Compatibility Policy](docs/COMPATIBILITY.md) that guarantees stability for our core API and schemas.

## Current status: v1.0.0 (Stable)

We have reached our first major stable milestone:
- **API Stabilization**: Core interfaces and schemas are frozen.
- **Evaluation & Quality Harness**: Production-grade tools to measure RAG performance.
- **Comprehensive Documentation**: Detailed guides for every component.
- **CI/CD**: Automated testing across multiple Python versions.

For a detailed list of changes, see the [CHANGELOG](CHANGELOG.md).

## Installation

See our [Getting Started Guide](docs/GETTING_STARTED.md) for detailed instructions.

```bash
# Clone the repository
git clone https://github.com/Cruz1122/generic-rag.git
cd generic-rag

# Install in editable mode with development dependencies
pip install -e .[dev]
```

## Quickstart: CLI

The CLI is the easiest way to verify your environment and test loaders:

```bash
# Verify dependencies
generic-rag doctor

# Run an offline demo
generic-rag demo offline

# Inspect how a file is loaded into documents
generic-rag inspect file README.md
```

## Quickstart: offline demo (Code)

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
