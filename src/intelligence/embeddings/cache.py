import os
import json
import numpy as np
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class EmbeddingCache:
    def __init__(self, model_name: str, base_dir: str = "artifacts/embeddings"):
        self.model_name = model_name
        self.cache_dir = os.path.join(base_dir, model_name)
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.vectors_file = os.path.join(self.cache_dir, "embedding_index.npy")
        self.metadata_file = os.path.join(self.cache_dir, "metadata.json")
        self.fingerprints_file = os.path.join(self.cache_dir, "fingerprints.json")
        
        self._fingerprint_to_idx: Dict[str, int] = {}
        self._vectors: Optional[np.ndarray] = None
        
        self.load()

    def load(self) -> None:
        if os.path.exists(self.fingerprints_file) and os.path.exists(self.vectors_file):
            with open(self.fingerprints_file, 'r', encoding='utf-8') as f:
                self._fingerprint_to_idx = json.load(f)
            self._vectors = np.load(self.vectors_file)
        else:
            self._fingerprint_to_idx = {}
            self._vectors = None

    def save(self, provider: str = "sentence-transformers", pipeline_version: str = "0.4.0", dataset_version: str = "1.0") -> None:
        with open(self.fingerprints_file, 'w', encoding='utf-8') as f:
            json.dump(self._fingerprint_to_idx, f, indent=2)
            
        if self._vectors is not None:
            np.save(self.vectors_file, self._vectors)
            
            # Save robust metadata
            metadata = {
                "provider": provider,
                "model": self.model_name,
                "dimension": self._vectors.shape[1] if len(self._vectors.shape) > 1 else 0,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "pipeline_version": pipeline_version,
                "dataset_version": dataset_version,
                "record_count": len(self._fingerprint_to_idx)
            }
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)

    def get(self, fingerprint: str) -> Optional[np.ndarray]:
        if self._vectors is None:
            return None
        idx = self._fingerprint_to_idx.get(fingerprint)
        if idx is not None:
            return self._vectors[idx]
        return None

    def add(self, fingerprint: str, vector: np.ndarray) -> None:
        if fingerprint in self._fingerprint_to_idx:
            return # Already cached
            
        if self._vectors is None:
            self._vectors = np.expand_dims(vector, axis=0)
            self._fingerprint_to_idx[fingerprint] = 0
        else:
            idx = len(self._fingerprint_to_idx)
            self._vectors = np.vstack([self._vectors, vector])
            self._fingerprint_to_idx[fingerprint] = idx
