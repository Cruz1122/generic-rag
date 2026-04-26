# Roadmap

`generic-rag` evolves through small, focused releases. The project prioritizes a lightweight core, strict typing, offline tests, optional integrations, and clear boundaries between reusable RAG infrastructure and application-specific adapters.

## Completed

### v1.0.0 — API Stabilization

- Frozen Public API contracts and Pydantic schemas.
- Compatibility Policy (`docs/COMPATIBILITY.md`).
- Official CHANGELOG and contributing guidelines.
- GitHub Actions CI for multi-version Python testing.
- Release checklist and smoke test suite.

### v0.9.0 — Evaluation & Quality Harness

- Deterministic, offline evaluation tools for retrieval, reranking, citations, and context quality.
- JSON/JSONL dataset formats for small benchmark datasets.
- Retrieval metrics (Recall@k, Precision@k, MRR).
- Reranking metrics (nDCG@k, MRR).
- Citation and Context coverage checks.
- Materialized predictions support.
- CLI command: `generic-rag eval retrieval`.
- Example evaluation demo and `docs/EVALUATION.md`.

## Planned

### v1.1.0 — Additional Optional Vector Stores

Goal: expand backend support only after public APIs and evaluation tools are stable.

Candidates:

- `ChromaVectorStore` via optional `chroma` extra.
- `FAISSVectorStore` via optional `faiss` extra.

### v1.2.0 — Advanced Retrieval Patterns

Candidate scope:

- Hybrid retrieval composition.
- Multi-retriever fusion.
- Score normalization utilities.
- Query expansion hooks.
- Optional BM25 sparse retrieval.

### v1.3.0 — Optional Semantic/LLM Evaluation

Candidate scope:
- LLM-as-a-judge patterns (optional extra).
- Semantic answer similarity metrics.
- Faithfulness and relevancy checks via external providers.
