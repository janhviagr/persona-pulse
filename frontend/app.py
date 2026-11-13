import streamlit as st

from theme import apply_theme

st.set_page_config(
    page_title="PersonaPulse | Synthetic Consumer Intelligence",
    page_icon=":material/hub:",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
st.logo("frontend/assets/personapulse-brand.svg", size="large")

pages = [
    st.Page("pages/0_Overview.py", title="Overview", icon=":material/home:", url_path="", default=True),
    st.Page("pages/1_Product_Submission.py", title="Product Submission", icon=":material/package_2:", url_path="product-submission"),
    st.Page("pages/2_Persona_Generation.py", title="Persona Generation", icon=":material/groups:", url_path="personas"),
    st.Page("pages/3_Simulation.py", title="Simulation", icon=":material/hub:", url_path="simulation"),
    st.Page("pages/4_Analytics.py", title="Analytics", icon=":material/monitoring:", url_path="analytics"),
]
navigation = st.navigation(pages, position="sidebar")
navigation.run()
