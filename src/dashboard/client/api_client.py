from src.dashboard.client.transport import Transport

class JobPulseApiClient:
    def __init__(self):
        self.transport = Transport()

    # Core Intelligence
    def search_jobs(self, query: str) -> dict:
        return self.transport.post("/search/semantic", json_data={"query": query})
        
    def analyze_candidate(self, profile: dict) -> dict:
        return self.transport.post("/career/analyze", json_data=profile)

    def generate_learning_plan(self, profile: dict) -> dict:
        return self.transport.post("/learning/plan", json_data=profile)

    def get_market_report(self) -> dict:
        return self.transport.get("/market/discovery")

    def run_pipeline(self) -> dict:
        return self.transport.post("/pipeline/run")

    # Developer Observability
    def get_health(self) -> dict:
        return self.transport.get("/health")

    def get_version(self) -> dict:
        return self.transport.get("/version")

    def get_ready(self) -> dict:
        return self.transport.get("/ready")
