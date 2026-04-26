"""
Ejemplo de uso de CrossEncoderReranker.
Requiere: pip install -e ".[rerankers]"
"""
import asyncio
from generic_rag.core.schemas import ScoredChunk, SourceRef
from generic_rag.reranking.cross_encoder import CrossEncoderReranker

async def main():
    source = SourceRef(source_id="demo", source_type="txt")
    chunks = [
        ScoredChunk(
            id="1", document_id="demo", chunk_index=0, content="Paris is the capital of France", 
            start_char=0, end_char=30, source=source, score=0.9
        ),
        ScoredChunk(
            id="2", document_id="demo", chunk_index=1, content="Berlin is the capital of Germany", 
            start_char=31, end_char=63, source=source, score=0.8
        ),
        ScoredChunk(
            id="3", document_id="demo", chunk_index=2, content="Madrid is the capital of Spain", 
            start_char=64, end_char=94, source=source, score=0.7
        )
    ]
    
    query = "What is the capital of Germany?"
    
    # Este modelo es ligero y bueno para demos
    model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    print(f"Query: {query}")
    print(f"Loading model: {model_name}...")
    
    try:
        reranker = CrossEncoderReranker(model_name=model_name)
        
        print("\nOriginal Retrieval Order:")
        for c in chunks:
            print(f"- [{c.id}] Score: {c.score:.2f} | Content: {c.content}")
            
        reranked = await reranker.rerank(query, chunks)
        
        print(f"\nReranked Order ({model_name}):")
        for c in reranked:
            print(f"- [{c.id}] Rerank Score: {c.score:.2f} | Content: {c.content}")
            
    except Exception as e:
        print(f"\nError: {e}")
        print("Asegúrate de tener instalada la dependencia: pip install \"sentence-transformers>=3.0.0\"")

if __name__ == "__main__":
    asyncio.run(main())
