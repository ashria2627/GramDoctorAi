import streamlit as st
from streamlit_cookies_controller import CookieController

import auth
import database as db

COOKIE_NAME = "gd_session"



def get_controller():
    return CookieController()


def restore_session():
    """Call at the very top of every page (before checking logged_in).
    If a valid session cookie exists, silently re-logs the user in."""
    if st.session_state.get("logged_in"):
        return  # already logged in this run, nothing to do

    controller = get_controller()
    try:
        token = controller.get(COOKIE_NAME)
    except TypeError:
        return  # cookie controller hasn't finished loading yet — try again next rerun

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

def _start_guest_session():
    """No-account demo path. is_guest() checks user_id == 0, so this
    stays consistent with the rest of the app (e.g. history isn't saved)."""
    st.session_state.logged_in = True
    st.session_state.user_id = 0
    st.session_state.username = "Guest"
    st.session_state.pref_language = "English"
    st.session_state.pref_theme = "light"
    st.session_state.pref_font_size = "medium"
    st.session_state.session_token = None
    st.rerun()


def show_login():
    st.markdown("""
    <div style="text-align:center; margin: 10px 0 20px;">
        <div style="font-size:2.2rem;">🩺</div>
        <div style="font-size:1.4rem; font-weight:800;">GramDoctor AI</div>
        <div style="font-size:0.85rem; opacity:0.75;">Sign in to continue</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Try it now — Guest Access (no signup needed)", key="guest_access_btn", type="primary", use_container_width=True):
        _start_guest_session()
    st.caption("Jump straight into a live triage demo — no account required.")
    st.divider()

    if "auth_view" not in st.session_state:
        st.session_state.auth_view = "login"

    tab_login, tab_register = st.tabs(["Log In", "Register"])

    with tab_login:
        if st.session_state.auth_view == "login":
            _render_login_form()
        elif st.session_state.auth_view == "forgot_request":
            _render_forgot_request()
        elif st.session_state.auth_view == "forgot_verify":
            _render_forgot_verify()
        elif st.session_state.auth_view == "forgot_reset":
            _render_forgot_reset()

    with tab_register:
        _render_register_form()


def _render_login_form():
    with st.form("login_form"):
        identifier = st.text_input("Username or Email", key="login_identifier")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Log In", type="primary", use_container_width=True)

    # sits directly below the password field, outside the form
    if st.button("Forgot password?", key="forgot_password_link"):
        st.session_state.auth_view = "forgot_request"
        st.rerun()

    if submitted:
        user = auth.verify_user_by_identifier(identifier, password)
        if user:
            token = db.create_session(user["id"])

            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.username = user["username"]
            st.session_state.pref_language = user["language"]
            st.session_state.pref_theme = user["theme"]
            st.session_state.pref_font_size = user["font_size"]
            st.session_state.session_token = token

            try:
                get_controller().set(COOKIE_NAME, token)
            except TypeError:
                pass

            st.rerun()
        else:
            st.error("Incorrect username/email or password.")


def _render_register_form():
    with st.form("register_form"):
        new_username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm password", type="password", key="reg_confirm")
        reg_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

    if reg_submitted:
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = auth.register_user(new_username, new_email, new_password)
            (st.success if success else st.error)(message)


def _render_forgot_request():
    st.caption("Enter your account email — we'll send you a 6-digit code.")
    with st.form("forgot_request_form"):
        email = st.text_input("Email", key="forgot_email")
        send_submitted = st.form_submit_button("Send Code", type="primary", use_container_width=True)

    if st.button("← Back to Log In", key="back_to_login_1"):
        st.session_state.auth_view = "login"
        st.rerun()

    if send_submitted:
        success, message = auth.request_password_reset(email)
        if success:
            st.session_state.reset_email = email.strip().lower()
            st.session_state.auth_view = "forgot_verify"
            st.rerun()
        else:
            st.error(message)


def _render_forgot_verify():
    st.caption(f"Enter the 6-digit code sent to {st.session_state.get('reset_email', '')}")
    with st.form("forgot_verify_form"):
        code = st.text_input("6-digit code", key="forgot_code")
        verify_submitted = st.form_submit_button("Verify Code", type="primary", use_container_width=True)

    if st.button("← Back", key="back_to_login_2"):
        st.session_state.auth_view = "forgot_request"
        st.rerun()

    if verify_submitted:
        if auth.check_reset_code(st.session_state.reset_email, code.strip()):
            st.session_state.reset_code = code.strip()
            st.session_state.auth_view = "forgot_reset"
            st.rerun()
        else:
            st.error("Invalid or expired code.")


def _render_forgot_reset():
    st.caption("Choose a new password.")
    with st.form("forgot_reset_form"):
        new_password = st.text_input("New password", type="password", key="forgot_new_password")
        confirm_new = st.text_input("Confirm new password", type="password", key="forgot_confirm_password")
        reset_submitted = st.form_submit_button("Set New Password", type="primary", use_container_width=True)

    if reset_submitted:
        if new_password != confirm_new:
            st.error("Passwords do not match.")
        else:
            success, message = auth.reset_password_with_code(
                st.session_state.reset_email, st.session_state.reset_code, new_password
            )
            if success:
                st.success("Password reset successfully. Please log in.")
                for k in ["reset_email", "reset_code"]:
                    st.session_state.pop(k, None)
                st.session_state.auth_view = "login"
                st.rerun()
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
        try:
            get_controller().remove(COOKIE_NAME)
        except KeyError:
            pass 
        for k in ["logged_in", "user_id", "username", "pref_language", "pref_theme", "pref_font_size", "session_token"]:
            st.session_state.pop(k, None)
        st.rerun()

def is_guest():
    return st.session_state.get("user_id") == 0