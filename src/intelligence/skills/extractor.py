import re
from typing import List
from src.domain.entities.job_posting import JobPosting
from src.intelligence.skills.ontology import SkillOntology
from src.intelligence.skills.models import SkillOccurrence

class SkillExtractor:
    def __init__(self, ontology: SkillOntology):
        self.ontology = ontology
        
        # Build regex for word-boundary alias matching (longest aliases first)
        aliases = sorted(self.ontology.alias_map.keys(), key=len, reverse=True)
        escaped_aliases = [re.escape(a) for a in aliases if len(a) > 1]
        
        if escaped_aliases:
            self.pattern = re.compile(r'\b(' + '|'.join(escaped_aliases) + r')\b', re.IGNORECASE)
        else:
            self.pattern = None

    def extract_from_text(self, text: str, source: str) -> List[SkillOccurrence]:
        if not text or not self.pattern:
            return []
            
        occurrences = []
        for match in self.pattern.finditer(text):
            raw_match = match.group(1)
            canonical = self.ontology.resolve(raw_match)
            if canonical:
                occurrences.append(
                    SkillOccurrence(
                        skill=canonical,
                        confidence=0.9,
                        source=source,
                        start_offset=match.start(),
                        end_offset=match.end()
                    )
                )
        return occurrences
        
    def extract_all(self, job: JobPosting) -> List[SkillOccurrence]:
        results = []
        
        if job.title:
            results.extend(self.extract_from_text(job.title, "title"))
            
        if job.description:
            results.extend(self.extract_from_text(job.description, "description"))
            
        return results
