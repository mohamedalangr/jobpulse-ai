import streamlit as st
from src.dashboard.client.api_client import JobPulseApiClient
from src.dashboard.components.error_ux import handle_api_error
from src.dashboard.components.job_cards import render_job_card

st.title("🔍 Semantic Search")
st.markdown("Discover opportunities using natural language context instead of strict keywords.")

query = st.text_input("Describe your ideal role:", value="I want a remote backend engineering role focused on distributed systems and Python.")

if st.button("Search Jobs", type="primary", use_container_width=True):
    client = JobPulseApiClient()
    try:
        with st.spinner("Searching semantic vectors..."):
            response = client.search_jobs(query)
            
        data = response.get("data", {})
        results = data.get("results", [])
        
        if not results:
            st.warning("No matching opportunities found.")
        else:
            st.success(f"Found {len(results)} relevant positions.")
            for match in results:
                # Based on the API schema, match contains 'job' and 'score'
                job = match.get("job", match)
                score = match.get("score")
                render_job_card(job, score)
                
    except Exception as e:
        handle_api_error(e)
