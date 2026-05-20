"""
TEAMS - Tiger-AI Effectiveness Assessment & Monitoring System
Navigation controller — all pages are file-based for reliable path resolution.
"""
import streamlit as st

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
