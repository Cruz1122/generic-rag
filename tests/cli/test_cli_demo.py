from generic_rag.cli.main import main

def test_cli_demo_offline(capsys):
    exit_code = main(["demo", "offline"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "[Demo Offline]" in captured.out
    assert "Question: What is generic-rag?" in captured.out
    assert "Retrieved chunks:" in captured.out
    assert "Answer:" in captured.out
    assert "Citations:" in captured.out
