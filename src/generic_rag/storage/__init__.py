from generic_rag.storage.base import BaseVectorStore, BaseDocumentStore
from generic_rag.storage.in_memory import InMemoryVectorStore

__all__ = [
    "BaseVectorStore",
    "BaseDocumentStore",
    "InMemoryVectorStore",
    "QdrantVectorStore",
]

try:
    from generic_rag.storage.qdrant import QdrantVectorStore
except ImportError:
    # QdrantVectorStore is optional and requires qdrant-client
    pass
