from enum import Enum

class ModelCategory(str, Enum):
    EMBEDDING = "embedding"
    REDUCER = "reducer"
    CLUSTERER = "clusterer"
    FORECAST = "forecast"
    RECOMMENDATION = "recommendation"
