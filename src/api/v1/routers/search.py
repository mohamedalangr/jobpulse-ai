from fastapi import APIRouter, Request, Depends
from src.api.schemas.responses import APIResponse, JobSearchResultDTO
from src.api.schemas.requests import SearchRequest
from src.api.exceptions import SearchError
from src.application.queries.search_jobs import SearchJobsQuery, SearchJobsUseCase
import time

from src.application.providers.embedding import get_embedding_provider
from src.intelligence.vectorstore.pgvector_store import PgVectorStore
from src.intelligence.semantic_search.service import SemanticSearchService
from src.database.session import SessionLocal
from src.database.models.job import Job
from src.domain.entities.job_posting import JobPosting
from src.domain.entities.metadata import RecordMetadata

class DBJobFetcher:
    def get_by_fingerprint(self, fingerprint: str) -> JobPosting | None:
        with SessionLocal() as session:
            record = session.query(Job).filter(Job.fingerprint == fingerprint).first()
            if not record:
                return None
            return JobPosting(
                id=str(record.id),
                title=record.title,
                company=record.company,
                description=record.description,
                url=record.url,
                raw_data=record.raw_data,
                location=record.location,
                country=record.country,
                employment_type=record.employment_type,
                experience_level=record.experience_level,
                salary_min=record.salary_min,
                salary_max=record.salary_max,
                currency=record.currency,
                skills=record.skills or [],
                metadata=RecordMetadata(
                    source=record.meta_source,
                    pipeline_version=record.meta_pipeline_version,
                    first_seen_at=record.meta_first_seen_at,
                    last_seen_at=record.meta_last_seen_at,
                    fingerprint=record.fingerprint
                )
            )

# Dependency override target
def get_search_use_case(request: Request):
    provider = get_embedding_provider(request.app.state.model_registry)
    store = PgVectorStore()
    fetcher = DBJobFetcher()
    matcher = SemanticSearchService(provider=provider, store=store, fetcher=fetcher)
    return SearchJobsUseCase(semantic_matcher=matcher)

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
        
        # Map results to DTOs
        mapped_data = []
        for job, score in results:
            mapped_data.append(
                JobSearchResultDTO(
                    id=job.id,
                    title=job.title,
                    company=job.company,
                    location=job.location,
                    url=job.url,
                    salary_min=job.salary_min,
                    salary_max=job.salary_max,
                    currency=job.currency,
                    similarity_score=score
                )
            )
            
        return APIResponse(
            success=True,
            request_id=getattr(request.state, "request_id", "unknown"),
            timestamp=time.time(),
            data=mapped_data
        )
    except Exception as e:
        raise SearchError(f"Failed to execute semantic search: {str(e)}")
