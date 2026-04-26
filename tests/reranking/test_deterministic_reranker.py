import pytest
from generic_rag.core.schemas import ScoredChunk, SourceRef
from generic_rag.reranking.deterministic import DeterministicReranker
from generic_rag.core.exceptions import ConfigurationError

@pytest.fixture
def sample_chunks():
    source = SourceRef(source_id="doc1", source_type="txt")
    return [
        ScoredChunk(
            id="c1", document_id="doc1", chunk_index=0, content="The cat is on the mat",
            start_char=0, end_char=21, source=source, score=0.9, metadata={"original": "meta"}
        ),
        ScoredChunk(
            id="c2", document_id="doc1", chunk_index=1, content="Dogs like bones",
            start_char=22, end_char=37, source=source, score=0.8
        ),
        ScoredChunk(
            id="c3", document_id="doc1", chunk_index=2, content="The mat is blue",
            start_char=38, end_char=53, source=source, score=0.7
        )
    ]

@pytest.mark.asyncio
async def test_deterministic_reranker_reorders_by_overlap(sample_chunks):
    reranker = DeterministicReranker()
    # Query has "mat", which is in c1 and c3. 
    # c1 has "The", "cat", "is", "on", "the", "mat" -> 2 overlaps ("the" and "mat") if we use set of query terms
    # Actually my implementation counts total occurrences of query terms in chunk content.
    # Query: "blue mat" -> terms {blue, mat}
    # c1: "The cat is on the mat" -> "mat" (1)
    # c2: "Dogs like bones" -> 0
    # c3: "The mat is blue" -> "mat", "blue" (2)
    
    results = await reranker.rerank("blue mat", sample_chunks)
    
    assert len(results) == 3
    assert results[0].id == "c3"  # 2 overlaps
    assert results[1].id == "c1"  # 1 overlap
    assert results[2].id == "c2"  # 0 overlaps
    
    # Verify metadata preservation
    assert results[1].metadata["original"] == "meta"
    assert results[1].metadata["retrieval_score"] == 0.9
    assert results[1].metadata["reranker"] == "deterministic"
    assert results[1].score == 1.0

@pytest.mark.asyncio
async def test_deterministic_reranker_top_n(sample_chunks):
    reranker = DeterministicReranker()
    results = await reranker.rerank("blue mat", sample_chunks, top_n=2)
    assert len(results) == 2
    assert results[0].id == "c3"
    assert results[1].id == "c1"

@pytest.mark.asyncio
async def test_deterministic_reranker_empty_chunks():
    reranker = DeterministicReranker()
    results = await reranker.rerank("query", [])
    assert results == []

@pytest.mark.asyncio
async def test_deterministic_reranker_invalid_top_n(sample_chunks):
    reranker = DeterministicReranker()
    with pytest.raises(ConfigurationError):
        await reranker.rerank("query", sample_chunks, top_n=0)

@pytest.mark.asyncio
async def test_deterministic_reranker_stable_tie_break(sample_chunks):
    reranker = DeterministicReranker()
    # Both c1 and c3 have "mat"
    results = await reranker.rerank("mat", sample_chunks)
    # Query "mat" -> terms {mat}
    # c1: "The cat is on the mat" -> 1
    # c2: 0
    # c3: "The mat is blue" -> 1
    # Tie between c1 and c3. Original order was c1 then c3.
    assert results[0].id == "c1"
    assert results[1].id == "c3"
    assert results[2].id == "c2"
