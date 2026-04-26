import pytest
from generic_rag.cli.main import main

def test_cli_version(capsys):
    """Verify 'generic-rag --version' returns success and version string."""
    code = main(["--version"])
    assert code == 0
    captured = capsys.readouterr()
    assert "1.0.0" in captured.out

def test_cli_help(capsys):
    """Verify 'generic-rag --help' returns success and usage instructions."""
    # argparse might call sys.exit for --help depending on version/config, 
    # but usually main returns or it raises SystemExit.
    # Let's handle both.
    try:
        code = main(["--help"])
        assert code == 0
    except SystemExit as e:
        assert e.code == 0
    
    captured = capsys.readouterr()
    assert "usage: generic-rag" in captured.out

def test_cli_doctor(capsys):
    """Verify 'generic-rag doctor' returns success."""
    code = main(["doctor"])
    assert code == 0
    captured = capsys.readouterr()
    assert "core: ok" in captured.out
    assert "python: ok" in captured.out

def test_cli_provider_check_env(capsys):
    """Verify 'generic-rag provider check-env' returns success."""
    code = main(["provider", "check-env"])
    assert code == 0
    captured = capsys.readouterr()
    assert "GENERIC_RAG_PROVIDER" in captured.out
