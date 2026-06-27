import streamlit as st
from src.dashboard.client.api_client import JobPulseApiClient
from src.dashboard.components.error_ux import handle_api_error
from src.dashboard.state import get_candidate_profile

st.title("📚 Learning Intelligence")
st.markdown("Generate an ROI-focused learning roadmap detailing exact salary impacts and unlocked opportunities.")

profile = get_candidate_profile()

if st.button("Generate Learning Plan", type="primary", use_container_width=True):
    client = JobPulseApiClient()
    try:
        with st.spinner("Calculating skill impact and assembling roadmap..."):
            response = client.generate_learning_plan(profile)
            
        data = response.get("data", {})
        
        st.subheader("Recommended Next Skill")
        st.success(f"### {data.get('recommended_skill', 'Unknown')}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Expected Salary Increase", f"+{data.get('projected_salary_increase_pct', 0)}%")
        col2.metric("Unlocked Opportunities", f"+{data.get('unlocked_opportunities', 0)}")
        col3.metric("ROI Score", f"{data.get('roi_score', 0.0):.2f}")
        
        st.subheader("Step-by-Step Roadmap")
        roadmap = data.get("roadmap", [])
        if roadmap:
            for step in roadmap:
                with st.container():
                    st.markdown(f"#### {step.get('step', 'Step')} - {step.get('skill', 'Skill')}")
                    st.markdown(f"**Reason:** {step.get('reason', '')}")
                    st.divider()
        else:
            st.info("No detailed roadmap steps returned.")
                
        with st.expander("Raw Learning Response"):
            st.json(data)

    except Exception as e:
        handle_api_error(e)
