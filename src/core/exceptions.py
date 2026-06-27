"""
Custom exceptions for JobPulse AI.
"""

class JobPulseError(Exception):
    """Base exception for all JobPulse AI errors."""
    pass

class DatabaseConnectionError(JobPulseError):
    """Exception raised when the database is unreachable."""
    pass

class ConfigurationError(Exception):
    """Raised when there is a configuration error."""
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
