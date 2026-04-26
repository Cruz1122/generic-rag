import pytest
from generic_rag.context.xml import XMLContextBuilder
from generic_rag.core.schemas import ScoredChunk, SourceRef, ContextOptions

def test_xml_context_builder():
    builder = XMLContextBuilder()
    
    source = SourceRef(source_id="s1", source_type="pdf", title="Doc <&> Title", uri="http://test.com", page=5)
    chunk = ScoredChunk(
        id="c1", document_id="d1", chunk_index=0, content="Some <test> content & more", 
        start_char=0, end_char=20, source=source, score=0.85
    )
    
    options = ContextOptions(max_tokens=4000, include_metadata=True, format="xml")
    context_str = builder.build_context([chunk], options)
    
    assert "<context>" in context_str
    assert 'chunk_id="c1"' in context_str
    assert 'score="0.8500"' in context_str
    assert 'title="Doc &lt;&amp;&gt; Title"' in context_str
    assert 'uri="http://test.com"' in context_str
    assert 'page="5"' in context_str
    assert 'Some &lt;test&gt; content &amp; more' in context_str
    assert "</context>" in context_str

def test_xml_context_builder_max_tokens():
    builder = XMLContextBuilder()
    source = SourceRef(source_id="s1", source_type="txt")
    chunk1 = ScoredChunk(id="c1", document_id="d1", chunk_index=0, content="A" * 40, start_char=0, end_char=40, source=source, score=1.0)
    chunk2 = ScoredChunk(id="c2", document_id="d1", chunk_index=1, content="B" * 40, start_char=40, end_char=80, source=source, score=0.9)
    
    # 1 token ~ 4 chars. max_tokens=10 means ~40 chars max for the whole XML. 
    # chunk1 XML alone is ~150 chars. So it should stop after chunk1.
    options = ContextOptions(max_tokens=10, include_metadata=True, format="xml")
    context_str = builder.build_context([chunk1, chunk2], options)
    
    assert "c1" in context_str
    assert "c2" not in context_str
