import streamlit as st
from src.dashboard.client.api_client import JobPulseApiClient
from src.dashboard.components.error_ux import handle_api_error
import os

st.title("🗺️ Market Discovery")
st.markdown("Discover emergent job clusters and macro-market trends.")

client = JobPulseApiClient()

try:
    with st.spinner("Fetching market discovery data..."):
        response = client.get_market_report()
        data = response.get("data", {})

    st.subheader("Emergent Clusters")
    clusters = data.get("clusters", [])
    
    if not clusters:
        st.info("No clusters available yet. Run the discovery pipeline from the Home page.")
    else:
        for cluster in clusters:
            st.markdown(f"### Cluster {cluster.get('cluster_id')}")
            col1, col2 = st.columns(2)
            col1.metric("Job Count", cluster.get("size", 0))
            col2.metric("Median Salary", f"${cluster.get('median_salary', 0):,}")
            
            st.markdown("**Top Skills:** " + ", ".join(cluster.get("top_skills", [])))
            st.divider()

    st.subheader("Market Visualization (UMAP)")
    st.markdown("Pre-rendered UMAP projection from the latest pipeline run. This avoids heavy re-computations inside the UI client.")
    
    artifact_path = "artifacts/umap_clusters.png"
    if os.path.exists(artifact_path):
        st.image(artifact_path, caption="Semantic Market Clusters", use_container_width=True)
    else:
        st.warning(f"UMAP artifact not found at `{artifact_path}`. Please run the Intelligence Pipeline to generate the visualization.")

except Exception as e:
    handle_api_error(e)
