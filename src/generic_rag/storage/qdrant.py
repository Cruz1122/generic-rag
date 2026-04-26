import uuid
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

try:
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.http import models
except ImportError:
    # Estas dependencias son opcionales
    AsyncQdrantClient = Any  # type: ignore
    models = Any  # type: ignore

from generic_rag.core.schemas import Chunk, ScoredChunk, SourceRef
from generic_rag.storage.base import BaseVectorStore
from generic_rag.core.exceptions import StorageError, ConfigurationError, InvalidResponseError

# Namespace interno determinístico para generic-rag
QDRANT_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "https://generic-rag.local/qdrant")

class QdrantVectorStore(BaseVectorStore):
    """
    Vector Store basado en Qdrant con soporte asíncrono.
    Requiere: pip install generic-rag[qdrant]
    """

    def __init__(
        self,
        client: "AsyncQdrantClient",
        collection_name: str,
        vector_size: int,
        distance: str = "Cosine",
    ) -> None:
        if not collection_name:
            raise ConfigurationError("collection_name cannot be empty")
        if vector_size <= 0:
            raise ConfigurationError("vector_size must be greater than 0")

        self.client = client
        self.collection_name = collection_name
        self.vector_size = vector_size
        
        # Mapeo de distancias
        # Solo intentamos acceder a models si no es Any
        if models is Any:
            raise ImportError("qdrant-client is not installed. Install it with pip install generic-rag[qdrant]")

        distance_map = {
            "Cosine": models.Distance.COSINE,
            "Dot": models.Distance.DOT,
            "Euclid": models.Distance.EUCLID,
        }
        if distance not in distance_map:
            raise ConfigurationError(f"Unsupported distance: {distance}. Supported: {list(distance_map.keys())}")
        
        self.distance = distance_map[distance]

    async def ensure_collection(self, recreate: bool = False) -> None:
        """
        Asegura que la colección existe. 
        Si recreate=True, la borra y la vuelve a crear (operación destructiva).
        """
        try:
            exists = await self.client.collection_exists(self.collection_name)
            
            if exists and recreate:
                await self.client.delete_collection(self.collection_name)
                exists = False
            
            if not exists:
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=self.distance
                    )
                )
        except Exception as e:
            if isinstance(e, (ConfigurationError, StorageError)):
                raise
            raise StorageError(f"Failed to ensure collection '{self.collection_name}': {self._sanitize_error_message(e)}")

    def _qdrant_point_id(self, chunk_id: str) -> str:
        """Genera un UUIDv5 determinístico estable a partir del chunk_id."""
        return str(uuid.uuid5(QDRANT_NAMESPACE, chunk_id))

    def _payload_from_chunk(self, chunk: Chunk) -> Dict[str, Any]:
        """Prepara el payload para Qdrant incluyendo el contenido completo."""
        return {
            "chunk_id": chunk.id,
            "document_id": chunk.document_id,
            "chunk_index": chunk.chunk_index,
            "content": chunk.content,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "token_count": chunk.token_count,
            "metadata": chunk.metadata,
            "source": chunk.source.model_dump(),
            "_rag_schema": "v1",
        }

    async def index_chunks(self, chunks: List[Chunk], embeddings: List[List[float]]) -> None:
        """Indexa chunks y sus embeddings en Qdrant."""
        if not chunks:
            if embeddings:
                raise ConfigurationError("Embeddings provided without chunks")
            return

        if len(chunks) != len(embeddings):
            raise ConfigurationError(f"Mismatch: {len(chunks)} chunks and {len(embeddings)} embeddings")

        points = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            if len(emb) != self.vector_size:
                raise ConfigurationError(
                    f"Embedding at index {i} has size {len(emb)}, expected {self.vector_size}"
                )
            
            points.append(models.PointStruct(
                id=self._qdrant_point_id(chunk.id),
                vector=emb,
                payload=self._payload_from_chunk(chunk)
            ))

        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        except Exception as e:
            if isinstance(e, (ConfigurationError, StorageError)):
                raise
            raise StorageError(f"Failed to index chunks: {self._sanitize_error_message(e)}")

    def _qdrant_filter_from_dict(self, filters: Optional[Dict[str, Any]]) -> Any:
        """Mapea filtros simples (exact match) a modelos de Qdrant."""
        if not filters:
            return None
        
        must_conditions = []
        for key, value in filters.items():
            if isinstance(value, (dict, list, tuple, set)):
                raise ConfigurationError(f"Unsupported complex filter value for key '{key}': {type(value)}")
            
            must_conditions.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
            )
        
        return models.Filter(must=must_conditions) if must_conditions else None

    async def search(
        self,
        query_embedding: List[float],
        top_k: int,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[ScoredChunk]:
        """Busca chunks por similitud vectorial."""
        if top_k <= 0:
            raise ConfigurationError("top_k must be greater than 0")
        if len(query_embedding) != self.vector_size:
            raise ConfigurationError(f"Query embedding size {len(query_embedding)} mismatch with {self.vector_size}")

        try:
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=self._qdrant_filter_from_dict(filters),
                with_payload=True
            )
            
            return [self._scored_chunk_from_point(res) for res in results]
        except Exception as e:
            if isinstance(e, (InvalidResponseError, ConfigurationError, StorageError)):
                raise
            raise StorageError(f"Search failed: {self._sanitize_error_message(e)}")

    def _scored_chunk_from_point(self, point: Any) -> ScoredChunk:
        """Reconstruye un ScoredChunk a partir de un resultado de Qdrant."""
        payload = point.payload
        if not payload:
            raise InvalidResponseError("Point result is missing payload")
        
        required_keys = ["chunk_id", "document_id", "chunk_index", "content", "start_char", "end_char", "source"]
        missing = [k for k in required_keys if k not in payload]
        if missing:
            raise InvalidResponseError(f"Payload missing required keys: {missing}")
        
        try:
            return ScoredChunk(
                id=payload["chunk_id"],
                document_id=payload["document_id"],
                chunk_index=payload["chunk_index"],
                content=payload["content"],
                start_char=payload["start_char"],
                end_char=payload["end_char"],
                token_count=payload.get("token_count"),
                source=SourceRef(**payload["source"]),
                metadata=payload.get("metadata", {}),
                score=point.score
            )
        except Exception as e:
            raise InvalidResponseError(f"Failed to reconstruct ScoredChunk from payload: {str(e)}")

    async def delete_chunks(self, document_ids: List[str]) -> None:
        """Borra todos los chunks asociados a los document_ids proporcionados."""
        if not document_ids:
            return

        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="document_id",
                                match=models.MatchAny(any=document_ids)
                            )
                        ]
                    )
                )
            )
        except Exception as e:
            if isinstance(e, (ConfigurationError, StorageError)):
                raise
            raise StorageError(f"Failed to delete chunks: {self._sanitize_error_message(e)}")

    def _sanitize_error_message(self, error: Exception) -> str:
        """Limpia mensajes de error para no exponer información sensible."""
        msg = str(error)
        # Sanitización básica: truncar si es muy largo y evitar patrones típicos de tokens/keys
        if len(msg) > 500:
            msg = msg[:500] + "..."
        return msg
