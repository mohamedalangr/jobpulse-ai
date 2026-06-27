from dataclasses import dataclass
from typing import List
from src.application.queries.base import QueryHandler
from src.application.context import RequestContext
from src.intelligence.clustering.summaries import ClusterSummary

@dataclass
class DiscoverMarketQuery:
    min_cluster_size: int = 5

class DiscoverMarketUseCase(QueryHandler):
    def __init__(self, dataset_provider, clustering_engine, analyzer, labeler):
        self.dataset_provider = dataset_provider
        self.engine = clustering_engine
        self.analyzer = analyzer
        self.labeler = labeler

    def execute(self, query: DiscoverMarketQuery, context: RequestContext) -> List[ClusterSummary]:
        dataset = self.dataset_provider.get_dataset()
        if not dataset:
            return []
            
        cluster_dataset = self.engine.cluster(dataset)
        summaries = self.analyzer.analyze(cluster_dataset)
        
        return summaries
