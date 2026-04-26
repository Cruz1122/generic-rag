# Getting Started

Welcome to `generic-rag`! This guide will walk you through setting up the project locally on your machine, running the offline demo, and preparing your environment for further development.

## Requirements

Before you begin, ensure you have the following installed:

- **Python 3.11+**: The library makes heavy use of modern Python typing and asyncio features.
- **Git**: To clone the repository.
- **PowerShell** (if on Windows): Recommended shell for running the setup commands.
- **Ollama** (Optional): If you plan to test local LLM inference without API costs.

## Installation

### Windows (PowerShell)

1. **Clone the repository**:
   ```powershell
   git clone <repository-url> generic-rag
   cd generic-rag
   ```

2. **Create a virtual environment**:
   ```powershell
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   *(If you get an execution policy error, you may need to run `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` first).*

4. **Upgrade pip and install the package in editable mode**:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   ```

### Linux / macOS (Bash)

1. **Clone the repository**:
   ```bash
   git clone <repository-url> generic-rag
   cd generic-rag
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

4. **Upgrade pip and install the package in editable mode**:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev]"
   ```

## Running the Tests

To ensure everything is installed correctly and functioning as expected, run the offline test suite:

```powershell
# Windows & Linux/macOS
python -m pytest
```

You should see all tests pass successfully. These tests use mocked network responses and do not require API keys.

## Running the Offline Demo

We include a basic RAG pipeline demonstration that runs entirely in memory. It uses deterministic (hash-based) embeddings and a fake LLM response, meaning it requires zero configuration and zero network connectivity.

```powershell
# Windows & Linux/macOS
python examples/basic_qa_demo.py
```

### Interpreting the Output

When you run the demo, you will see:
1. **Ingestion**: The system loads hardcoded markdown/text documents.
2. **Chunking**: Documents are split into smaller pieces.
3. **Embedding & Storage**: Chunks are "embedded" (using a fake hash approach) and stored in the `InMemoryVectorStore`.
4. **Retrieval**: A query is executed against the store, returning the most "relevant" chunks (based on fake cosine similarity).
5. **Context Building**: The chunks are assembled into an XML context block.
6. **LLM Generation**: A mocked LLM provider returns a static answer referencing the context.

## Next Steps

Now that you have the framework running locally:
- Try using your own text files. See [Using Your Own Corpus](USING_YOUR_OWN_CORPUS.md).
- Connect a real LLM like Ollama or OpenAI. See the [Providers Guide](PROVIDERS.md).
- Learn about the underlying design in [Architecture](ARCHITECTURE.md).
