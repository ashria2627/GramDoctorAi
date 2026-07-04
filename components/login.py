

import streamlit as st
from streamlit_cookies_controller import CookieController

import auth
import database as db

COOKIE_NAME = "gd_session"


@st.cache_resource
def get_controller():
    return CookieController()


def restore_session():
    """Call at the very top of every page (before checking logged_in).
    If a valid session cookie exists, silently re-logs the user in."""
    if st.session_state.get("logged_in"):
        return  # already logged in this run, nothing to do

    controller = get_controller()
    token = controller.get(COOKIE_NAME)
    if not token:
        return

    user = db.get_user_by_session_token(token)
    if user:
        st.session_state.logged_in = True
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.pref_language = user["language"]
        st.session_state.pref_theme = user["theme"]
        st.session_state.pref_font_size = user["font_size"]
        st.session_state.session_token = token


def show_login():
    st.markdown("""
    <div style="text-align:center; margin: 10px 0 20px;">
        <div style="font-size:2.2rem;">🩺</div>
        <div style="font-size:1.4rem; font-weight:800;">GramDoctor AI</div>
        <div style="font-size:0.85rem; opacity:0.75;">Sign in to continue</div>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["Log In", "Register"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)

        if submitted:
            user = auth.verify_user(username, password)
            if user:
                token = db.create_session(user["id"])

                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.session_state.pref_language = user["language"]
                st.session_state.pref_theme = user["theme"]
                st.session_state.pref_font_size = user["font_size"]
                st.session_state.session_token = token

                get_controller().set(COOKIE_NAME, token)
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username", key="reg_username")
            new_password = st.text_input("Choose a password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm")
            reg_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if reg_submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = auth.register_user(new_username, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)


def require_login():
    """Call at the top of every protected page."""
    restore_session()
    if not st.session_state.get("logged_in"):
        st.warning("Please log in to continue.")
        st.switch_page("app.py")
        st.stop()


def logout_button(label="Log out", key="logout_btn"):
    if st.button(label, key=key, use_container_width=True):
        db.delete_session(st.session_state.get("session_token"))
        get_controller().remove(COOKIE_NAME)
        for k in ["logged_in", "user_id", "username", "pref_language", "pref_theme", "pref_font_size", "session_token"]:
            st.session_state.pop(k, None)
        st.rerun()