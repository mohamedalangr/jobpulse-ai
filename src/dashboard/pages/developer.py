import streamlit as st
from src.dashboard.client.api_client import JobPulseApiClient
from src.dashboard.components.error_ux import handle_api_error

st.title("⚙️ Developer & System")
st.markdown("Observability and telemetry for interviewers assessing the JobPulse AI platform maturity.")

client = JobPulseApiClient()

try:
    with st.spinner("Fetching system telemetry..."):
        health = client.get_health()
        version = client.get_version()
        ready = client.get_ready()

    st.subheader("Runtime Environment")
    col1, col2, col3 = st.columns(3)
    version_data = version.get("data", {})
    health_data = health.get("data", {})
    
    col1.metric("API Version", version_data.get("version", "Unknown"))
    col2.metric("Environment", health_data.get("environment", "Unknown"))
    col3.metric("Status", "Healthy" if health.get("success") else "Degraded")

    st.subheader("Subsystem Readiness")
    st.markdown("Verifies connections to PostgreSQL, FAISS, and the Embedding Registry.")
    readiness_data = ready.get("data", {})
    
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.json(readiness_data.get("checks", {}))
    with status_col2:
        if readiness_data.get("status") == "ok":
            st.success("All systems operational.")
        else:
            st.error("One or more subsystems are degraded.")

    st.subheader("Raw Telemetry Responses")
    with st.expander("View /health"):
        st.json(health)
    with st.expander("View /version"):
        st.json(version)

except Exception as e:
    handle_api_error(e)
