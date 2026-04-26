import pytest

def test_stable_schema_exports():
    """Verify presence of key Stable Public API schemas."""
    from generic_rag.core.schemas import (
        Document,
        Chunk,
        ScoredChunk,
        LLMRequest,
        LLMResponse,
        SourceRef,
        Citation,
        RetrievalRequest,
        RetrievalResponse,
        PipelineRequest,
        PipelineResponse
    )

def test_stable_base_interfaces_exports():
    """Verify presence of key Stable Public API base interfaces."""
    from generic_rag.llm.base import BaseLLMProvider, BaseLLMDispatcher
    from generic_rag.embeddings.base import BaseEmbeddingProvider
    from generic_rag.storage.base import BaseVectorStore
    from generic_rag.retrieval.base import BaseRetriever
    from generic_rag.ingestion.base import BaseDocumentLoader, BaseChunker
    from generic_rag.reranking.base import BaseReranker
    from generic_rag.context.builder import BaseContextBuilder

def test_stable_evaluation_exports():
    """Verify presence of key Stable Public API evaluation components."""
    from generic_rag.evaluation.schemas import (
        EvaluationExample,
        EvaluationDataset,
        RetrievedItem,
        EvaluationReport
    )
    from generic_rag.evaluation.runner import evaluate_retrieval
    from generic_rag.evaluation.io import load_evaluation_dataset, load_predictions
