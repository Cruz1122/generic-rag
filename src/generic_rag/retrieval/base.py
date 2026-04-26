from abc import ABC, abstractmethod
from typing import List
from generic_rag.core.schemas import RetrievalRequest, RetrievalResponse, ScoredChunk

class BaseRetriever(ABC):
    """
    Estrategia de búsqueda. Usa internamente un BaseVectorStore y/o BM25, 
    gestiona la generación del embed de la query y orquesta la respuesta.
    """
    @abstractmethod
    async def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        pass

class BaseReranker(ABC):
    @abstractmethod
    async def rerank(self, query: str, chunks: List[ScoredChunk], top_n: int) -> List[ScoredChunk]:
        pass
