import pytest
from pathlib import Path
from generic_rag.core.exceptions import DocumentLoadError

bs4 = pytest.importorskip("bs4")
from generic_rag.ingestion.html import HTMLDocumentLoader

@pytest.mark.asyncio
async def test_html_loader_extracts_title_and_text():
    html_content = """
    <html>
        <head><title>Test Title</title></head>
        <body>
            <h1>Main Heading</h1>
            <p>This is a paragraph.</p>
        </body>
    </html>
    """
    loader = HTMLDocumentLoader()
    documents = await loader.load(html_content)
    
    assert len(documents) == 1
    doc = documents[0]
    
    assert doc.source.title == "Test Title"
    assert doc.source.source_type == "html"
    assert "Main Heading" in doc.content
    assert "This is a paragraph." in doc.content

@pytest.mark.asyncio
async def test_html_loader_removes_script_style_nav_footer_aside_header_noscript():
    html_content = """
    <html>
        <body>
            <header>Header content</header>
            <nav>Nav content</nav>
            <script>alert('test');</script>
            <style>body { color: red; }</style>
            <aside>Aside content</aside>
            <main>
                <p>Valid content</p>
            </main>
            <footer>Footer content</footer>
            <noscript>No script content</noscript>
        </body>
    </html>
    """
    loader = HTMLDocumentLoader()
    documents = await loader.load(html_content)
    
    doc = documents[0]
    content = doc.content
    
    assert "Valid content" in content
    assert "Header content" not in content
    assert "Nav content" not in content
    assert "alert('test')" not in content
    assert "color: red" not in content
    assert "Aside content" not in content
    assert "Footer content" not in content
    assert "No script content" not in content

@pytest.mark.asyncio
async def test_html_loader_raises_on_missing_file(tmp_path: Path):
    loader = HTMLDocumentLoader()
    missing_file = tmp_path / "does_not_exist.html"
    
    with pytest.raises(DocumentLoadError, match="Archivo no encontrado"):
        await loader.load(missing_file)

@pytest.mark.asyncio
async def test_html_loader_handles_empty_html():
    html_content = "<html><body></body></html>"
    loader = HTMLDocumentLoader()
    documents = await loader.load(html_content)
    
    assert len(documents) == 1
    assert documents[0].content.strip() == ""

@pytest.mark.asyncio
async def test_html_loader_supports_bytes_with_encoding():
    # Usando un caracter especial
    html_content = "<html><body><p>El niño corrió</p></body></html>"
    encoded_bytes = html_content.encode("utf-8")
    
    loader = HTMLDocumentLoader()
    documents = await loader.load(encoded_bytes, encoding="utf-8")
    
    assert len(documents) == 1
    assert "El niño corrió" in documents[0].content
    assert documents[0].source.uri == "memory"
