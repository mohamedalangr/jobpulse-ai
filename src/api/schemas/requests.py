from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class SearchRequest(BaseModel):
    query: str = Field(..., description="The semantic search query")
    top_k: int = Field(10, description="Number of results to return", ge=1, le=100)
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadata filters (future-proof)")
    include_explanations: bool = Field(False, description="Whether to include LLM or rule-based explainability in the results")
