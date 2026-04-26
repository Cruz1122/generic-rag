import json
import pytest
from generic_rag.cli.main import main

def test_cli_eval_retrieval_success(tmp_path, capsys):
    ds_path = tmp_path / "ds.json"
    ds_path.write_text(json.dumps({
        "name": "test-ds",
        "examples": [{"id": "q1", "query": "q1", "relevant_chunk_ids": ["c1"]}]
    }))
    
    preds_path = tmp_path / "preds.json"
    preds_path.write_text(json.dumps({
        "q1": [{"chunk_id": "c1", "score": 0.9}]
    }))
    
    exit_code = main(["eval", "retrieval", str(ds_path), str(preds_path), "--k", "1"])
    
    assert exit_code == 0
    out, err = capsys.readouterr()
    assert "dataset: test-ds" in out
    assert "examples: 1" in out
    assert "precision@1: 1.0000" in out
    assert "recall@1: 1.0000" in out
    assert "hit@1: 1.0000" in out
    assert "ndcg@1: 1.0000" in out

def test_cli_eval_retrieval_error(tmp_path, capsys):
    exit_code = main(["eval", "retrieval", "non-existent.json", "preds.json"])
    assert exit_code == 1
    out, err = capsys.readouterr()
    assert "Configuration error" in out
