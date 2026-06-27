import sys
from src.core.config import settings
from src.services.startup import startup, StartupResult
from src.core.exceptions import DatabaseConnectionError

# Force UTF-8 output to support checkmarks on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def print_banner():
    banner = f"""
====================================

        {settings.app_name}

Labor Market Intelligence Platform

Version {settings.app_version}

====================================
"""
    print(banner)

def print_status(component: str, success: bool):
    symbol = "✓" if success else "✗"
    print(f"{symbol} {component}")

def main():
    print_banner()
    try:
        result = startup()
        print_status("Configuration Loaded", result.configuration_loaded)
        print_status("Logger Initialized", result.logger_initialized)
        print_status("Database Connected", result.database_connected)
        print("\nSystem Ready")
        print("====================================")
    except DatabaseConnectionError as e:
        print_status("Configuration Loaded", True)
        print_status("Logger Initialized", True)
        print_status("Database Connected", False)
        print(f"\nSystem Startup Failed: {e}")
        print("====================================")
        sys.exit(1)
    except Exception as e:
        print(f"\nCritical System Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
