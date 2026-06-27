import streamlit as st

def render_job_card(job: dict, score: float = None):
    with st.container():
        st.markdown(f"### {job.get('title', 'Unknown Title')}")
        
        # Meta info
        company = job.get('company', 'Unknown Company')
        location = job.get('location', 'Remote')
        salary = job.get('salary_range', 'Salary Unspecified')
        st.markdown(f"**{company}** | 📍 {location} | 💰 {salary}")
        
        if score is not None:
            st.caption(f"Semantic Similarity: {score:.3f}")
            
        st.markdown(f"*{job.get('job_type', 'Full-Time')}*")
        
        explanation = job.get('explanation', '')
        if explanation:
            st.info(f"💡 **Why this matches:** {explanation}")
            
        with st.expander("View Details"):
            st.markdown(job.get('description', 'No description provided.'))
            st.markdown(f"🔗 **Apply**: [{job.get('source', 'Link')}]({job.get('url', '#')})")
            
            skills = job.get('skills', [])
            if skills:
                st.markdown("**Required Skills:**")
                st.markdown(", ".join(skills))
        
        st.divider()
