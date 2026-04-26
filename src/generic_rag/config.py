from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, SecretStr, Field

class ProviderConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    api_key: Optional[SecretStr] = None
    base_url: Optional[str] = None
    default_model: str
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_backoff_seconds: float = 2.0
    extra_headers: Dict[str, str] = Field(default_factory=dict)
    extra_params: Dict[str, Any] = Field(default_factory=dict)

class EmbeddingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: str
    model: str
    dimensions: int
    batch_size: int = 32

class RetrievalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    default_top_k: int = 5
    score_threshold: float = 0.0

class PipelineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    default_context_tokens: int = 4000
    providers: Dict[str, ProviderConfig]
    embeddings: EmbeddingConfig
    retrieval: RetrievalConfig
