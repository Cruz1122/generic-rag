import pytest
from generic_rag.core.schemas import Document, SourceRef
from generic_rag.ingestion.chunkers import CharacterChunker
from generic_rag.core.exceptions import ConfigurationError
import uuid

def create_doc(content: str) -> Document:
    return Document(
        id=str(uuid.uuid4()),
        content=content,
        source=SourceRef(source_id="1", source_type="txt"),
        metadata={"author": "test"}
    )

def test_character_chunker_basic():
    chunker = CharacterChunker(chunk_size=10, chunk_overlap=2)
    doc = create_doc("1234567890abcdefghij") # length 20
    # chunk 1: 0 to 10 "1234567890"
    # start next: 10 - 2 = 8
    # chunk 2: 8 to 18 "90abcdefgh"
    # start next: 18 - 2 = 16
    # chunk 3: 16 to 20 "ghij"
    
    chunks = chunker.split_documents([doc])
    assert len(chunks) == 3
    assert chunks[0].content == "1234567890"
    assert chunks[0].start_char == 0
    assert chunks[0].end_char == 10
    
    assert chunks[1].content == "90abcdefgh"
    assert chunks[1].start_char == 8
    assert chunks[1].end_char == 18
    
    assert chunks[2].content == "ghij"
    assert chunks[2].start_char == 16
    assert chunks[2].end_char == 20

    assert chunks[0].metadata == {"author": "test"}

def test_character_chunker_validation():
    with pytest.raises(ConfigurationError):
        CharacterChunker(chunk_size=10, chunk_overlap=10)
