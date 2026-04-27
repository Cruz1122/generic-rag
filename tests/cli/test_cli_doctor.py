from generic_rag.cli.main import main

def test_cli_doctor(capsys):
    exit_code = main(["doctor"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "core: ok" in captured.out
    assert "python: ok" in captured.out
    assert "pydantic: ok" in captured.out
    assert "httpx: ok" in captured.out
    assert "qdrant:" in captured.out
    assert "pdf:" in captured.out
    assert "html:" in captured.out
    assert "fastapi:" in captured.out
    assert "rerankers:" in captured.out
