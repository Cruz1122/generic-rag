from typing import Dict, List, Optional
from generic_rag.core.exceptions import ConfigurationError
from generic_rag.evaluation.schemas import (
    EvaluationDataset, 
    EvaluationReport, 
    MetricResult, 
    RetrievalEvaluationResult, 
    RetrievedItem
)
from generic_rag.evaluation import metrics

def evaluate_retrieval(
    dataset: EvaluationDataset,
    predictions: Dict[str, List[RetrievedItem]],
    k_values: Optional[List[int]] = None,
) -> EvaluationReport:
    if k_values is None:
        k_values = [1, 3, 5, 10]
    
    if any(k <= 0 for k in k_values):
        raise ConfigurationError("All k_values must be positive integers.")
    
    # Check for duplicate query IDs in dataset
    query_ids = [ex.id for ex in dataset.examples]
    if len(query_ids) != len(set(query_ids)):
        raise ConfigurationError("Duplicate query IDs found in evaluation dataset.")

    per_query_results: List[RetrievalEvaluationResult] = []
    
    for example in dataset.examples:
        if not example.relevant_chunk_ids:
            raise ConfigurationError(f"Query '{example.id}' has no relevant_chunk_ids.")
        
        if example.id not in predictions:
            raise ConfigurationError(f"Prediction missing for query '{example.id}'.")
        
        prediction_items = predictions[example.id]
        
        # Check for duplicate chunk_ids in predictions for this query
        retrieved_ids = []
        seen_chunks = set()
        for item in prediction_items:
            if item.chunk_id in seen_chunks:
                raise ConfigurationError(f"Duplicate chunk_id '{item.chunk_id}' in prediction for query '{example.id}'.")
            seen_chunks.add(item.chunk_id)
            retrieved_ids.append(item.chunk_id)
        
        query_metrics: Dict[str, MetricResult] = {}
        
        # Binary relevance map for metrics that might need it (like nDCG if graded is missing)
        relevance_map = example.graded_relevance or {cid: 1.0 for cid in example.relevant_chunk_ids}
        
        for k in k_values:
            query_metrics[f"precision@{k}"] = MetricResult(value=metrics.precision_at_k(retrieved_ids, example.relevant_chunk_ids, k))
            query_metrics[f"recall@{k}"] = MetricResult(value=metrics.recall_at_k(retrieved_ids, example.relevant_chunk_ids, k))
            query_metrics[f"hit@{k}"] = MetricResult(value=metrics.hit_at_k(retrieved_ids, example.relevant_chunk_ids, k))
            query_metrics[f"mrr@{k}"] = MetricResult(value=metrics.reciprocal_rank_at_k(retrieved_ids, example.relevant_chunk_ids, k))
            query_metrics[f"ndcg@{k}"] = MetricResult(value=metrics.ndcg_at_k(retrieved_ids, relevance_map, k))
        
        per_query_results.append(RetrievalEvaluationResult(
            query_id=example.id,
            metrics=query_metrics
        ))
    
    # Aggregate metrics
    aggregate_metrics: Dict[str, float] = {}
    if per_query_results:
        metric_names = per_query_results[0].metrics.keys()
        for name in metric_names:
            total_value = sum(res.metrics[name].value for res in per_query_results)
            aggregate_metrics[name] = total_value / len(per_query_results)
            
    return EvaluationReport(
        dataset_name=dataset.name,
        aggregate_metrics=aggregate_metrics,
        per_query_results=per_query_results
    )
