# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) starting from v1.0.0.

## [Unreleased]

## [1.0.0] - 2026-04-26

### Added
- Official v1.0.0 stabilization release.
- Compatibility Policy (`docs/COMPATIBILITY.md`).
- Release Checklist (`docs/RELEASE_CHECKLIST.md`).
- Contributing Guidelines (`CONTRIBUTING.md`).
- GitHub Actions CI for multi-version Python testing.
- Comprehensive smoke test suite for core functionality and CLI.

### Changed
- Frozen Stable Public API contracts.
- Updated documentation and roadmap.

## [0.9.0] - 2026-04-26

### Added
- Evaluation & Quality Harness for offline performance measurement.
- Metrics: Precision@k, Recall@k, HitRate, MRR, nDCG, Citation Coverage.
- CLI command: `generic-rag eval retrieval`.
- Support for JSON/JSONL evaluation datasets.
- Materialized predictions support.

## [0.8.0] - 2026-04-26

### Added
- Reranking Support with `BaseReranker` contract.
- `DeterministicReranker` (keyword-based) and `CrossEncoderReranker` (semantic).
- `rerankers` optional extra.
- `DefaultQAPipeline` integration for reranking.

## [0.7.0] - 2026-04-26

### Added
- Lightweight CLI with `doctor`, `demo`, `inspect`, and `provider` commands.
- Diagnostic and environment verification tools.

## [0.6.0] - 2026-04-26

### Added
- Integration adapter examples (FastAPI, Service Layer, Simple Domain).
- `fastapi` optional extra.
- Documentation for architectural patterns.

## [0.5.0] - 2026-04-26

### Added
- Optional PDF loader using PyMuPDF (`[pdf]`).
- Optional HTML loader using BeautifulSoup4 (`[html]`).

## [0.4.0] - 2026-04-26

### Added
- Optional Qdrant Vector Store integration (`[qdrant]`).
- Support for persistent vector storage.

## [0.3.0] - 2026-04-26

### Added
- OpenAI-compatible Embedding Provider.
- Environment-based embedding configuration.

## [0.2.0] - 2026-04-26

### Added
- LLM Provider hardening (Ollama, Gemini, OpenAI-compatible).
- Structured output support (JSON Mode/Schema).
- HTTP error mapping and retry dispatcher.

## [0.1.0] - 2026-04-26

### Added
- Initial core contracts and Pydantic v2 schemas.
- Base interfaces for RAG components.
- InMemoryVectorStore and SimpleRetriever.
- Character-based chunking.
- DefaultQAPipeline.
- TXT/MD loaders.
