import argparse
from generic_rag.core.exceptions import ConfigurationError
from generic_rag.evaluation import load_evaluation_dataset, load_predictions, evaluate_retrieval

def eval_retrieval_handler(args: argparse.Namespace) -> int:
    try:
        dataset = load_evaluation_dataset(args.dataset)
        predictions = load_predictions(args.predictions)
        
        k_values = [int(k) for k in args.k.split(",")]
        
        report = evaluate_retrieval(dataset, predictions, k_values=k_values)
        
        print(f"dataset: {report.dataset_name}")
        print(f"examples: {len(report.per_query_results)}")
        
        # Sort metrics for stable output
        sorted_metrics = sorted(report.aggregate_metrics.items())
        for name, value in sorted_metrics:
            print(f"{name}: {value:.4f}")
            
        return 0
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 2
