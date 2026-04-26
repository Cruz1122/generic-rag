import math
from typing import List, Optional, Dict, Any
from generic_rag.core.schemas import Chunk, ScoredChunk
from generic_rag.storage.base import BaseVectorStore
from generic_rag.core.exceptions import StorageError

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError("Vectors must have the same length")
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

class InMemoryVectorStore(BaseVectorStore):
    def __init__(self):
        self._chunks: List[Chunk] = []
        self._embeddings: List[List[float]] = []

    async def index_chunks(self, chunks: List[Chunk], embeddings: List[List[float]]) -> None:
        if len(chunks) != len(embeddings):
            raise StorageError("Number of chunks and embeddings must match")
        self._chunks.extend(chunks)
        self._embeddings.extend(embeddings)

    def _matches_filters(self, chunk: Chunk, filters: Optional[Dict[str, Any]]) -> bool:
        if not filters:
            return True
        for k, v in filters.items():
            if chunk.metadata.get(k) != v:
                return False
        return True

    async def search(self, query_embedding: List[float], top_k: int, filters: Optional[Dict[str, Any]] = None) -> List[ScoredChunk]:
        scored_chunks = []
        for chunk, emb in zip(self._chunks, self._embeddings):
            if not self._matches_filters(chunk, filters):
                continue
            score = cosine_similarity(query_embedding, emb)
            scored_chunks.append((score, chunk))
            
        # sort descending by score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, chunk in scored_chunks[:top_k]:
            results.append(ScoredChunk(
                id=chunk.id,
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
                token_count=chunk.token_count,
                source=chunk.source,
                metadata=chunk.metadata,
                score=score
            ))
        return results

    async def delete_chunks(self, document_ids: List[str]) -> None:
        doc_ids_set = set(document_ids)
        new_chunks = []
        new_embeddings = []
        for chunk, emb in zip(self._chunks, self._embeddings):
            if chunk.document_id not in doc_ids_set:
                new_chunks.append(chunk)
                new_embeddings.append(emb)
        self._chunks = new_chunks
        self._embeddings = new_embeddings
