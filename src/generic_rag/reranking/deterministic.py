import re
from typing import List, Optional
from generic_rag.core.schemas import ScoredChunk
from generic_rag.reranking.base import BaseReranker
from generic_rag.core.exceptions import ConfigurationError

class DeterministicReranker(BaseReranker):
    """
    Reranker determinístico basado en keyword overlap.
    Ideal para tests y demos sin dependencias de modelos.
    """

    async def rerank(
        self,
        query: str,
        chunks: List[ScoredChunk],
        top_n: Optional[int] = None,
    ) -> List[ScoredChunk]:
        if not chunks:
            return []

        if top_n is not None and top_n <= 0:
            raise ConfigurationError(f"top_n must be greater than 0, got {top_n}")

        # Tokenización simple
        query_terms = set(re.findall(r"\w+", query.lower()))
        
        results = []
        for i, chunk in enumerate(chunks):
            chunk_content_terms = re.findall(r"\w+", chunk.content.lower())
            
            # Calcular overlap (cuenta total de ocurrencias de términos de la query)
            overlap_count = 0
            for term in chunk_content_terms:
                if term in query_terms:
                    overlap_count += 1
            
            # Crear nuevo ScoredChunk para no mutar el original
            # Preserva SourceRef y metadata
            new_metadata = chunk.metadata.copy()
            new_metadata["retrieval_score"] = chunk.score
            new_metadata["rerank_score"] = float(overlap_count)
            new_metadata["reranker"] = "deterministic"
            
            new_chunk = ScoredChunk(
                id=chunk.id,
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                start_char=chunk.start_char,
                end_char=chunk.end_char,
                token_count=chunk.token_count,
                source=chunk.source,
                metadata=new_metadata,
                score=float(overlap_count)
            )
            # Guardamos el índice original para desempate estable
            results.append((new_chunk, i))

        # Ordenar por rerank_score desc, luego por índice original asc (tie-break)
        results.sort(key=lambda x: (-x[0].score, x[1]))
        
        ordered_chunks = [r[0] for r in results]
        
        if top_n is not None:
            ordered_chunks = ordered_chunks[:top_n]
            
        return ordered_chunks
