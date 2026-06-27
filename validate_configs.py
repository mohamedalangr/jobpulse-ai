from src.application.config.settings import ConfigManager
import sys

def main():
    try:
        manager = ConfigManager()
        print("Configuration parsed successfully!")
        print(f"API Port: {manager.app_settings.api.port}")
        print(f"Loaded {len(manager.model_settings.models)} models")
        print(f"Loaded {len(manager.feature_settings.features)} features")
        sys.exit(0)
    except Exception as e:
        print(f"Error parsing configuration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
