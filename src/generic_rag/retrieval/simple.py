from generic_rag.core.schemas import RetrievalRequest, RetrievalResponse
from generic_rag.retrieval.base import BaseRetriever
from generic_rag.embeddings.base import BaseEmbeddingProvider
from generic_rag.storage.base import BaseVectorStore

class SimpleRetriever(BaseRetriever):
    def __init__(self, embedding_provider: BaseEmbeddingProvider, vector_store: BaseVectorStore):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        query_emb = await self.embedding_provider.embed_query(request.query)
        
        chunks = await self.vector_store.search(
            query_embedding=query_emb,
            top_k=request.top_k,
            filters=request.filters
        )
        
        if request.score_threshold is not None:
            chunks = [c for c in chunks if c.score >= request.score_threshold]
            
        return RetrievalResponse(
            query=request.query,
            chunks=chunks,
            metadata={"provider": "SimpleRetriever"}
        )
