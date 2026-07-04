"""
components/header.py
App-wide CSS loader, green header banner, and the medical disclaimer banner.
UI only — no backend logic here.
"""

import os
import streamlit as st

_CSS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")


def load_css():
    """Injects assets/style.css once per page render."""
    try:
        with open(_CSS_PATH, "r", encoding="utf-8") as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def render_header(t):
    st.markdown(f"""
    <div class="gd-header">
        <div class="gd-header-logo">🩺</div>
        <div class="gd-header-text">
            <div class="gd-header-title">{t['title']}</div>
            <div class="gd-header-subtitle">{t['subtitle']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_warning_banner(t):
    st.markdown(f'<div class="gd-warning-banner">⚠️ {t["warning"]}</div>', unsafe_allow_html=True)
