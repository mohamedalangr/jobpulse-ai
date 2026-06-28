from fastapi import APIRouter, Request
from src.api.schemas.responses import APIResponse
import time

router = APIRouter(tags=["Intelligence (Mock)"])

@router.post("/career/analyze", response_model=APIResponse[dict])
async def analyze_career(request: Request):
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={
            "readiness_score": 8.7,
            "total_opportunities": 142,
            "missing_skills": ["GraphQL", "Kubernetes"],
            "transition_graph": [
                {"current_role": "Backend Engineer", "next_role": "Senior Backend Engineer", "confidence_score": 0.92},
                {"current_role": "Backend Engineer", "next_role": "Distributed Systems Engineer", "confidence_score": 0.78}
            ]
        }
    )

@router.post("/learning/plan", response_model=APIResponse[dict])
async def learning_plan(request: Request):
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={
            "recommended_skill": "Distributed Systems (Kafka)",
            "projected_salary_increase_pct": 18,
            "unlocked_opportunities": 89,
            "roi_score": 9.4,
            "roadmap": [
                {"step": 1, "skill": "Apache Kafka Fundamentals", "reason": "High demand in remote backend roles."},
                {"step": 2, "skill": "Event-Driven Architecture", "reason": "Crucial for scaling Python microservices."},
                {"step": 3, "skill": "gRPC / Protobufs", "reason": "Standard for high-performance internal communication."}
            ]
        }
    )

@router.get("/market/discovery", response_model=APIResponse[dict])
async def market_discovery(request: Request):
    return APIResponse(
        success=True,
        request_id=getattr(request.state, "request_id", "unknown"),
        timestamp=time.time(),
        data={
            "clusters": [
                {"cluster_id": "C-01 (Data Engineering)", "size": 1250, "median_salary": 145000, "top_skills": ["Python", "SQL", "Spark"]},
                {"cluster_id": "C-02 (AI / ML Ops)", "size": 890, "median_salary": 160000, "top_skills": ["Python", "PyTorch", "Docker"]},
                {"cluster_id": "C-03 (Backend / API)", "size": 3400, "median_salary": 130000, "top_skills": ["Python", "FastAPI", "PostgreSQL"]}
            ]
        }
    )
