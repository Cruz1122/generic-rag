from typing import List
from generic_rag.core.schemas import ScoredChunk, Citation

def build_citations(chunks: List[ScoredChunk]) -> List[Citation]:
    citations = []
    for i, chunk in enumerate(chunks):
        citations.append(Citation(
            citation_id=str(i + 1),
            chunk_id=chunk.id,
            document_id=chunk.document_id,
            source=chunk.source,
            snippet=chunk.content[:200] + ("..." if len(chunk.content) > 200 else ""),
            score=chunk.score
        ))
    return citations
