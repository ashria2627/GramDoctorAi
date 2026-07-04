"""
pages/4_Settings.py
Lets the user set preferred language / theme / font size.
These are stored in the users table (database.py) and are cosmetic
preferences only — they do not touch triage/ML logic.
"""

import streamlit as st

import database as db
from components.login import require_login, logout_button
from components.header import load_css, render_header
from components.bottom_nav import render_nav
from i18n import TEXTS

st.set_page_config(page_title="GramDoctor AI — Settings", page_icon="⚙️", layout="centered")

require_login()
load_css()

language = st.session_state.get("language_selector", "English")
t = TEXTS[language]

render_header(t)

with st.sidebar:
    st.caption(f"Logged in as **{st.session_state.get('username', '')}**")
    logout_button()

st.markdown('<div class="gd-section-title">⚙️ Settings</div>', unsafe_allow_html=True)

user = db.get_user_by_username(st.session_state.username)

pref_language = st.selectbox("Preferred language", ["English", "বাংলা"],
                              index=0 if user["language"] == "English" else 1)
pref_theme = st.selectbox("Theme", ["Follow system", "Light", "Dark"],
                           index=["Follow system", "Light", "Dark"].index(
                               {"light": "Light", "dark": "Dark"}.get(user["theme"], "Follow system")
                           ))
pref_font = st.selectbox("Font size", ["Normal", "Large"],
                          index=0 if user["font_size"] != "large" else 1)

st.caption("Theme follows your device/browser setting automatically — 'Light'/'Dark' here is saved as your preference for future updates to this feature.")

if st.button("Save Settings", type="primary", use_container_width=True):
    db.update_user_preferences(
        st.session_state.user_id,
        language=pref_language,
        theme=pref_theme.lower(),
        font_size=pref_font.lower(),
    )
    st.session_state.pref_language = pref_language
    st.success("Settings saved.")

st.divider()
st.caption("GramDoctor AI — v1.0")

render_nav(active="Settings")
