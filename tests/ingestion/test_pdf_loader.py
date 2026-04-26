import pytest
import uuid
from pathlib import Path
from generic_rag.core.exceptions import DocumentLoadError

fitz = pytest.importorskip("fitz")
from generic_rag.ingestion.pdf import PyMuPDFDocumentLoader

@pytest.fixture
def temp_pdf(tmp_path: Path) -> Path:
    """Crea un PDF temporal simple con fitz para pruebas."""
    doc = fitz.Document()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello from page 1")
    page2 = doc.new_page()
    page2.insert_text((50, 50), "Hello from page 2")
    
    # Agregar metadata para probar su extracción
    doc.set_metadata({"title": "Test PDF Document"})
    
    file_path = tmp_path / "test.pdf"
    doc.save(str(file_path))
    doc.close()
    return file_path

@pytest.fixture
def empty_pdf(tmp_path: Path) -> Path:
    """Crea un PDF con una página en blanco."""
    doc = fitz.Document()
    doc.new_page()  # Página vacía sin texto
    file_path = tmp_path / "empty.pdf"
    doc.save(str(file_path))
    doc.close()
    return file_path

@pytest.mark.asyncio
async def test_pdf_loader_loads_pages_correctly(temp_pdf: Path):
    loader = PyMuPDFDocumentLoader()
    documents = await loader.load(temp_pdf)
    
    assert len(documents) == 2
    assert "Hello from page 1" in documents[0].content
    assert "Hello from page 2" in documents[1].content
    assert documents[0].source.page == 1
    assert documents[1].source.page == 2

@pytest.mark.asyncio
async def test_pdf_loader_preserves_page_metadata(temp_pdf: Path):
    loader = PyMuPDFDocumentLoader()
    documents = await loader.load(temp_pdf)
    
    assert documents[0].source.source_type == "pdf"
    assert documents[0].source.title == "Test PDF Document"
    assert documents[0].source.uri == str(temp_pdf)
    assert documents[0].source.metadata["total_pages"] == 2
    assert documents[0].source.metadata["extraction_method"] == "pymupdf"
    assert "pdf_metadata" in documents[0].source.metadata

@pytest.mark.asyncio
async def test_pdf_loader_raises_on_missing_file(tmp_path: Path):
    loader = PyMuPDFDocumentLoader()
    missing_file = tmp_path / "does_not_exist.pdf"
    
    with pytest.raises(DocumentLoadError, match="Archivo no encontrado"):
        await loader.load(missing_file)

@pytest.mark.asyncio
async def test_pdf_loader_handles_empty_page(empty_pdf: Path):
    loader = PyMuPDFDocumentLoader()
    documents = await loader.load(empty_pdf)
    
    assert len(documents) == 1
    assert documents[0].content.strip() == ""
    assert documents[0].source.page == 1
    assert documents[0].source.metadata["total_pages"] == 1
