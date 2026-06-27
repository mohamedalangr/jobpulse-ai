from typing import List, Dict
from src.intelligence.skills.models import SkillOccurrence
from collections import defaultdict

class SkillStatistics:
    @staticmethod
    def aggregate(occurrences: List[SkillOccurrence]) -> Dict[str, int]:
        """Returns the frequency of each canonical skill across the occurrences."""
        freq = defaultdict(int)
        for occ in occurrences:
            freq[occ.skill] += 1
        return dict(freq)
