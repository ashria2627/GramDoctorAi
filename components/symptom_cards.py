
import streamlit as st
from i18n import BANGLA_FEATURES

MANUAL_FIELDS = ["age", "sex-no", "ispregnant"]


def render_symptom_selector(t, language, feature_cols, key="symptom_ms"):
    """Returns (selected_symptoms: dict[str,int], sorted_symptoms: list[str])."""
    symptom_features = [col for col in feature_cols if col not in MANUAL_FIELDS]
    sorted_symptoms = sorted(symptom_features)

    symptom_options = {
        (
            BANGLA_FEATURES.get(symptom, symptom.title())
            if language == "বাংলা"
            else symptom.title()
        ): symptom
        for symptom in sorted_symptoms
    }

    if key not in st.session_state:
        st.session_state[key] = []

    selected_labels = st.multiselect(
        t['search'],
        options=symptom_options.keys(),
        key=key
    )

    selected_symptoms = {
        symptom: symptom in [symptom_options[label] for label in selected_labels]
        for symptom in sorted_symptoms
    }

    return selected_symptoms, sorted_symptoms
