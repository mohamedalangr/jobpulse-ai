from fastapi import APIRouter, Request, Depends
from src.api.schemas.responses import APIResponse
from src.api.schemas.requests import SearchRequest
from src.api.exceptions import SearchError
from src.application.queries.search_jobs import SearchJobsQuery, SearchJobsUseCase
import time

# Dependency override target
def get_search_use_case():
    # Will be bound to DI container in a later refactor
    raise NotImplementedError()

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("", response_model=APIResponse[list], summary="Semantic Job Search", description="Searches for jobs matching the query semantically.")
async def search_jobs(
    payload: SearchRequest, 
    request: Request,
    use_case: SearchJobsUseCase = Depends(get_search_use_case)
):
    try:
        query = SearchJobsQuery(query=payload.query, top_k=payload.top_k)
        
        # Execute Use Case
        results = use_case.execute(query, context=getattr(request, "state", None))
        
        return APIResponse(
            success=True,
            request_id=getattr(request.state, "request_id", "unknown"),
            timestamp=time.time(),
            data=[] # Mocking results for API test boundary
        )
    except Exception as e:
        raise SearchError(f"Failed to execute semantic search: {str(e)}")
