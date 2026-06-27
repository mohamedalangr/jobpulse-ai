import os
import json
import csv
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import numpy as np
from src.intelligence.analytics.dataset import EmbeddingDataset

class Visualizer(ABC):
    @abstractmethod
    def render(self, 
               dataset: EmbeddingDataset, 
               reduced_vectors: np.ndarray, 
               labels: List[str], 
               metrics: Dict[str, Any],
               output_dir: str) -> str:
        """
        Renders the visualization and dumps all configuration/coordinate artifacts.
        """
        pass

class MatplotlibVisualizer(Visualizer):
    def render(self, 
               dataset: EmbeddingDataset, 
               reduced_vectors: np.ndarray, 
               labels: List[str], 
               metrics: Dict[str, Any],
               output_dir: str) -> str:
        import matplotlib.pyplot as plt
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Export Coordinates (CSV)
        csv_path = os.path.join(output_dir, "coordinates.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["fingerprint", "x", "y", "label"])
            for fp, vec, label in zip(dataset.fingerprints, reduced_vectors, labels):
                writer.writerow([fp, float(vec[0]), float(vec[1]), label])
                
        # 2. Export Metrics/Config (JSON)
        json_path = os.path.join(output_dir, "metrics.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "dataset_metadata": dataset.metadata,
                "model_name": dataset.model_name,
                "reduction_metrics": metrics
            }, f, indent=2)
            
        # 3. Export PNG
        png_path = os.path.join(output_dir, "projection.png")
        
        plt.figure(figsize=(10, 8))
        
        unique_labels = list(set(labels))
        if len(unique_labels) > 20:
            plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], c='gray', alpha=0.5, s=15)
        else:
            for label in unique_labels:
                idx = [i for i, x in enumerate(labels) if x == label]
                plt.scatter(reduced_vectors[idx, 0], reduced_vectors[idx, 1], label=label, alpha=0.7, s=20)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', markerscale=2)

        reducer_name = metrics.get('reducer', 'Unknown Reducer')
        model_name = dataset.model_name
        samples = metrics.get('samples', 0)
        ds_version = dataset.metadata.get('dataset_version', 'v1.0')
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        title = f"{reducer_name} Projection\nModel: {model_name} | Jobs: {samples} | Dataset: {ds_version} | Date: {date_str}"
        plt.title(title, pad=15)
        
        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.tight_layout()
        plt.savefig(png_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return png_path
