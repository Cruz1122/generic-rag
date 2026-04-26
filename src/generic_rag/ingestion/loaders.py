import uuid
from typing import List, Union
from pathlib import Path
from generic_rag.core.schemas import Document, SourceRef
from generic_rag.ingestion.base import BaseDocumentLoader

class TextDocumentLoader(BaseDocumentLoader):
    async def load(self, source: Union[str, bytes], **kwargs) -> List[Document]:
        if isinstance(source, bytes):
            content = source.decode("utf-8")
            uri = None
        else:
            path = Path(source)
            if path.exists() and path.is_file():
                content = path.read_text(encoding="utf-8")
                uri = str(path)
            else:
                content = source
                uri = None

        source_ref = SourceRef(
            source_id=str(uuid.uuid4()),
            source_type="txt",
            uri=uri,
            metadata=kwargs
        )
        doc = Document(
            id=str(uuid.uuid4()),
            content=content,
            source=source_ref,
            metadata=kwargs
        )
        return [doc]

class MarkdownDocumentLoader(BaseDocumentLoader):
    async def load(self, source: Union[str, bytes], **kwargs) -> List[Document]:
        if isinstance(source, bytes):
            content = source.decode("utf-8")
            uri = None
        else:
            path = Path(source)
            if path.exists() and path.is_file():
                content = path.read_text(encoding="utf-8")
                uri = str(path)
            else:
                content = source
                uri = None

        source_ref = SourceRef(
            source_id=str(uuid.uuid4()),
            source_type="markdown",
            uri=uri,
            metadata=kwargs
        )
        doc = Document(
            id=str(uuid.uuid4()),
            content=content,
            source=source_ref,
            metadata=kwargs
        )
        return [doc]
