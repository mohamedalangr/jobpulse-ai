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
    
    st.divider()
    
    st.subheader("Pipeline Operations")
    st.markdown("Manually trigger the data ingestion and intelligence pipeline.")
    
    if st.button("🚀 Run Pipeline", use_container_width=True):
        try:
            with st.spinner("Pipeline is running... This may take a minute."):
                res = client.run_pipeline()
                st.success("✅ Pipeline executed successfully!")
                with st.expander("Pipeline Output"):
                    st.json(res)
        except Exception as e:
            handle_api_error(e)

except Exception as e:
    handle_api_error(e)
