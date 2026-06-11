"""
TEAMS - Tiger-AI Effectiveness Assessment & Monitoring System
Navigation controller — all pages are file-based for reliable path resolution.
"""
import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

# Check if this is a popout request for a fullscreen chart
popout_key = st.query_params.get("popout")
if popout_key:
    st.set_page_config(
        page_title="TEAMS Chart Viewer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # Inject styling to hide all Streamlit structural chrome (header, sidebar, padding)
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            [data-testid="stDecoration"] { display: none !important; }
            .main .block-container { padding: 0 !important; max-width: 100vw !important; }
            iframe { width: 100vw !important; height: 100vh !important; border: none; }
        </style>
    """, unsafe_allow_html=True)
    
    # Read and render the stored HTML file directly (bypassing the static folder MIME issue)
    repo_root = Path(__file__).resolve().parent
    chart_file = repo_root / "static" / "charts" / f"{popout_key}.html"
    
    if chart_file.exists():
        html_content = chart_file.read_text(encoding="utf-8")
        components.html(html_content, height=850, scrolling=False)
    else:
        st.error(f"Chart '{popout_key}' not found.")
    st.stop()

st.set_page_config(
    page_title="TEAMS - Tiger Conservation Dashboard",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="expanded",
)

home_page     = st.Page("pages/home_page.py",            title="Home Page",            default=True)
national_page = st.Page("pages/01_national_overview.py", title="National Overview")
state_page    = st.Page("pages/02_state_explorer.py",    title="State Explorer")
finance_page  = st.Page("pages/03_financial_analysis.py", title="Financial Analysis")
mortality_page= st.Page("pages/04_mortality_conflict.py", title="Mortality & Conflict")

pg = st.navigation({
    "TEAMS": [home_page, national_page, state_page, finance_page, mortality_page]
})

pg.run()
