

import streamlit as st

import database as db
from components.header import load_css
from components.login import show_login, restore_session

st.set_page_config(
    page_title="GramDoctor AI",
    page_icon="🩺",
    layout="centered"
)

db.init_db()
load_css()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
restore_session()
if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")
    st.page_link("pages/1_Home.py", label="🏠 Go to Home / Triage", use_container_width=True)
    st.page_link("pages/2_History.py", label="🕘 View History", use_container_width=True)
    st.page_link("pages/3_Profile.py", label="👤 Profile", use_container_width=True)
    st.page_link("pages/4_Settings.py", label="⚙️ Settings", use_container_width=True)
else:
    show_login()
    st.divider()
    if st.button("👀 Continue as Guest (skip login for demo)", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.user_id = 0
        st.session_state.username = "guest"
        st.switch_page("pages/1_Home.py")

