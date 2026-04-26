from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

# --- Ingestion & Documents ---

class SourceRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str
    source_type: Literal["pdf", "markdown", "txt", "json", "web", "html", "other"]
    title: Optional[str] = None
    uri: Optional[str] = Field(default=None, description="URL o path al archivo")
    page: Optional[int] = None
    section: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Document(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    content: str
    source: SourceRef
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Chunk(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    document_id: str
    chunk_index: int
    content: str
    start_char: int
    end_char: int
    token_count: Optional[int] = None
    source: SourceRef
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ScoredChunk(Chunk):
    model_config = ConfigDict(extra="forbid")
    score: float

class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    citation_id: str
    chunk_id: str
    document_id: str
    source: SourceRef
    snippet: str
    score: Optional[float] = None

# --- LLM & Chat ---

class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str] = None

class LLMRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: Optional[str] = None
    model: str
    messages: List[ChatMessage] = Field(..., min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, gt=0)
    timeout_seconds: int = Field(default=30, gt=0)
    response_format: Literal["text", "json_object"] = "text"
    json_schema: Optional[Dict[str, Any]] = None
    stream: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TokenUsage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class ProviderInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    model: str
    latency_ms: Optional[int] = None

class LLMResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    structured: Optional[Dict[str, Any]] = None
    usage: TokenUsage = Field(default_factory=TokenUsage)
    provider_info: ProviderInfo
    finish_reason: Optional[str] = None

# --- Retrieval & Pipeline ---

class RetrievalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str
    top_k: int = Field(default=5, gt=0)
    filters: Optional[Dict[str, Any]] = None
    score_threshold: Optional[float] = None
    use_dense: bool = True
    use_sparse: bool = False

class RetrievalResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str
    chunks: List[ScoredChunk]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ContextOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_tokens: int = 4000
    include_metadata: bool = True
    format: Literal["xml", "markdown", "json"] = "xml"

class PipelineRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str
    retrieval: RetrievalRequest
    llm: LLMRequest
    context_options: ContextOptions = Field(default_factory=ContextOptions)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class PipelineResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: LLMResponse
    retrieved_chunks: List[ScoredChunk]
    citations: List[Citation]
