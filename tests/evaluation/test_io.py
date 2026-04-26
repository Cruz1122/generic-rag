import json
import pytest
from generic_rag.core.exceptions import ConfigurationError
from generic_rag.evaluation.io import load_evaluation_dataset, load_predictions

def test_load_evaluation_dataset_json(tmp_path):
    d = tmp_path / "ds.json"
    data = {
        "name": "test",
        "examples": [
            {"id": "q1", "query": "q1", "relevant_chunk_ids": ["c1"]}
        ]
    }
    d.write_text(json.dumps(data))
    ds = load_evaluation_dataset(d)
    assert ds.name == "test"
    assert len(ds.examples) == 1

def test_load_evaluation_dataset_jsonl(tmp_path):
    d = tmp_path / "ds.jsonl"
    d.write_text('{"id": "q1", "query": "q1", "relevant_chunk_ids": ["c1"]}\n')
    ds = load_evaluation_dataset(d)
    assert ds.name == "ds"
    assert len(ds.examples) == 1

def test_load_predictions(tmp_path):
    p = tmp_path / "preds.json"
    data = {
        "q1": [{"chunk_id": "c1", "score": 0.9}]
    }
    p.write_text(json.dumps(data))
    preds = load_predictions(p)
    assert "q1" in preds
    assert preds["q1"][0].chunk_id == "c1"

def test_load_io_errors(tmp_path):
    with pytest.raises(ConfigurationError, match="not found"):
        load_evaluation_dataset(tmp_path / "nope.json")
    
    with pytest.raises(ConfigurationError, match="Unsupported dataset extension"):
        p = tmp_path / "nope.txt"
        p.write_text("dummy")
        load_evaluation_dataset(p)
