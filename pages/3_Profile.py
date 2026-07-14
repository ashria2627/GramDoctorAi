import streamlit as st

import database as db
from components.login import require_login, logout_button, is_guest
from components.header import load_css, render_header
from components.bottom_nav import render_nav
from i18n import TEXTS

st.set_page_config(page_title="GramDoctor AI — Profile", page_icon="👤", layout="centered")

require_login()
load_css(st.session_state.get("pref_theme", "light"))

language = st.session_state.get("language_selector", "English")
t = TEXTS[language]

render_header(t)

with st.sidebar:
    st.caption(f"Logged in as **{st.session_state.get('username', '')}**")
    logout_button()

st.markdown('<div class="gd-section-title">👤 Profile</div>', unsafe_allow_html=True)

if is_guest():
    st.info("👀 You're in Guest Mode — profile info isn't tracked. Register for a real account to save your data across sessions."if language=="English" else "👀 আপনি গেস্ট মোডে আছেন — প্রোফাইলের তথ্য ট্র্যাক করা হয় না। বিভিন্ন সেশনে আপনার ডেটা সংরক্ষণ করতে একটি আসল অ্যাকাউন্টের জন্য নিবন্ধন করুন।")
else:
    user = db.get_user_by_username(st.session_state.username)
    history_count = len(db.get_history_for_user(st.session_state.user_id, limit=1000))

    st.markdown(f"""
    <div class="gd-recommend-card">
    <b>Username:</b> {user['username']}<br>
    <b>Email:</b> {user['email'] if user['email'] else 'N/A'}<br>
    <b>Member since:</b> {user['created_at'][:10]}<br>
    <b>Preferred language:</b> {user['language']}<br>
    <b>Triage sessions logged:</b> {history_count}
    </div>
    """, unsafe_allow_html=True)

st.divider()
logout_button(label="Log out", key="profile_logout")

render_nav(active="Profile")