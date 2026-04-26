from generic_rag.cli.main import main

def test_cli_provider_check_env(monkeypatch, capsys):
    monkeypatch.setenv("GENERIC_RAG_PROVIDER", "ollama")
    monkeypatch.setenv("GENERIC_RAG_API_KEY", "sk-12345")
    monkeypatch.setenv("GENERIC_RAG_BASE_URL", "http://localhost:11434")
    
    exit_code = main(["provider", "check-env"])
    assert exit_code == 0
    captured = capsys.readouterr()
    
    assert "GENERIC_RAG_PROVIDER: ollama" in captured.out
    assert "GENERIC_RAG_API_KEY: present (redacted)" in captured.out
    assert "GENERIC_RAG_BASE_URL: present" in captured.out
    assert "sk-12345" not in captured.out
    assert "http://localhost:11434" not in captured.out
    assert "GENERIC_RAG_MODEL: missing" in captured.out
