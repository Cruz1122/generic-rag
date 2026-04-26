# Release Notes

## v0.8.0 - Reranking Support

### New Features

- **Reranking Layer**: Introduced a new optional stage in the RAG pipeline after retrieval to reorder chunks for better accuracy.
- **`BaseReranker`**: Abstract contract for implementing custom reranking strategies.
- **`DeterministicReranker`**: A zero-dependency reranker based on keyword overlap. Perfect for testing and lightweight environments.
- **`CrossEncoderReranker`**: Optional semantic reranker using `sentence-transformers`. Requires `pip install "generic-rag[rerankers]"`.
- **Pipeline Integration**: `DefaultQAPipeline` now accepts an optional `reranker` in its constructor and automatically applies it if provided.

### Internal Changes

- Updated `ScoredChunk` to preserve original retrieval scores in `metadata["retrieval_score"]` when reranking.
- Added `rerankers` optional dependency to `pyproject.toml`.

### Documentation

- New guide: `docs/RERANKING.md`.
- Updated API Reference and Roadmap.

## v0.7.0 - CLI & Diagnostic Tools

- Added `generic-rag` CLI command.
- Diagnostic and inspection tools.
- Offline demo mode.
