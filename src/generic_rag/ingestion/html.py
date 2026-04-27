import uuid
import pathlib
from typing import List, Union, Any

from generic_rag.core.schemas import Document, SourceRef
from generic_rag.core.exceptions import DocumentLoadError
from generic_rag.ingestion.base import BaseDocumentLoader
from generic_rag.core.optional import require_optional_dependency

class HTMLDocumentLoader(BaseDocumentLoader):
    """Cargador de documentos HTML usando BeautifulSoup."""

    def __init__(self) -> None:
        require_optional_dependency("bs4", "html", "beautifulsoup4")

    async def load(self, source: Union[str, pathlib.Path, bytes], encoding: str = "utf-8", **kwargs: Any) -> List[Document]:
        """Carga un documento HTML desde un path local, string o bytes."""
        from bs4 import BeautifulSoup # type: ignore
        
        if isinstance(source, pathlib.Path):
            source = str(source)

        html_content = ""
        uri = "memory"

        try:
            if isinstance(source, bytes):
                html_content = source.decode(encoding)
            elif isinstance(source, str) and (source.strip().startswith("<") or "\n" in source):
                # Es probable que sea el contenido HTML directamente
                html_content = source
            elif isinstance(source, str):
                path = pathlib.Path(source)
                if not path.exists():
                    raise DocumentLoadError(f"Archivo no encontrado: {source}")
                with open(path, "r", encoding=encoding) as f:
                    html_content = f.read()
                uri = str(source)
        except DocumentLoadError:
            raise
        except Exception as e:
            raise DocumentLoadError(f"Error al leer la fuente HTML: {str(e)}") from e

        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            title = None
            if soup.title and soup.title.string:
                title = soup.title.string.strip()

            tags_to_remove = ["script", "style", "nav", "footer", "aside", "header", "noscript"]
            for tag in soup(tags_to_remove):
                tag.extract()

            text = soup.get_text(separator="\n\n", strip=True)

            source_ref = SourceRef(
                source_id=str(uuid.uuid4()),
                source_type="html",
                title=title,
                uri=uri,
                metadata={
                    "extraction_method": "beautifulsoup",
                    "removed_tags": tags_to_remove
                }
            )

            doc = Document(
                id=str(uuid.uuid4()),
                content=text or "",
                source=source_ref
            )

            return [doc]
        except Exception as e:
            raise DocumentLoadError(f"Error al procesar el HTML: {str(e)}") from e
