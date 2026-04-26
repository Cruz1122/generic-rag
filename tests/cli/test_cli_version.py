import pytest
from generic_rag.cli.main import main
from importlib import metadata

def test_cli_version(capsys):
    exit_code = main(["--version"])
    assert exit_code == 0
    captured = capsys.readouterr()
    pkg_version = metadata.version("generic-rag")
    assert f"generic-rag version: {pkg_version}" in captured.out
    assert "python version:" in captured.out
