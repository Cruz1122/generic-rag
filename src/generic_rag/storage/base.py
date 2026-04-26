from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from generic_rag.core.schemas import Document, Chunk, ScoredChunk

class BaseDocumentStore(ABC):
    """Almacén crudo de documentos completos (ej. MongoDB, S3)."""
    @abstractmethod
    async def save_documents(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    async def get_document(self, document_id: str) -> Optional[Document]:
        pass

    @abstractmethod
    async def delete_documents(self, document_ids: List[str]) -> None:
        pass

class BaseVectorStore(ABC):
    """Almacén de vectores (ej. Chroma, FAISS, Qdrant)."""
    @abstractmethod
    async def index_chunks(self, chunks: List[Chunk], embeddings: List[List[float]]) -> None:
        pass
        
    @abstractmethod
    async def search(self, query_embedding: List[float], top_k: int, filters: Optional[Dict[str, Any]] = None) -> List[ScoredChunk]:
        pass

    @abstractmethod
    async def delete_chunks(self, document_ids: List[str]) -> None:
        pass
