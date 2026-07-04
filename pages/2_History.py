"""
pages/2_History.py
Displays past triage sessions for the logged-in user.
Reads only from database.py (new file) — never touches the ML/triage backend.
"""

import json
import streamlit as st

import database as db
from components.login import require_login, logout_button
from components.header import load_css, render_header
from components.bottom_nav import render_nav
from i18n import TEXTS

st.set_page_config(page_title="GramDoctor AI — History", page_icon="🕘", layout="centered")

require_login()
load_css()

language = st.session_state.get("language_selector", "English")
t = TEXTS[language]

render_header(t)

with st.sidebar:
    st.caption(f"Logged in as **{st.session_state.get('username', '')}**")
    logout_button()

st.markdown('<div class="gd-section-title">🕘 Your Triage History</div>', unsafe_allow_html=True)

rows = db.get_history_for_user(st.session_state.user_id)

if not rows:
    st.info("No past triage sessions yet. Results are logged automatically once you complete a triage on the Home page.")
else:
    color_icon = {"green": "🟢", "orange": "🟠", "red": "🔴", "gray": "⚪"}
    for row in rows:
        icon = color_icon.get(row["triage_color"], "⚪")
        title = f"{icon} {row['created_at'][:16].replace('T', ' ')} — {(row['triage_color'] or 'unknown').upper()}"
        with st.expander(title):
            st.write(f"**Language:** {row['language']}")
            st.write(f"**Decision source:** {row['decision_source']}")
            st.write(f"**Message:** {row['message']}")
            if row["confidence"] is not None:
                st.write(f"**Confidence:** {row['confidence']}%")
            if row["referral"]:
                st.write(f"**Referred to:** {row['referral']}")
            if row["alternate_referral"]:
                st.write(f"**Alternate:** {row['alternate_referral']}")

            try:
                active = json.loads(row["active_symptoms_json"] or "[]")
            except Exception:
                active = []
            if active:
                st.write("**Symptoms:**", ", ".join(active))

            try:
                followups = json.loads(row["followup_answers_json"] or "{}")
            except Exception:
                followups = {}
            answered = {k: v for k, v in followups.items() if v}
            if answered:
                st.write("**Follow-up answers:**")
                for k, v in answered.items():
                    st.write(f"- {v}")

            if row["ai_response"]:
                st.write("**AI referral note:**")
                st.markdown(row["ai_response"])

            if st.button("Delete this entry", key=f"del_{row['id']}"):
                db.delete_history_entry(row["id"], st.session_state.user_id)
                st.rerun()

render_nav(active="History")
