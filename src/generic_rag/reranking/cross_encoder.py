from typing import List, Optional, Any
from generic_rag.core.schemas import ScoredChunk
from generic_rag.reranking.base import BaseReranker
from generic_rag.core.exceptions import ConfigurationError, InvalidResponseError
from generic_rag.core.optional import require_optional_dependency

class CrossEncoderReranker(BaseReranker):
    """
    Reranker basado en Cross-Encoders (sentence-transformers).
    Requiere la dependencia opcional [rerankers].
    """

    def __init__(self, model_name: str, **model_kwargs: Any) -> None:
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self._model = None

    def _get_model(self) -> Any:
        if self._model is None:
            require_optional_dependency("sentence_transformers", "rerankers", "sentence-transformers")
            from sentence_transformers import CrossEncoder # type: ignore
            self._model = CrossEncoder(self.model_name, **self.model_kwargs)
        return self._model

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

        model = self._get_model()
        
        # Preparar pares (query, content)
        pairs = [(query, chunk.content) for chunk in chunks]
        
        # Ejecutar inferencia (típicamente síncrona en sentence-transformers)
        # Nota: En un entorno de producción real con mucha carga, esto podría 
        # envolverse en un thread pool si bloquea demasiado el event loop.
        scores = model.predict(pairs)
        
        if len(scores) != len(chunks):
            raise InvalidResponseError(
                message=f"Expected {len(chunks)} scores, but got {len(scores)}",
                provider="sentence-transformers"
            )

        results = []
        for i, (chunk, score) in enumerate(zip(chunks, scores)):
            new_metadata = chunk.metadata.copy()
            new_metadata["retrieval_score"] = chunk.score
            new_metadata["rerank_score"] = float(score)
            new_metadata["reranker"] = self.model_name
            
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
                score=float(score)
            )
            results.append(new_chunk)

        # Ordenar por rerank_score desc
        results.sort(key=lambda x: x.score, reverse=True)
        
        if top_n is not None:
            results = results[:top_n]
            
        return results
