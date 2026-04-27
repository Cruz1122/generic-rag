import pytest
from unittest.mock import patch
from generic_rag.core.exceptions import ConfigurationError

def test_pdf_loader_guard():
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=False):
        from generic_rag.ingestion.pdf import PyMuPDFDocumentLoader
        with pytest.raises(ConfigurationError) as excinfo:
            PyMuPDFDocumentLoader()
        assert "pip install \"generic-rag[pdf]\"" in str(excinfo.value)

def test_html_loader_guard():
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=False):
        from generic_rag.ingestion.html import HTMLDocumentLoader
        with pytest.raises(ConfigurationError) as excinfo:
            HTMLDocumentLoader()
        assert "pip install \"generic-rag[html]\"" in str(excinfo.value)

def test_qdrant_vector_store_guard():
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=False):
        from generic_rag.storage.qdrant import QdrantVectorStore
        with pytest.raises(ConfigurationError) as excinfo:
            # client can be None since the guard should trigger first
            QdrantVectorStore(client=None, collection_name="test", vector_size=128) # type: ignore
        assert "pip install \"generic-rag[qdrant]\"" in str(excinfo.value)

def test_cross_encoder_reranker_guard():
    from generic_rag.core.schemas import ScoredChunk, SourceRef
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=False):
        from generic_rag.reranking.cross_encoder import CrossEncoderReranker
        reranker = CrossEncoderReranker(model_name="test")
        with pytest.raises(ConfigurationError) as excinfo:
            # The guard is in _get_model which is called by rerank
            import asyncio
            dummy_chunk = ScoredChunk(
                id="1", document_id="1", chunk_index=0, content="test", 
                start_char=0, end_char=4, score=1.0, 
                source=SourceRef(source_id="1", source_type="other", uri="test")
            )
            asyncio.run(reranker.rerank("query", [dummy_chunk]))
        assert "pip install \"generic-rag[rerankers]\"" in str(excinfo.value)
