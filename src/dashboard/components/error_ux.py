import streamlit as st
from src.dashboard.client.exceptions import ApiClientError
from src.dashboard.config import settings

def handle_api_error(e: Exception):
    """Provides a consistent, traceback-free error UX for the dashboard."""
    if isinstance(e, ApiClientError):
        if e.status_code == 401:
            st.error("❌ **Invalid API Key**. Please check your configuration.")
        elif e.status_code == 403:
            st.error("🚫 **Permission Denied**. Your API Key lacks the required privileges.")
        elif e.status_code == 503:
            st.error(f"📡 **Unable to reach API**.\n\n**API URL**: `{settings.api_url}`\n\n**Status**: `503 Service Unavailable`")
        else:
            st.error(f"⚠️ **API Error** ({e.status_code}): {e.message}")
            if e.details:
                with st.expander("Error Details"):
                    st.json(e.details)
    else:
        st.error(f"🛑 **Unexpected Dashboard Error**: {str(e)}")
