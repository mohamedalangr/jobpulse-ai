import os
import json
import numpy as np
import faiss
from typing import List, Tuple, Dict
from src.intelligence.vectorstore.base import VectorStore

class FaissVectorStore(VectorStore):
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_map: Dict[int, str] = {}
        self.reverse_id_map: Dict[str, int] = {}
        self._next_id = 0

    def add(self, vectors: np.ndarray, ids: List[str]) -> None:
        if len(vectors) != len(ids):
            raise ValueError("Vectors and ids must have the same length")
            
        self.index.add(vectors.astype(np.float32))
        
        for str_id in ids:
            self.id_map[self._next_id] = str_id
            self.reverse_id_map[str_id] = self._next_id
            self._next_id += 1

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, List[List[str]]]:
        distances, indices = self.index.search(query_vector.astype(np.float32), top_k)
        
        result_ids = []
        for row in indices:
            row_ids = [self.id_map[idx] for idx in row if idx != -1]
            result_ids.append(row_ids)
            
        return distances, result_ids

    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        faiss.write_index(self.index, f"{filepath}.faiss")
        with open(f"{filepath}_meta.json", "w", encoding="utf-8") as f:
            json.dump({
                "id_map": {str(k): v for k, v in self.id_map.items()},
                "dimension": self.dimension,
                "next_id": self._next_id
            }, f)

    def load(self, filepath: str) -> None:
        self.index = faiss.read_index(f"{filepath}.faiss")
        with open(f"{filepath}_meta.json", "r", encoding="utf-8") as f:
            meta = json.load(f)
            self.dimension = meta["dimension"]
            self._next_id = meta["next_id"]
            self.id_map = {int(k): v for k, v in meta["id_map"].items()}
            self.reverse_id_map = {v: k for k, v in self.id_map.items()}

    def count(self) -> int:
        return self.index.ntotal
