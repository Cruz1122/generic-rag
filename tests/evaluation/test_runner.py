import pytest
from generic_rag.core.exceptions import ConfigurationError
from generic_rag.evaluation.schemas import EvaluationDataset, EvaluationExample, RetrievedItem
from generic_rag.evaluation.runner import evaluate_retrieval

def test_evaluate_retrieval_success():
    dataset = EvaluationDataset(
        name="test-ds",
        examples=[
            EvaluationExample(id="q1", query="q1", relevant_chunk_ids=["c1"]),
            EvaluationExample(id="q2", query="q2", relevant_chunk_ids=["c2"]),
        ]
    )
    predictions = {
        "q1": [RetrievedItem(chunk_id="c1", score=0.9)],
        "q2": [RetrievedItem(chunk_id="other", score=0.8)],
    }
    
    report = evaluate_retrieval(dataset, predictions, k_values=[1])
    
    assert report.dataset_name == "test-ds"
    assert len(report.per_query_results) == 2
    # q1: prec@1=1.0, recall@1=1.0, hit@1=1.0
    # q2: prec@1=0.0, recall@1=0.0, hit@1=0.0
    # Aggregates: 0.5
    assert report.aggregate_metrics["precision@1"] == 0.5
    assert report.aggregate_metrics["recall@1"] == 0.5
    assert report.aggregate_metrics["hit@1"] == 0.5
    assert report.aggregate_metrics["mrr@1"] == 0.5

def test_evaluate_retrieval_missing_prediction():
    dataset = EvaluationDataset(
        name="test-ds",
        examples=[EvaluationExample(id="q1", query="q1", relevant_chunk_ids=["c1"])]
    )
    predictions = {}
    with pytest.raises(ConfigurationError, match="Prediction missing"):
        evaluate_retrieval(dataset, predictions)

def test_evaluate_retrieval_duplicate_query_id():
    dataset = EvaluationDataset(
        name="test-ds",
        examples=[
            EvaluationExample(id="q1", query="q1", relevant_chunk_ids=["c1"]),
            EvaluationExample(id="q1", query="q1 bis", relevant_chunk_ids=["c1"]),
        ]
    )
    with pytest.raises(ConfigurationError, match="Duplicate query IDs"):
        evaluate_retrieval(dataset, {})

def test_evaluate_retrieval_duplicate_chunk_id():
    dataset = EvaluationDataset(
        name="test-ds",
        examples=[EvaluationExample(id="q1", query="q1", relevant_chunk_ids=["c1"])]
    )
    predictions = {
        "q1": [
            RetrievedItem(chunk_id="c1", score=0.9),
            RetrievedItem(chunk_id="c1", score=0.8),
        ]
    }
    with pytest.raises(ConfigurationError, match="Duplicate chunk_id"):
        evaluate_retrieval(dataset, predictions)

def test_evaluate_retrieval_invalid_k():
    dataset = EvaluationDataset(name="t", examples=[])
    with pytest.raises(ConfigurationError, match="positive integers"):
        evaluate_retrieval(dataset, {}, k_values=[0])
