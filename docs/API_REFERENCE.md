# API Reference

This is a high-level reference for the core components and schemas of `generic-rag` v0.8.0.
 For deep implementation details, please inspect the `src/generic_rag/` source code.

## Core Schemas (`generic_rag.core.schemas`)

All core data structures inherit from Pydantic `BaseModel` with `extra="forbid"`.

### Documents & Chunks
- **`SourceRef`**: Identifies the origin of a document (`source_id`, `source_type`, `uri`, `metadata`).
- **`Document`**: A full parsed document containing `content` and a `SourceRef`.
- **`Chunk`**: A partitioned piece of a document (`start_char`, `end_char`, `chunk_index`).
- **`ScoredChunk`**: Inherits from `Chunk` and adds a `score: float` (used during retrieval).
- **`Citation`**: Links a generated answer back to a specific `ScoredChunk`.

### LLM Orchestration
- **`ChatMessage`**: Standard role-based message (`role`, `content`, `name`).
- **`LLMRequest`**: Encapsulates parameters for the provider (`model`, `messages`, `temperature`, `max_tokens`, `response_format`, `json_schema`).
- **`LLMResponse`**: The result from the provider (`text`, `usage: TokenUsage`, `provider_info`, `finish_reason`).

### Retrieval & Pipelines
- **`RetrievalRequest`**: Query parameters (`query`, `top_k`, `score_threshold`).
- **`RetrievalResponse`**: Returns a list of `ScoredChunk`.
- **`PipelineRequest`**: The aggregate request combining retrieval and LLM parameters.
- **`PipelineResponse`**: The final output containing the `answer: LLMResponse`, `retrieved_chunks`, and `citations`.

## Configuration (`generic_rag.config`)

- **`ProviderConfig`**: Safely configures an LLM Provider.
  - `name`: string identifier.
  - `api_key`: `Optional[SecretStr]` (prevents leaking secrets in logs).
  - `base_url`: `Optional[str]`.
  - `default_model`: `str`.
  - `timeout_seconds`, `max_retries`, `retry_backoff_seconds`.

## Base Interfaces (`generic_rag.llm.base`, `generic_rag.storage.base`, etc.)

- **`BaseLLMProvider`**: Abstract base class requiring `name` and async `generate(request: LLMRequest)`.
- **`BaseLLMDispatcher`**: Abstract base class for routing requests and managing retries.
- **`BaseVectorStore`**: Abstract base class requiring `index_chunks` and `search`.
- **`BaseRetriever`**: Abstract base class requiring `retrieve`.

## Reranking (`generic_rag.reranking`)

- **`BaseReranker`**: Abstract base class requiring async `rerank(query, chunks, top_n)`.
- **`DeterministicReranker`**: Keyword-overlap based reordering.
- **`CrossEncoderReranker`**: Semantic reranking using `sentence-transformers` (optional via `[rerankers]`).

## Exceptions (`generic_rag.core.exceptions`)

All exceptions inherit from `GenericRagError`. The LLM layer specifically throws:
- `ProviderAuthError` (401/403)
- `ProviderRateLimitError` (429)
- `ProviderTimeoutError` (Timeouts/504)
- `InvalidResponseError` (Malformed JSON, 400/422 client errors)
- `ProviderError` (General 500s or unhandled HTTP errors)

## Default Implementations

- **Providers**: `OpenAICompatibleProvider`, `OllamaProvider`, `GeminiProvider`.
- **Dispatcher**: `DefaultLLMDispatcher` (handles transient retries automatically).
- **Storage**: `InMemoryVectorStore` and `QdrantVectorStore` (via `[qdrant]` extra).
- **Ingestion**: `TextDocumentLoader`, `MarkdownDocumentLoader`, `PyMuPDFDocumentLoader` (via `[pdf]`), `HTMLDocumentLoader` (via `[html]`).
- **Chunking**: `CharacterChunker`.
- **Retrieval**: `SimpleRetriever`.
- **Reranking**: `DeterministicReranker`, `CrossEncoderReranker` (optional).
