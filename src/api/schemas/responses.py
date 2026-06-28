from typing import Any, Dict, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    correlation_id: str

class APIResponse(BaseModel, Generic[T]):
    success: bool
    request_id: str
    timestamp: float
    version: str = "0.5.0"
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None

class JobSearchResultDTO(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    url: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    similarity_score: float
