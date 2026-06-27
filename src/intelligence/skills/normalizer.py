from typing import List
from src.intelligence.skills.ontology import SkillOntology
from src.intelligence.skills.models import SkillOccurrence

class SkillNormalizer:
    def __init__(self, ontology: SkillOntology):
        self.ontology = ontology

    def normalize(self, raw_skills: List[str], source: str = "metadata") -> List[SkillOccurrence]:
        occurrences = []
        for raw in raw_skills:
            canonical = self.ontology.resolve(raw)
            if canonical:
                occurrences.append(
                    SkillOccurrence(
                        skill=canonical,
                        confidence=1.0,
                        source=source
                    )
                )
        return occurrences
