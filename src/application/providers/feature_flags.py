from src.application.config.settings import ConfigManager

class FeatureFlagProvider:
    def __init__(self, config_manager: ConfigManager):
        self.features = config_manager.feature_settings.features

    def is_enabled(self, feature_name: str) -> bool:
        flag = self.features.get(feature_name)
        if not flag:
            return False
        return flag.enabled

_global_feature_provider = None

def init_feature_provider(config_manager: ConfigManager) -> None:
    global _global_feature_provider
    _global_feature_provider = FeatureFlagProvider(config_manager)

def get_feature_provider() -> FeatureFlagProvider:
    if not _global_feature_provider:
        raise RuntimeError("FeatureFlagProvider not initialized")
    return _global_feature_provider
