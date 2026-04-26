from abc import ABC, abstractmethod
from typing import List, Optional
from generic_rag.core.schemas import ScoredChunk

class BaseReranker(ABC):
    """
    Contrato base para reordenar chunks recuperados por un retriever.
    """
    @abstractmethod
    async def rerank(
        self,
        query: str,
        chunks: List[ScoredChunk],
        top_n: Optional[int] = None,
    ) -> List[ScoredChunk]:
        """
        Reevalúa y reordena una lista de chunks dados según la query.

        Args:
            query: La consulta del usuario.
            chunks: Lista de ScoredChunks obtenidos del retriever.
            top_n: (Opcional) Número máximo de chunks a retornar tras el reordenamiento.

        Returns:
            Lista de ScoredChunks reordenados.
        """
        pass
