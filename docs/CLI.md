# CLI Reference

`generic-rag` includes a lightweight command-line interface for diagnostics, file inspection, and quick demos. It is designed to be a developer tool, not a full application framework.

## Installation

The CLI is included with the base package. If you have installed `generic-rag` in editable mode or via pip, it should be available as `generic-rag`.

```bash
pip install generic-rag
```

## Global Options

- `--version`: Show the version of `generic-rag` and Python.
- `-h`, `--help`: Show help message and exit.

## Commands

### `doctor`

Checks the environment and detects which optional dependencies (extras) are installed.

```bash
generic-rag doctor
```

**Example Output:**
```text
core: ok
python: ok (3.11.5)
pydantic: ok
httpx: ok
qdrant: not installed
pdf: ok
html: ok
fastapi: not installed
```

### `demo offline`

Runs a minimal RAG pipeline using only in-memory components and a simulated LLM. No network calls or API keys are required.

```bash
generic-rag demo offline
```

### `inspect file <path>`

Loads a file and shows how `generic-rag` parses it into `Document` objects. This is useful for verifying loader behavior.

```bash
generic-rag inspect file my_document.pdf
```

**Supported Extensions:**
- `.txt`: Text loader.
- `.md`, `.markdown`: Markdown loader.
- `.pdf`: PyMuPDF loader (requires `[pdf]` extra).
- `.html`, `.htm`: HTML loader (requires `[html]` extra).

### `provider check-env`

Checks for the presence of known environment variables used by LLM and Embedding providers.

```bash
generic-rag provider check-env
```

**Note:** For security, API keys are redacted and Base URLs are only shown as "present".

## Exit Codes

- `0`: Success.
- `1`: User error or configuration issue (e.g., file not found, missing extra).
- `2`: Internal error or unexpected exception.

## Limitations

- No network calls by default (except if you were to extend it).
- No interactive chat mode.
- No crawling or OCR.
- Designed for local inspection and setup validation.
