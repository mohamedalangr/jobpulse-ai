import pandas as pd
from typing import List, Dict, Any
from src.export.exporters.base import BaseExporter

class ParquetExporter(BaseExporter):
    @property
    def extension(self) -> str:
        return ".parquet"

    def export(self, data: List[Dict[str, Any]], filepath: str) -> None:
        df = pd.DataFrame(data)
        df.to_parquet(filepath, index=False)
