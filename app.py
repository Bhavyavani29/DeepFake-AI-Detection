"""
DeepSafe — DeepFake Face Detector
Run with: streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from views.shared import inject_global_css, render_navbar, render_footer
from views import home, about, how_it_works, detection, login

load_dotenv()

st.set_page_config(
    page_title="DeepSafe — DeepFake Detector",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()
render_navbar()

if "page" not in st.session_state:
    st.session_state.page = "home"

PAGES = {
    "home": home.render,
    "about": about.render,
    "how": how_it_works.render,
    "detect": detection.render,
    "login": login.render,
}

PAGES.get(st.session_state.page, home.render)()

render_footer()
