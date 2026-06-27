import yaml
import os
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class CanonicalSkill(BaseModel):
    category: str
    aliases: List[str] = Field(default_factory=list)
    related: List[str] = Field(default_factory=list)

class SkillOntology:
    def __init__(self, filepath: str = "config/skills.yaml"):
        self.filepath = filepath
        self.skills: Dict[str, CanonicalSkill] = {}
        self.alias_map: Dict[str, str] = {}
        
        if os.path.exists(self.filepath):
            self.load()

    def load(self) -> None:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
            
        for canonical_name, props in data.items():
            skill = CanonicalSkill.model_validate(props)
            self.skills[canonical_name] = skill
            
            # Map canonical itself
            self.alias_map[canonical_name.lower()] = canonical_name
            for alias in skill.aliases:
                self.alias_map[alias.lower()] = canonical_name

    def resolve(self, term: str) -> Optional[str]:
        """Resolves an alias to its canonical name."""
        return self.alias_map.get(term.lower().strip())
