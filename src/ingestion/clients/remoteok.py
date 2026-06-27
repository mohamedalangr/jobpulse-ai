from src.ingestion.clients.base import BaseHttpClient
from typing import List, Dict, Any

class RemoteOKClient(BaseHttpClient):
    def __init__(self):
        super().__init__(base_url="https://remoteok.com", timeout=15)

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        # RemoteOK returns a JSON array
        return self.get("/api")
