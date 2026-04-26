from abc import ABC, abstractmethod
from typing import List, Union
from generic_rag.core.schemas import Document, Chunk

class BaseDocumentLoader(ABC):
    @abstractmethod
    async def load(self, source: Union[str, bytes], **kwargs) -> List[Document]:
        pass

class BaseChunker(ABC):
    @abstractmethod
    def split_documents(self, documents: List[Document]) -> List[Chunk]:
        pass
