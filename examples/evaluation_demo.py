"""
Evaluation Demo for generic-rag v1.0.0.
"""
from generic_rag.evaluation import (
    EvaluationDataset, 
    EvaluationExample, 
    RetrievedItem, 
    evaluate_retrieval
)

def run_evaluation_demo():
    print("--- generic-rag Evaluation Demo ---")
    
    # 1. Define an evaluation dataset
    dataset = EvaluationDataset(
        name="demo-dataset",
        examples=[
            EvaluationExample(
                id="q1",
                query="What is generic-rag?",
                relevant_chunk_ids=["chunk-1", "chunk-3"],
                graded_relevance={"chunk-1": 3.0, "chunk-3": 1.0}
            ),
            EvaluationExample(
                id="q2",
                query="How to use embeddings?",
                relevant_chunk_ids=["chunk-5"]
            )
        ]
    )
    
    # 2. Materialize predictions (e.g. from your pipeline or a JSON file)
    # In a real scenario, you would run your RAG pipeline and collect these results.
    predictions = {
        "q1": [
            RetrievedItem(chunk_id="chunk-1", score=0.95),
            RetrievedItem(chunk_id="chunk-2", score=0.80),
            RetrievedItem(chunk_id="chunk-3", score=0.75),
        ],
        "q2": [
            RetrievedItem(chunk_id="chunk-10", score=0.90),
            RetrievedItem(chunk_id="chunk-5", score=0.85),
        ]
    }
    
    # 3. Run evaluation
    print(f"Evaluating {len(dataset.examples)} examples...")
    report = evaluate_retrieval(dataset, predictions, k_values=[1, 3])
    
    # 4. Show results
    print(f"\nResults for dataset: {report.dataset_name}")
    print("-" * 30)
    for metric, value in sorted(report.aggregate_metrics.items()):
        print(f"{metric:15}: {value:.4f}")
        
    print("\nPer-query reciprocal rank:")
    for res in report.per_query_results:
        rr = res.metrics["reciprocal_rank"].value
        print(f"  {res.query_id}: {rr:.4f}")

if __name__ == "__main__":
    run_evaluation_demo()
