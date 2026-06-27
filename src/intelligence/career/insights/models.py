from dataclasses import dataclass

@dataclass
class CareerInsights:
    most_valuable_skill: str
    most_valuable_skill_prevalence: float # e.g. 0.72 for 72%
    highest_salary_increase_role: str
    highest_salary_increase_pct: float
    fastest_transition_role: str
    fastest_transition_gap: str
