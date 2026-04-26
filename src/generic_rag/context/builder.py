from abc import ABC, abstractmethod
from typing import List
from generic_rag.core.schemas import ScoredChunk, ContextOptions

class BaseContextBuilder(ABC):
    @abstractmethod
    def build_context(self, chunks: List[ScoredChunk], options: ContextOptions) -> str:
        """Serializa los chunks respetando el formato (xml, json) y el límite de tokens."""
        pass
