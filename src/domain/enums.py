"""
Domain enumerations.
"""
from enum import Enum

class ScraperStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"

class EmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    FREELANCE = "FREELANCE"
    INTERNSHIP = "INTERNSHIP"

class ExperienceLevel(str, Enum):
    ENTRY_LEVEL = "ENTRY_LEVEL"
    MID_LEVEL = "MID_LEVEL"
    SENIOR = "SENIOR"
    EXECUTIVE = "EXECUTIVE"

class JobSource(str, Enum):
    REMOTEOK = "REMOTEOK"
    GREENHOUSE = "GREENHOUSE"
    WWR = "WWR"
    MOCK = "MOCK"
