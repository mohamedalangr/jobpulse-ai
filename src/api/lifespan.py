from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from src.application.config.settings import ConfigManager
from src.application.providers.feature_flags import init_feature_provider
from src.application.models.registry import ModelRegistry
from src.application.providers.embedding import get_embedding_provider

logger = logging.getLogger("api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load settings
    config_manager = ConfigManager()
    
    # Fail-fast validation
    if not config_manager.security_settings.api_key_hash:
        raise RuntimeError("CRITICAL: API key hash configuration is missing. Refusing to start.")
        
    init_feature_provider(config_manager)
    
    model_registry = ModelRegistry(config_manager)
    
    app.state.config_manager = config_manager
    app.state.model_registry = model_registry
    
    # Check preload logic
    preload_settings = config_manager.app_settings.preload
    
    if preload_settings.embeddings:
        logger.info("Preloading embedding model...")
        provider = get_embedding_provider(model_registry)
        provider._ensure_loaded()
        
    # Mark startup as successfully completed for /health/startup
    app.state.startup_complete = True
        
    logger.info("Application lifespan started.")
    yield
    
    logger.info("Application lifespan ended.")
