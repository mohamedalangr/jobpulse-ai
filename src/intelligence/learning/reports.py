import os
from src.intelligence.career.profiles.candidate import CandidateProfile
from src.intelligence.learning.models import LearningPlan

class LearningReportRenderer:
    def render(self, candidate: CandidateProfile, plan: LearningPlan, output_path: str) -> None:
        lines = []
        lines.append("# Personalized Learning Intelligence")
        lines.append("")
        
        lines.append("## Executive Summary")
        lines.append(f"**Target Role Profile**: {plan.candidate_role}")
        lines.append(f"**Estimated Total Effort**: {plan.total_estimated_hours} hours")
        lines.append(f"**Projected Salary Gain**: +{plan.projected_salary_gain_pct}%")
        lines.append(f"**Overall Plan ROI Score**: {plan.evaluation.roi_score}")
        lines.append("")
        
        if plan.top_synergy:
            lines.append("## Highest ROI Skill Combination")
            lines.append(f"**{ ' + '.join(plan.top_synergy.skills) }**")
            lines.append(f"- **Estimated Learning Time**: {plan.top_synergy.estimated_learning_time} hours")
            lines.append(f"- **Jobs Unlocked**: +{plan.top_synergy.jobs_unlocked}")
            lines.append(f"- **Salary Increase**: +{plan.top_synergy.salary_increase_pct}%")
            lines.append(f"- **Match Confidence**: {plan.top_synergy.confidence:.2f}")
            lines.append("")
            
        lines.append("## Opportunity Gain Simulation")
        for state in plan.simulations:
            lines.append(f"### {state.state_name}")
            lines.append(f"- **Career Paths (Unique Titles)**: {state.career_paths}")
            lines.append(f"- **Average Match Confidence**: {state.match_confidence*100:.1f}%")
            lines.append(f"- **Average Salary**: ${state.average_salary:,.0f}")
            lines.append("")
            
        lines.append("## Skill ROI Ranking")
        lines.append("| Skill | Est. Hours | Unlocked Jobs | Salary Gain | ROI Rating |")
        lines.append("|-------|------------|---------------|-------------|------------|")
        for roi in plan.skill_rois:
            lines.append(f"| {roi.skill} | {roi.learning_time_hours}h | +{roi.jobs_unlocked} | +{roi.salary_gain_pct}% | {roi.roi_rating} |")
        lines.append("")
        
        lines.append("## Learning Curriculum")
        for m in plan.milestones:
            lines.append(f"### {m.title}")
            lines.append(f"- **Estimated Time**: {m.estimated_hours} hours")
            lines.append(f"- **Skills**: {', '.join(m.skills)}")
            lines.append(f"- **Unlocks**: {', '.join(m.unlocks) if m.unlocks else 'None'}")
            lines.append("")
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
