import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SkillNode:
    name: str
    estimated_hours: float
    difficulty: str
    category: str
    demand_weight: float
    prerequisites: List[str]
    unlocks: List[str]

class LearningGraph:
    def __init__(self, graph_path: str, meta_path: str):
        self.nodes: Dict[str, SkillNode] = {}
        
        with open(graph_path, 'r', encoding='utf-8') as f:
            graph_data = yaml.safe_load(f) or {}
            
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta_data = yaml.safe_load(f) or {}
            
        for skill, g_info in graph_data.items():
            m_info = meta_data.get(skill, {})
            self.nodes[skill] = SkillNode(
                name=skill,
                estimated_hours=m_info.get("estimated_hours", 20.0),
                difficulty=m_info.get("difficulty", "intermediate"),
                category=m_info.get("category", "unknown"),
                demand_weight=m_info.get("demand_weight", 0.5),
                prerequisites=g_info.get("prerequisites", []),
                unlocks=g_info.get("unlocks", [])
            )
            
    def get_node(self, skill: str) -> Optional[SkillNode]:
        return self.nodes.get(skill.lower())

    def get_learning_path(self, target_skill: str) -> List[str]:
        path = []
        visited = set()
        
        def dfs(node_name: str):
            if node_name in visited: return
            visited.add(node_name)
            node = self.get_node(node_name)
            if node:
                for prereq in node.prerequisites:
                    dfs(prereq)
                path.append(node_name)
                
        dfs(target_skill.lower())
        return path
