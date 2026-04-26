import pytest
from pathlib import Path
from generic_rag.cli.main import main

def test_cli_inspect_txt(tmp_path, capsys):
    p = tmp_path / "hello.txt"
    p.write_text("hello world", encoding="utf-8")
    
    exit_code = main(["inspect", "file", str(p)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert f"file: {p}" in captured.out
    assert "documents: 1" in captured.out
    assert "document[0].source_type: txt" in captured.out
    assert "document[0].content_length: 11" in captured.out
    assert "document[0].preview: hello world" in captured.out

def test_cli_inspect_md(tmp_path, capsys):
    p = tmp_path / "test.md"
    p.write_text("# Title\ncontent", encoding="utf-8")
    
    exit_code = main(["inspect", "file", str(p)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "document[0].source_type: markdown" in captured.out

def test_cli_inspect_missing(capsys):
    exit_code = main(["inspect", "file", "non_existent.txt"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.err

def test_cli_inspect_unsupported(tmp_path, capsys):
    p = tmp_path / "test.exe"
    p.write_text("binary", encoding="utf-8")
    exit_code = main(["inspect", "file", str(p)])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error: Unsupported file extension" in captured.err
