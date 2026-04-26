import pytest
import tempfile
from pathlib import Path
from generic_rag.ingestion.loaders import TextDocumentLoader, MarkdownDocumentLoader

@pytest.mark.asyncio
async def test_text_loader_from_string():
    loader = TextDocumentLoader()
    docs = await loader.load("Hello world", meta="data")
    assert len(docs) == 1
    assert docs[0].content == "Hello world"
    assert docs[0].source.source_type == "txt"
    assert docs[0].metadata == {"meta": "data"}

@pytest.mark.asyncio
async def test_text_loader_from_file():
    loader = TextDocumentLoader()
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("File content")
        path = f.name
    try:
        docs = await loader.load(path)
        assert len(docs) == 1
        assert docs[0].content == "File content"
        assert docs[0].source.uri == path
    finally:
        Path(path).unlink()

@pytest.mark.asyncio
async def test_markdown_loader_from_bytes():
    loader = MarkdownDocumentLoader()
    docs = await loader.load(b"# Markdown")
    assert len(docs) == 1
    assert docs[0].content == "# Markdown"
    assert docs[0].source.source_type == "markdown"
