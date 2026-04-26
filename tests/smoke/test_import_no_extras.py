import pytest

def test_core_imports():
    """Verify that core modules can be imported without any optional extras."""
    import generic_rag
    import generic_rag.core.schemas
    import generic_rag.core.exceptions
    import generic_rag.config
    import generic_rag.llm.base
    import generic_rag.storage.base
    import generic_rag.retrieval.base
    import generic_rag.ingestion.base
    import generic_rag.pipelines.qa

def test_default_implementations_imports():
    """Verify that default (non-extra) implementations can be imported."""
    from generic_rag.storage.in_memory import InMemoryVectorStore
    from generic_rag.retrieval.simple import SimpleRetriever
    from generic_rag.ingestion.loaders import TextDocumentLoader, MarkdownDocumentLoader
    from generic_rag.ingestion.chunkers import CharacterChunker
    from generic_rag.embeddings.hash import DeterministicEmbeddingProvider
    from generic_rag.context.xml import XMLContextBuilder
