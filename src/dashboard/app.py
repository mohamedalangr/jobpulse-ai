import streamlit as st
from src.dashboard.state import init_state

st.set_page_config(
    page_title="JobPulse AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
init_state()

# Navigation definition
pages = {
    "Operations": [
        st.Page("pages/home.py", title="Dashboard Home", icon="🏠"),
        st.Page("pages/developer.py", title="Developer & System", icon="⚙️")
    ],
    "Intelligence": [
        st.Page("pages/search.py", title="Semantic Search", icon="🔍"),
        st.Page("pages/career.py", title="Career Intelligence", icon="📈"),
        st.Page("pages/learning.py", title="Learning Intelligence", icon="📚"),
        st.Page("pages/market.py", title="Market Discovery", icon="🗺️")
    ]
}

pg = st.navigation(pages)
pg.run()
