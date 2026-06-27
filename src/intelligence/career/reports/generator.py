import os
from src.intelligence.career.matching.models import RecommendationResult
from src.intelligence.career.profiles.candidate import CandidateProfile, MarketScore

class CareerReportRenderer:
    def render(self, candidate: CandidateProfile, market_score: MarketScore, result: RecommendationResult, output_path: str) -> None:
        lines = []
        lines.append("# Career Intelligence Report")
        lines.append("")
        
        # Profile Summary
        lines.append("## Profile Summary")
        lines.append(f"**Current Role**: {candidate.current_role or 'Unknown'}")
        lines.append(f"**Experience**: {candidate.experience}")
        if candidate.salary_expectation:
            lines.append(f"**Target Salary**: ${candidate.salary_expectation:,.0f}")
        lines.append(f"**Core Skills**: {', '.join(candidate.skills)}")
        lines.append("")
        
        # Candidate vs Market
        lines.append("## Candidate vs Market")
        lines.append(f"**Market Competitiveness Score**: {market_score.overall_score} / 100")
        lines.append(f"- **Strengths**: {', '.join(market_score.strengths)}")
        lines.append(f"- **Weaknesses**: {', '.join(market_score.weaknesses)}")
        lines.append("")
        lines.append("### Estimated Readiness")
        for role, readiness in market_score.readiness_by_role.items():
            pct = int(readiness * 100)
            lines.append(f"- **{role}**: {pct}%")
        lines.append("")
        
        # Transition Path
        lines.append("## Recommended Career Transition")
        if result.transition_path:
            path = " ➔ ".join([candidate.current_role or "Candidate"] + [e.to_role for e in result.transition_path])
            lines.append(f"**{path}**")
            lines.append("")
            lines.append("### Stepping Stones")
            for edge in result.transition_path:
                lines.append(f"- **{edge.to_role}** (+{edge.salary_delta_pct}% Salary | Difficulty: {edge.difficulty})")
                lines.append(f"  - *Learn*: {', '.join(edge.required_skills[:3]) if edge.required_skills else 'None'}")
        else:
            lines.append("*No clear transition path identified.*")
        lines.append("")
        
        # Insights
        lines.append("## Market Insights")
        lines.append(f"- **Most Valuable Skill**: {result.insights.most_valuable_skill} (Appears in {result.insights.most_valuable_skill_prevalence*100:.0f}% of similar roles)")
        lines.append(f"- **Highest Salary Increase**: {result.insights.highest_salary_increase_role} (+{result.insights.highest_salary_increase_pct}%)")
        lines.append(f"- **Fastest Transition**: {result.insights.fastest_transition_role} (Gap: {result.insights.fastest_transition_gap})")
        lines.append("")
        
        # Top Matches
        lines.append("## Top Job Matches")
        for i, rec in enumerate(result.recommendations[:3]):
            lines.append(f"### {i+1}. {rec.job.title} at {rec.job.company}")
            lines.append(f"**Match Confidence**: {rec.confidence:.2f} | **Salary Delta**: +{rec.salary_delta_pct or 0}% | **Demand**: {rec.market_demand_score}")
            lines.append(f"- **Transferable Skills**: {', '.join(rec.transferable_skills[:5])}")
            lines.append(f"- **Missing Skills**: {', '.join(rec.missing_skills[:5])}")
            lines.append(f"- **Emerging Skills**: {', '.join(rec.emerging_skills[:3])}")
            lines.append("")
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
