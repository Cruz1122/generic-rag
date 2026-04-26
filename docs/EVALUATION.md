# Evaluation & Quality Harness

`generic-rag` provides a deterministic, offline evaluation framework to measure the performance of your RAG components (retrieval, reranking, citation, context) without relying on LLMs or external services.

## Core Concepts

- **Materialized Predictions:** Evaluation is performed on static results (chunk IDs and scores) rather than running live pipelines. This ensures reproducibility and speed.
- **Deterministic Metrics:** All metrics are calculated using pure mathematical formulas.
- **Offline First:** No network calls or heavy models required.

## Dataset Formats

### JSON Dataset
A JSON file with a `name` and a list of `examples`.

```json
{
  "name": "documentation-eval",
  "examples": [
    {
      "id": "q1",
      "query": "What is generic-rag?",
      "relevant_chunk_ids": ["chunk-1", "chunk-3"],
      "graded_relevance": {"chunk-1": 3.0, "chunk-3": 1.0},
      "expected_citation_ids": ["chunk-1"],
      "metadata": {"category": "general"}
    }
  ]
}
```

### JSONL Dataset
One `EvaluationExample` object per line. The dataset name is inferred from the filename.

```jsonlines
{"id": "q1", "query": "q1", "relevant_chunk_ids": ["c1"]}
{"id": "q2", "query": "q2", "relevant_chunk_ids": ["c2"]}
```

## Predictions Format

A JSON dictionary mapping `query_id` to a list of `RetrievedItem` objects.

```json
{
  "q1": [
    {"chunk_id": "chunk-1", "score": 0.95},
    {"chunk_id": "chunk-2", "score": 0.82}
  ]
}
```

## Metrics

| Metric | Description |
| --- | --- |
| `precision@k` | Proportion of retrieved chunks in top-k that are relevant. Denominator is always `k`. |
| `recall@k` | Proportion of all relevant chunks that were retrieved in top-k. |
| `hit@k` | 1.0 if at least one relevant chunk is in top-k, else 0.0. |
| `mrr@k` | Reciprocal Rank of the first relevant chunk within the top-k results. |
| `ndcg@k` | Normalized Discounted Cumulative Gain. Uses `graded_relevance` if provided. |
| `citation_coverage` | Proportion of expected citations present in the output. |
| `context_coverage` | Proportion of relevant chunks present in the final context. |

### Edge Case Behavior
- If `relevant_chunk_ids` is empty in the dataset, a `ConfigurationError` is raised.
- If `predictions` are missing for a query, a `ConfigurationError` is raised.
- `precision@k` is calculated as `hits / k` (Classical Rigor). If less than `k` items are retrieved, the missing items are treated as irrelevant.

## CLI Usage

You can evaluate retrieval performance directly from the CLI:

```bash
generic-rag eval retrieval dataset.json predictions.json --k 1,3,5
```

## Python API Usage

```python
from generic_rag.evaluation import load_evaluation_dataset, load_predictions, evaluate_retrieval

dataset = load_evaluation_dataset("dataset.json")
predictions = load_predictions("predictions.json")

report = evaluate_retrieval(dataset, predictions, k_values=[1, 3, 5])

print(f"Aggregated Precision@1: {report.aggregate_metrics['precision@1']}")
```

## Limitations

- **ID-based:** Matches are performed on Chunk IDs. Semantically equivalent but differently IDed chunks count as misses.
- **No LLM-as-a-judge:** This version does not support using LLMs to evaluate generation quality (faithfulness, relevance).
- **Static:** You must materialize your predictions first.
