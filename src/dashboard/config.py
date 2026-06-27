from pydantic_settings import BaseSettings
from pydantic import Field
import yaml
import os

class DashboardSettings(BaseSettings):
    api_url: str = Field(default="http://localhost:8000/api/v1", validation_alias="API_URL")
    api_key: str = Field(default="dev-secret-key", validation_alias="API_KEY")
    request_timeout: int = Field(default=30, validation_alias="REQUEST_TIMEOUT")

def load_settings() -> DashboardSettings:
    settings_dict = {}
    
    yaml_path = os.path.join(os.getcwd(), "config", "dashboard.yaml")
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data:
                settings_dict.update(yaml_data)
                
    # pydantic_settings will automatically override kwargs with Environment Variables
    return DashboardSettings(**settings_dict)

settings = load_settings()
