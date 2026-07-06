

import os
import streamlit as st

_CSS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")


def load_css(theme="system"):
    """theme: 'light', 'dark', or 'system' (falls back to OS/browser preference)."""
    try:
        with open(_CSS_PATH, "r", encoding="utf-8") as f:
            css = "\n".join(line for line in f.read().splitlines() if line.strip() != "")
    except FileNotFoundError:
        return

    if theme == "dark":
        override = """
        <style>
        :root{
            --gd-card-bg: rgba(255,255,255,0.06);
            --gd-card-border: rgba(120,120,120,0.25);
        }
        </style>
        """
    elif theme == "light":
        override = """
        <style>
        :root{
            --gd-card-bg: #FFFFFF;
            --gd-card-border: #E1E8E4;
        }
        </style>
        """
    else:
        override = ""  # leave the existing @media query in style.css to handle "system"

    st.markdown(css + override, unsafe_allow_html=True)


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
