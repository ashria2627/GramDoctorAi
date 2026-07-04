

import streamlit as st


def render_confidence(confidence, language):
    if confidence is None:
        return
    st.progress(min(max(float(confidence) / 100, 0), 1), text=f"Model Confidence: {confidence}%")
    if confidence < 60:
        st.warning(
            "Low confidence - please consult a doctor."
            if language == "English"
            else "Low confidence - অনুগ্রহ করে ডাক্তারের পরামর্শ নিন। "
        )
