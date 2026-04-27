import pytest
from unittest.mock import MagicMock, patch
import sys
from generic_rag.core.schemas import ScoredChunk, SourceRef
from generic_rag.reranking.cross_encoder import CrossEncoderReranker
from generic_rag.core.exceptions import ConfigurationError, InvalidResponseError

@pytest.fixture
def sample_chunks():
    source = SourceRef(source_id="doc1", source_type="txt")
    return [
        ScoredChunk(
            id="c1", document_id="doc1", chunk_index=0, content="Content 1",
            start_char=0, end_char=9, source=source, score=0.9
        ),
        ScoredChunk(
            id="c2", document_id="doc1", chunk_index=1, content="Content 2",
            start_char=10, end_char=19, source=source, score=0.8
        )
    ]

def test_cross_encoder_missing_dependency():
    # Force ImportError/Availability failure
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=False):
        reranker = CrossEncoderReranker(model_name="test-model")
        with pytest.raises(ConfigurationError) as excinfo:
            reranker._get_model()
        assert "Optional dependency 'sentence-transformers' is required" in str(excinfo.value)

@pytest.mark.asyncio
async def test_cross_encoder_rerank_success(sample_chunks):
    mock_model = MagicMock()
    mock_model.predict.return_value = [0.1, 0.9] # c1 -> 0.1, c2 -> 0.9
    
    mock_st = MagicMock()
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=True):
        with patch.dict(sys.modules, {'sentence_transformers': mock_st}):
            mock_st.CrossEncoder.return_value = mock_model
            reranker = CrossEncoderReranker(model_name="test-model")
            results = await reranker.rerank("query", sample_chunks)
            
            assert len(results) == 2
            assert results[0].id == "c2" # Highest score
            assert results[0].score == 0.9
            assert results[0].metadata["retrieval_score"] == 0.8
            assert results[0].metadata["rerank_score"] == 0.9
            assert results[0].metadata["reranker"] == "test-model"
            
            assert results[1].id == "c1"
            assert results[1].score == 0.1

@pytest.mark.asyncio
async def test_cross_encoder_score_mismatch(sample_chunks):
    mock_model = MagicMock()
    mock_model.predict.return_value = [0.5] # Only one score for two chunks
    
    mock_st = MagicMock()
    with patch("generic_rag.core.optional.is_optional_dependency_available", return_value=True):
        with patch.dict(sys.modules, {'sentence_transformers': mock_st}):
            mock_st.CrossEncoder.return_value = mock_model
            reranker = CrossEncoderReranker(model_name="test-model")
            with pytest.raises(InvalidResponseError):
                await reranker.rerank("query", sample_chunks)

@pytest.mark.asyncio
async def test_cross_encoder_empty_chunks():
    reranker = CrossEncoderReranker(model_name="test-model")
    results = await reranker.rerank("query", [])
    assert results == []
