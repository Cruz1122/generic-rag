import hashlib
import random
from typing import List
from generic_rag.embeddings.base import BaseEmbeddingProvider

class DeterministicEmbeddingProvider(BaseEmbeddingProvider):
    """
    A deterministic embedding provider for testing. 
    It generates random vectors based on the hash of the text.
    """
    def __init__(self, dimensions: int = 1536):
        self.dimensions = dimensions

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [await self.embed_query(t) for t in texts]
        
    async def embed_query(self, text: str) -> List[float]:
        # seed with hash of text to be deterministic
        seed = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)
        r = random.Random(seed)
        return [r.uniform(-1.0, 1.0) for _ in range(self.dimensions)]
