import os
from typing import List
import numpy as np
import httpx
from openai import OpenAI

from src.intelligence.embeddings.base import EmbeddingProvider

class HostedEmbeddingProvider(EmbeddingProvider):
    pass

class OpenAIProvider(HostedEmbeddingProvider):
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def embed(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            input=text,
            model=self.model_name
        )
        return np.array(response.data[0].embedding, dtype=np.float32)

    def embed_many(self, texts: List[str]) -> np.ndarray:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model_name
        )
        embeddings = [data.embedding for data in response.data]
        return np.array(embeddings, dtype=np.float32)


class HuggingFaceProvider(HostedEmbeddingProvider):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
        self.token = os.environ.get("HF_TOKEN")
        if not self.token:
            raise RuntimeError("HF_TOKEN environment variable is required for HuggingFaceProvider")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _call_api(self, payload: dict) -> list:
        with httpx.Client() as client:
            response = client.post(self.api_url, headers=self.headers, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()

    def embed(self, text: str) -> np.ndarray:
        result = self._call_api({"inputs": text})
        return np.array(result, dtype=np.float32)

    def embed_many(self, texts: List[str]) -> np.ndarray:
        result = self._call_api({"inputs": texts})
        return np.array(result, dtype=np.float32)
