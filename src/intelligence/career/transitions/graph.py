from typing import List
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.career.explainability.models import JobRecommendation
from src.intelligence.career.transitions.models import TransitionEdge

class TransitionGraphGenerator:
    def generate(self, candidate: CandidateProfile, recommendations: List[JobRecommendation]) -> List[TransitionEdge]:
        edges = []
        current_role = candidate.current_role or "Candidate"
        
        for rec in recommendations:
            to_role = rec.job.title or "Unknown Role"
            
            # Layer 2: Business Constraints
            curr_lower = current_role.lower()
            to_lower = to_role.lower()
            if "junior" in curr_lower and ("principal" in to_lower or "director" in to_lower):
                continue
                
            # Compute Difficulty
            difficulty = "Low"
            if len(rec.missing_skills) > 5:
                difficulty = "High"
            elif len(rec.missing_skills) > 2:
                difficulty = "Medium"
                
            # Score for ranking (Layer 3)
            salary_bonus = min(rec.salary_delta_pct or 0.0, 50.0) / 100.0
            rank_score = rec.confidence + (salary_bonus * 0.5) - (len(rec.missing_skills) * 0.05)
            
            edge = TransitionEdge(
                from_role=current_role,
                to_role=to_role,
                similarity=rec.similarity_score,
                salary_delta_pct=rec.salary_delta_pct or 0.0,
                required_skills=rec.missing_skills,
                difficulty=difficulty
            )
            edges.append((edge, rank_score))
            
        # Layer 3: Sort by calculated rank_score
        edges.sort(key=lambda x: x[1], reverse=True)
        
        # Deduplicate to_roles for clean transition path
        unique_edges = []
        seen = set()
        for edge, score in edges:
            if edge.to_role not in seen:
                seen.add(edge.to_role)
                unique_edges.append(edge)
                if len(unique_edges) >= 3:
                    break
                    
        return unique_edges
