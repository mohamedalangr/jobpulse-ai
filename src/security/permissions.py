from enum import Enum

class Permission(str, Enum):
    SEARCH = "search"
    CAREER_ANALYSIS = "career_analysis"
    LEARNING_PLAN = "learning_plan"
    RUN_PIPELINE = "run_pipeline"
    VIEW_ANALYTICS = "view_analytics"
    ADMIN = "admin"
