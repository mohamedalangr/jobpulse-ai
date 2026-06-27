from typing import List, Tuple
from src.domain.entities.job_posting import JobPosting
from src.intelligence.career.profiles.candidate import CandidateProfile, MarketScore
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.skills.extractor import SkillExtractor

class ExplainabilityEngine:
    def __init__(self, extractor: SkillExtractor):
        self.extractor = extractor

    def explain(self, candidate: CandidateProfile, matches: List[Tuple[JobPosting, float]]) -> List[JobRecommendation]:
        recommendations = []
        candidate_skills = set([s.lower() for s in candidate.skills])
        
        for job, similarity in matches:
            # 1. Extract skills from Job
            job_occurrences = self.extractor.extract_all(job)
            job_skills = set([occ.skill for occ in job_occurrences])
            
            # 2. Transferable / Missing
            transferable = list(candidate_skills.intersection(job_skills))
            missing = list(job_skills.difference(candidate_skills))
            
            # 3. Emerging Skills (Heuristic Proxy)
            emerging = missing[:2] if missing else []
            
            # 4. Market Demand (Heuristic Proxy)
            demand_score = "High" if len(job_skills) > 5 else ("Medium" if len(job_skills) > 2 else "Low")
            
            # 5. Salary Delta
            salary_delta = None
            if candidate.salary_expectation and job.salary_max:
                try:
                    delta = float(job.salary_max) - candidate.salary_expectation
                    salary_delta = round((delta / candidate.salary_expectation) * 100, 1)
                except:
                    pass
                    
            # 6. Confidence
            penalty = len(missing) * 0.05
            confidence = max(0.0, similarity - penalty)
            
            rec = JobRecommendation(
                job=job,
                similarity_score=round(similarity, 3),
                transferable_skills=transferable,
                missing_skills=missing,
                emerging_skills=emerging,
                market_demand_score=demand_score,
                salary_delta_pct=salary_delta,
                confidence=round(confidence, 3)
            )
            recommendations.append(rec)
            
        # Sort by confidence descending instead of raw similarity
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return recommendations

class MarketAssessor:
    def assess(self, candidate: CandidateProfile, recommendations: List[JobRecommendation]) -> MarketScore:
        if not recommendations:
            return MarketScore(0, [], [], {})
            
        best_confidence = max(r.confidence for r in recommendations)
        score = int(min(100, best_confidence * 100 + 10)) # Boost slightly for market score representation
        
        all_transferable = []
        for r in recommendations:
            all_transferable.extend(r.transferable_skills)
        # Unique strengths maintaining frequency ordering heuristic
        strengths = list(dict.fromkeys(all_transferable))[:3]
        if not strengths: strengths = candidate.skills[:3]
        
        all_missing = []
        for r in recommendations:
            all_missing.extend(r.missing_skills)
        weaknesses = list(dict.fromkeys(all_missing))[:3]
        
        readiness = {}
        seen_titles = set()
        for r in recommendations:
            title = r.job.title or "Unknown Role"
            if title not in seen_titles and len(seen_titles) < 3:
                readiness[title] = round(r.confidence, 2)
                seen_titles.add(title)
            
        return MarketScore(
            overall_score=score,
            strengths=strengths,
            weaknesses=weaknesses,
            readiness_by_role=readiness
        )
