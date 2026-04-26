import json
from pathlib import Path
from typing import Dict, List, Union
from generic_rag.core.exceptions import ConfigurationError
from generic_rag.evaluation.schemas import EvaluationDataset, EvaluationExample, RetrievedItem

def load_evaluation_dataset(path: Union[str, Path]) -> EvaluationDataset:
    path = Path(path)
    if not path.exists():
        raise ConfigurationError(f"Dataset file not found: {path}")
    
    try:
        if path.suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            dataset = EvaluationDataset.model_validate(data)
        elif path.suffix == ".jsonl":
            examples = []
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if not line.strip():
                        continue
                    try:
                        ex_data = json.loads(line)
                        examples.append(EvaluationExample.model_validate(ex_data))
                    except Exception as e:
                        raise ConfigurationError(f"Error parsing JSONL line {i+1} in {path}: {e}")
            dataset = EvaluationDataset(name=path.stem, examples=examples)
        else:
            raise ConfigurationError(f"Unsupported dataset extension: {path.suffix}. Use .json or .jsonl")
    except Exception as e:
        if isinstance(e, ConfigurationError):
            raise e
        raise ConfigurationError(f"Error loading dataset from {path}: {e}")
    
    # Check for duplicate query IDs
    query_ids = [ex.id for ex in dataset.examples]
    if len(query_ids) != len(set(query_ids)):
        raise ConfigurationError(f"Duplicate query IDs found in dataset {path}")
        
    return dataset

def load_predictions(path: Union[str, Path]) -> Dict[str, List[RetrievedItem]]:
    path = Path(path)
    if not path.exists():
        raise ConfigurationError(f"Predictions file not found: {path}")
    
    if path.suffix != ".json":
        raise ConfigurationError(f"Unsupported predictions extension: {path.suffix}. Only .json is supported")
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        predictions: Dict[str, List[RetrievedItem]] = {}
        for q_id, items in data.items():
            if not isinstance(items, list):
                 raise ConfigurationError(f"Predictions for query '{q_id}' must be a list of items.")
            
            parsed_items = []
            seen_chunks = set()
            for i, item in enumerate(items):
                p_item = RetrievedItem.model_validate(item)
                if p_item.chunk_id in seen_chunks:
                    raise ConfigurationError(f"Duplicate chunk_id '{p_item.chunk_id}' in predictions for query '{q_id}'.")
                seen_chunks.add(p_item.chunk_id)
                parsed_items.append(p_item)
            predictions[q_id] = parsed_items
            
        return predictions
    except Exception as e:
        if isinstance(e, ConfigurationError):
            raise e
        raise ConfigurationError(f"Error loading predictions from {path}: {e}")
