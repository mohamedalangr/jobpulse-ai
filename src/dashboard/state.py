import streamlit as st

def init_state():
    if "api_key" not in st.session_state:
        from src.dashboard.config import settings
        st.session_state.api_key = settings.api_key
    if "candidate_profile" not in st.session_state:
        st.session_state.candidate_profile = {
            "skills": ["python", "docker", "fastapi", "kubernetes", "aws", "postgresql"],
            "experience": "Mid-level backend engineer specializing in APIs and data pipelines.",
            "desired_roles": ["Backend Engineer", "Platform Engineer", "Data Engineer"],
            "preferred_locations": ["Remote", "New York"]
        }

def get_api_key() -> str:
    return st.session_state.get("api_key", "")

def set_api_key(api_key: str):
    st.session_state.api_key = api_key

def get_candidate_profile() -> dict:
    return st.session_state.get("candidate_profile", {})

def set_candidate_profile(profile: dict):
    st.session_state.candidate_profile = profile
