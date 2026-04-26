import asyncio
from generic_rag.core.schemas import ScoredChunk, SourceRef
from generic_rag.reranking.deterministic import DeterministicReranker

async def main():
    source = SourceRef(source_id="demo", source_type="txt")
    chunks = [
        ScoredChunk(
            id="1", document_id="demo", chunk_index=0, content="The sky is blue", 
            start_char=0, end_char=15, source=source, score=0.9
        ),
        ScoredChunk(
            id="2", document_id="demo", chunk_index=1, content="The grass is green", 
            start_char=16, end_char=34, source=source, score=0.8
        ),
        ScoredChunk(
            id="3", document_id="demo", chunk_index=2, content="The sun is yellow", 
            start_char=35, end_char=52, source=source, score=0.7
        )
    ]
    
    query = "green grass"
    reranker = DeterministicReranker()
    
    print(f"Query: {query}")
    print("\nOriginal Retrieval Order:")
    for c in chunks:
        print(f"- [{c.id}] Score: {c.score:.2f} | Content: {c.content}")
        
    reranked = await reranker.rerank(query, chunks)
    
    print("\nReranked Order (Deterministic):")
    for c in reranked:
        print(f"- [{c.id}] Rerank Score: {c.score:.2f} | Content: {c.content}")
        print(f"  Metadata: {c.metadata}")

if __name__ == "__main__":
    asyncio.run(main())
