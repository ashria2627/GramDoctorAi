
import streamlit as st

import database as db
from components.login import require_login, logout_button
from components.header import load_css, render_header
from components.bottom_nav import render_nav
from i18n import TEXTS

st.set_page_config(page_title="GramDoctor AI — Settings", page_icon="⚙️", layout="centered")

require_login()
load_css(st.session_state.get("pref_theme", "light"))

language = st.session_state.get("language_selector", "English")
t = TEXTS[language]
user = db.get_user_by_username(st.session_state.username)
render_header(t)

with st.sidebar:
    st.caption(f"Logged in as **{st.session_state.get('username', '')}**")
    logout_button()
st.divider()
st.markdown('<div class="gd-card-heading">📧 Email Address</div>', unsafe_allow_html=True)

current_email = user["email"] if user["email"] else None

if current_email:
    st.write(f"Current email: **{current_email}**")
    st.caption("Used for password-reset codes.")

with st.form("set_email_form"):
    new_email = st.text_input(
        "Update email" if current_email else "Add an email (required for password reset)",
        key="settings_email_input"
    )
    email_submitted = st.form_submit_button("Save Email", type="primary", use_container_width=True)

if email_submitted:
    import auth
    success, message = auth.set_email(st.session_state.user_id, new_email)
    (st.success if success else st.error)(message)
st.markdown('<div class="gd-section-title">⚙️ Settings</div>', unsafe_allow_html=True)

user = db.get_user_by_username(st.session_state.username)


st.markdown('<div class="gd-card-heading">🔒 Change Password</div>', unsafe_allow_html=True)
with st.form("change_password_form"):
    old_password = st.text_input("Current password", type="password", key="cp_old")
    new_password = st.text_input("New password", type="password", key="cp_new")
    confirm_new = st.text_input("Confirm new password", type="password", key="cp_confirm")
    cp_submitted = st.form_submit_button("Update Password", type="primary", use_container_width=True)

if cp_submitted:
    if new_password != confirm_new:
        st.error("New passwords do not match.")
    else:
        import auth
        success, message = auth.change_password(st.session_state.user_id, old_password, new_password)
        (st.success if success else st.error)(message)

st.divider()
logout_button(label="Log out", key="profile_logout")
st.caption("GramDoctor AI — v1.0")
st.caption("Theme follows your device/browser setting automatically")
render_nav(active="Settings")
