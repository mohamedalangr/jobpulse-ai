from typing import List
from src.intelligence.learning.models import LearningMilestone, SkillROI
from src.intelligence.learning.graph import LearningGraph

class CurriculumGenerator:
    def __init__(self, graph: LearningGraph):
        self.graph = graph

    def generate(self, top_rois: List[SkillROI]) -> List[LearningMilestone]:
        if not top_rois:
            return []
            
        milestones = []
        phases = [
            ("Phase 1: High-Impact Fundamentals", top_rois[:2]),
            ("Phase 2: Market Expansion", top_rois[2:5]),
            ("Phase 3: Advanced Specialization", top_rois[5:8])
        ]
        
        for title, rois in phases:
            if not rois: continue
            
            skills = [r.skill for r in rois]
            hours = sum(r.learning_time_hours for r in rois)
            
            unlocks = set()
            for s in skills:
                node = self.graph.get_node(s)
                if node: unlocks.update(node.unlocks)
                
            expected_delta = sum(r.salary_gain_pct for r in rois) / len(rois)
            
            milestones.append(LearningMilestone(
                title=title,
                estimated_hours=hours,
                skills=skills,
                unlocks=list(unlocks)[:3],
                expected_salary_delta=round(expected_delta, 1)
            ))
            
        return milestones
