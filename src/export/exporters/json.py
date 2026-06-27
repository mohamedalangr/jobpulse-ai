import json
from typing import List, Dict, Any
from src.export.exporters.base import BaseExporter

class JSONExporter(BaseExporter):
    @property
    def extension(self) -> str:
        return ".json"

    def export(self, data: List[Dict[str, Any]], filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
