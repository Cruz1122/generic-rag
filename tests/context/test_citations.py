import pytest
from generic_rag.context.citations import build_citations
from generic_rag.core.schemas import ScoredChunk, SourceRef

def test_build_citations():
    source = SourceRef(source_id="s1", source_type="txt")
    chunk = ScoredChunk(
        id="c1", document_id="d1", chunk_index=0, 
        content="A" * 300, 
        start_char=0, end_char=300, source=source, score=0.99
    )
    
    citations = build_citations([chunk])
    assert len(citations) == 1
    assert citations[0].citation_id == "1"
    assert citations[0].chunk_id == "c1"
    assert citations[0].document_id == "d1"
    assert citations[0].score == 0.99
    assert len(citations[0].snippet) == 203 # 200 + "..."
    assert citations[0].snippet.endswith("...")
