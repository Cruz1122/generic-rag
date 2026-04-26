from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

class EvaluationExample(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    id: str = Field(min_length=1)
    query: str = Field(min_length=1)
    relevant_chunk_ids: List[str]
    graded_relevance: Optional[Dict[str, float]] = None
    expected_citation_ids: Optional[List[str]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EvaluationDataset(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(min_length=1)
    examples: List[EvaluationExample]

class RetrievedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    chunk_id: str = Field(min_length=1)
    score: float

class MetricResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    value: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RetrievalEvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    query_id: str = Field(min_length=1)
    metrics: Dict[str, MetricResult]

class EvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    dataset_name: str = Field(min_length=1)
    aggregate_metrics: Dict[str, float]
    per_query_results: List[RetrievalEvaluationResult]
