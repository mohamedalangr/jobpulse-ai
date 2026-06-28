import streamlit as st
from src.dashboard.client.api_client import JobPulseApiClient
from src.dashboard.components.error_ux import handle_api_error

st.title("🏠 JobPulse AI Operations")
st.markdown("Welcome to the **JobPulse AI** reference client. This dashboard demonstrates the API capabilities without importing any backend intelligence or domain logic.")

client = JobPulseApiClient()

try:
    with st.spinner("Fetching platform status..."):
        health_res = client.get_health()
        health_data = health_res.get("data", {})
        
    st.subheader("Platform Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Status", health_data.get("status", "Unknown"))
    col2.metric("Environment", health_data.get("environment", "Unknown"))
    col3.metric("Timestamp", health_data.get("timestamp", "Unknown")[:10] if isinstance(health_data.get("timestamp"), str) else "Active")
    col4.metric("Version", "v0.5.0")
    
    # Pipeline execution is disabled in the Vercel serverless Cloud Edition
    # due to execution time limits on web scraping and background workers.
    # It remains fully functional in the local Enterprise Edition.

except Exception as e:
    handle_api_error(e)
