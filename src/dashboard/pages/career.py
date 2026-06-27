import streamlit as st
from src.dashboard.client.api_client import JobPulseApiClient
from src.dashboard.components.error_ux import handle_api_error
from src.dashboard.state import get_candidate_profile, set_candidate_profile
import json

st.title("📈 Career Intelligence")
st.markdown("Analyze a candidate's profile against the current job market to reveal readiness and optimal transition paths.")

profile = get_candidate_profile()

with st.expander("👤 Edit Candidate Profile", expanded=False):
    updated_profile_str = st.text_area(
        "JSON Profile", 
        value=json.dumps(profile, indent=2),
        height=200
    )
    if st.button("Save Profile"):
        try:
            set_candidate_profile(json.loads(updated_profile_str))
            st.success("Profile updated! Click below to analyze.")
            st.rerun()
        except json.JSONDecodeError:
            st.error("Invalid JSON format.")

if st.button("Analyze Career Potential", type="primary", use_container_width=True):
    client = JobPulseApiClient()
    try:
        with st.spinner("Analyzing market fit and transition probabilities..."):
            response = client.analyze_candidate(profile)
            
        data = response.get("data", {})
        
        col1, col2 = st.columns(2)
        col1.metric("Market Readiness Score", f"{data.get('readiness_score', 0.0):.2f}")
        col2.metric("Uncapped Opportunities", data.get("total_opportunities", 0))
        
        st.subheader("Missing Core Skills")
        skills = data.get("missing_skills", [])
        if skills:
            st.write(", ".join(skills))
        else:
            st.success("No critical skill gaps identified!")
            
        st.subheader("Optimal Transition Paths")
        transitions = data.get("transition_graph", [])
        if transitions:
            for t in transitions:
                st.info(f"**{t.get('current_role', 'Current')} ➔ {t.get('next_role', 'Target')}** (Confidence: {t.get('confidence_score', 0):.2f})")
        else:
            st.info("No transition graph provided in the response.")
            
        with st.expander("Raw Analysis Response"):
            st.json(data)

    except Exception as e:
        handle_api_error(e)
