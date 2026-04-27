import uuid
import pathlib
from typing import List, Union, Any

from generic_rag.core.schemas import Document, SourceRef
from generic_rag.core.exceptions import DocumentLoadError
from generic_rag.ingestion.base import BaseDocumentLoader
from generic_rag.core.optional import require_optional_dependency

class PyMuPDFDocumentLoader(BaseDocumentLoader):
    """Cargador de documentos PDF usando PyMuPDF (fitz)."""

    def __init__(self) -> None:
        require_optional_dependency("fitz", "pdf", "PyMuPDF")

    async def load(self, source: Union[str, pathlib.Path, bytes], **kwargs: Any) -> List[Document]:
        """Carga un documento PDF desde un path local o bytestream."""
        import fitz # type: ignore
        
        if isinstance(source, pathlib.Path):
            source = str(source)

        try:
            if isinstance(source, bytes):
                doc = fitz.Document(stream=source, filetype="pdf")
                uri = "memory"
            else:
                doc = fitz.Document(filename=source)
                uri = str(source)
        except Exception as e:
            if not isinstance(source, bytes):
                path = pathlib.Path(source)
                if not path.exists():
                    raise DocumentLoadError(f"Archivo no encontrado: {source}") from e
            raise DocumentLoadError(f"Error al cargar PDF: {str(e)}") from e

        try:
            total_pages = doc.page_count
            pdf_metadata = doc.metadata or {}
            title = pdf_metadata.get("title")

            documents = []
            for i in range(total_pages):
                page = doc[i]
                page_number = i + 1
                
                try:
                    text = page.get_text("text", sort=True)
                except Exception:
                    text = page.get_text()

                source_ref = SourceRef(
                    source_id=str(uuid.uuid4()),
                    source_type="pdf",
                    title=title,
                    uri=uri,
                    page=page_number,
                    metadata={
                        "total_pages": total_pages,
                        "extraction_method": "pymupdf",
                        "pdf_metadata": pdf_metadata
                    }
                )

                documents.append(
                    Document(
                        id=str(uuid.uuid4()),
                        content=text or "",
                        source=source_ref
                    )
                )

            return documents
        except Exception as e:
            raise DocumentLoadError(f"Error al procesar el PDF: {str(e)}") from e
        finally:
            doc.close()
