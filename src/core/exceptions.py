"""
Custom exceptions for JobPulse AI.
"""

class ConfigurationError(Exception):
    """Raised when there is a configuration error."""
    pass

class DatabaseConnectionError(Exception):
    """Raised when the database connection fails."""
    pass

class ScrapingError(Exception):
    """Raised when a scraping operation fails."""
    pass

class ETLError(Exception):
    """Raised when an ETL pipeline operation fails."""
    pass

class ModelTrainingError(Exception):
    """Raised when a machine learning model fails to train."""
    pass
