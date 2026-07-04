"""
components/bottom_nav.py
Navigation row linking to the real pages. Unlike the earlier cosmetic
version, these links are functional now that pages/ actually exist.
"""

import streamlit as st


def render_nav(active="Home"):
    st.markdown("<hr class='gd-divider'>", unsafe_allow_html=True)
    cols = st.columns(4)
    items = [
        ("🏠", "Home", "pages/1_Home.py"),
        ("🕘", "History", "pages/2_History.py"),
        ("👤", "Profile", "pages/3_Profile.py"),
        ("⚙️", "Settings", "pages/4_Settings.py"),
    ]
    for col, (icon, label, path) in zip(cols, items):
        with col:
            st.page_link(path, label=f"{icon} {label}", use_container_width=True,
                         disabled=(label == active))
