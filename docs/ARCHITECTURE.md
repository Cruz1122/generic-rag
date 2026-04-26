# Architecture of generic-rag

The architecture of `generic-rag` is based on Inversion of Control (IoC) and strict adherence to contracts (Pydantic v2 schemas). The design ensures that RAG orchestration and LLM communication are independent of infrastructure (real Vector DBs) and business logic.

## Pipeline Diagram (v0.2)

```text
[PipelineRequest]
       │
       ▼
 1. [QAPipeline] ───────────► [Retriever]
       │                           │
       │                           ▼
       │                    [VectorStore] ◄─── (Previously indexed Chunks & Embeddings)
       │                           │
       │                           ▼
       │                    [ScoredChunks]
       ▼                           │
 2. [ContextBuilder] ◄─────────────┘
       │
       ▼
  (Generates XML Context String)
       │
       ▼
 3. Assembles new [LLMRequest] (injecting context into messages)
       │
       ▼
 4. [DefaultLLMDispatcher] (Handles Retries & Errors)
       │
       ▼
 5. [LLMProvider] (OpenAI Compatible, Gemini, Ollama) 
       │          (Supports Structured Output / JSON)
       ▼
  [LLMResponse]
       │
       ▼
 6. Assembles [PipelineResponse] (Answer + Retrieved Chunks + Citations)
```

## Core Layers & Responsibilities

### 1. Core Contracts (`generic_rag.core.schemas`)
Absolute source of truth. Defines all Pydantic v2 models for Input/Output. Prevents coupling to loose dictionaries.
- **LLM**: `LLMRequest`, `LLMResponse`, `TokenUsage`.
- **Documents**: `Document`, `Chunk`, `ScoredChunk`, `SourceRef`.
- **RAG**: `RetrievalRequest`, `PipelineRequest`, `PipelineResponse`.

### 2. Hardened LLM Layer (`generic_rag.llm`)
In v0.2, the LLM layer was redesigned to be resilient and predictable:
- **Robust Error Mapping**: Raw HTTP errors (`httpx`) are intercepted and mapped to a contextual hierarchy: `ProviderAuthError`, `ProviderRateLimitError`, `ProviderTimeoutError`, `InvalidResponseError`.
- **Dispatcher with Retries**: `DefaultLLMDispatcher` intercepts transient exceptions (timeouts, 429s, 500s) and executes a retry strategy based on `ProviderConfig.max_retries` and `retry_backoff_seconds`.
- **Structured Output**: Standardized support for requesting JSON (both `json_object` mode and validation via `json_schema`), delegating specific payload transformations to each Provider.
- **Security**: API keys are stored using Pydantic's `SecretStr`, ensuring they are never accidentally exposed in logs or memory dumps.

### 3. Ingestion & Chunking (`generic_rag.ingestion`)
- Converts raw files (currently pure `.txt` and `.md`) into `Document` objects.
- `CharacterChunker` divides text respecting `chunk_size` and `chunk_overlap` limits.

### 4. Vector Storage (`generic_rag.storage`)
- Provides `InMemoryVectorStore`, an implementation using pure Python cosine similarity.
- **Explicit Limit**: This is ideal for offline pipelines and structural testing, but it does not scale for production. Integrations with real databases (Chroma, Qdrant) are planned for future versions (v0.4).

### 5. Embeddings (`generic_rag.embeddings`)
- The default implementation is `DeterministicEmbeddingProvider`, which uses a SHA-256 hash to generate vectors.
- **Explicit Limit**: **It is not semantic**. It serves purely to validate that the chunking, storage, and retrieval system works without requiring heavy downloads (like `sentence-transformers`) or network calls.

### 6. Pipeline Orchestrator (`generic_rag.pipelines`)
The `DefaultQAPipeline` ties all pieces together:
1. Takes the `PipelineRequest`.
2. Requests chunks from the Retriever.
3. Sends chunks to the `XMLContextBuilder` to inject them into a system prompt structurally.
4. Passes the final prompt to the `DefaultLLMDispatcher`.
5. Returns the generated response along with citation metadata.

## Package Boundaries

`generic-rag` **MUST NOT** know about:
- HTTP routes (FastAPI, Flask, etc.).
- UI logic or frontend adapters.
- Business-specific prompts ("You are an algorithm assistant...").
- Domain-specific response structures (e.g., `QuizGenerationResponse`).
- Hardcoded secrets or direct environment variables (these are injected via `ProviderConfig`).
