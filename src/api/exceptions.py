class JobPulseError(Exception):
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(JobPulseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("VALIDATION_ERROR", message, details)

class SearchError(JobPulseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("SEARCH_ERROR", message, details)

class ConfigurationError(JobPulseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("CONFIGURATION_ERROR", message, details)

class IntelligenceError(JobPulseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("INTELLIGENCE_ERROR", message, details)

class AuthenticationError(JobPulseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("AUTHENTICATION_ERROR", message, details)

class AuthorizationError(JobPulseError):
    def __init__(self, message: str, details: dict = None):
        super().__init__("AUTHORIZATION_ERROR", message, details)
