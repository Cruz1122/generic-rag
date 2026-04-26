import uuid
from typing import List
from generic_rag.core.schemas import Document, Chunk
from generic_rag.ingestion.base import BaseChunker
from generic_rag.core.exceptions import ConfigurationError

class CharacterChunker(BaseChunker):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_overlap >= chunk_size:
            raise ConfigurationError("chunk_overlap must be less than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents: List[Document]) -> List[Chunk]:
        chunks = []
        for doc in documents:
            text = doc.content
            start = 0
            chunk_index = 0
            
            if not text:
                continue

            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                
                chunk_text = text[start:end]
                
                chunk = Chunk(
                    id=str(uuid.uuid4()),
                    document_id=doc.id,
                    chunk_index=chunk_index,
                    content=chunk_text,
                    start_char=start,
                    end_char=end,
                    source=doc.source,
                    metadata=doc.metadata.copy()
                )
                chunks.append(chunk)
                chunk_index += 1
                
                if end >= len(text):
                    break
                    
                start = end - self.chunk_overlap
                
        return chunks
