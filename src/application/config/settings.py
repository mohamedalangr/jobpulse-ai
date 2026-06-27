from pydantic import BaseModel
from typing import Dict, Optional
import yaml
import os

class ApiSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    title: str = "JobPulse AI"
    description: str = ""

class ApplicationSettings(BaseModel):
    version: str
    environment: str
    debug: bool = False
    api: ApiSettings

class FeatureFlag(BaseModel):
    enabled: bool = False
    rollout: int = 100
    min_version: Optional[str] = None

class FeatureSettings(BaseModel):
    features: Dict[str, FeatureFlag]

class ModelDescriptorConfig(BaseModel):
    id: str
    name: str
    version: str
    category: str
    provider: str
    dimension: Optional[int] = None
    framework: str
    checksum: Optional[str] = None

class ModelSettings(BaseModel):
    models: Dict[str, ModelDescriptorConfig]

class ConfigManager:
    """Loads and validates all configurations synchronously at startup."""
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.app_settings = self._load(ApplicationSettings, "application.yaml")
        self.feature_settings = self._load(FeatureSettings, "features.yaml")
        self.model_settings = self._load(ModelSettings, "models.yaml")
        
    def _load(self, model_class, filename: str):
        path = os.path.join(self.config_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required configuration file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            
        return model_class(**data)
