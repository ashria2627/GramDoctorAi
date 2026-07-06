

import os
import json
import streamlit as st
from components.result_card import normalize_color, get_active_symptom_keys, get_symptom_display
from modules.doctor_finder import find_doctors, google_search_url

SPECIALIST_LABELS = {
    "General Physician": {"English": "General Physician", "বাংলা": "জেনারেল ফিজিশিয়ান"},
    "Cardiologist": {"English": "Cardiologist", "বাংলা": "কার্ডিওলজিস্ট / হৃদরোগ বিশেষজ্ঞ"},
    "Neurologist": {"English": "Neurologist", "বাংলা": "নিউরোলজিস্ট / স্নায়ুরোগ বিশেষজ্ঞ"},
    "Pulmonologist": {"English": "Pulmonologist", "বাংলা": "পালমোনোলজিস্ট / বক্ষব্যাধি বিশেষজ্ঞ"},
    "Gastroenterologist": {"English": "Gastroenterologist", "বাংলা": "পরিপাকতন্ত্র বিশেষজ্ঞ"},
    "Urologist": {"English": "Urologist", "বাংলা": "ইউরোলজিস্ট / মূত্ররোগ বিশেষজ্ঞ"},
    "Nephrologist": {"English": "Nephrologist", "বাংলা": "নেফ্রোলজিস্ট / কিডনি বিশেষজ্ঞ"},
    "Endocrinologist": {"English": "Endocrinologist", "বাংলা": "এন্ডোক্রাইনোলজিস্ট / হরমোন ও ডায়াবেটিস বিশেষজ্ঞ"},
    "Dermatologist": {"English": "Dermatologist", "বাংলা": "ডার্মাটোলজিস্ট / চর্মরোগ বিশেষজ্ঞ"},
    "ENT Specialist": {"English": "ENT Specialist", "বাংলা": "নাক-কান-গলা বিশেষজ্ঞ"},
    "Ophthalmologist": {"English": "Ophthalmologist", "বাংলা": "চক্ষু বিশেষজ্ঞ"},
    "Dentist": {"English": "Dentist", "বাংলা": "দন্ত চিকিৎসক"},
    "Gynecologist": {"English": "Gynecologist / Obstetrician", "বাংলা": "প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ"},
    "Pediatrician": {"English": "Pediatrician", "বাংলা": "শিশু বিশেষজ্ঞ"},
    "Orthopedic Specialist": {"English": "Orthopedic Specialist", "বাংলা": "হাড়-জোড়া বিশেষজ্ঞ"},
    "Psychiatrist": {"English": "Psychiatrist", "বাংলা": "মানসিক রোগ বিশেষজ্ঞ"},
    "General Surgeon": {"English": "General Surgeon", "বাংলা": "জেনারেল সার্জন"},
}

SPECIALIST_LANGUAGE_ALIASES = {
    "English": "English",
    "বাংলা": "বাংলা",
}



def specialist_label(name, language):
    normalized_language = SPECIALIST_LANGUAGE_ALIASES.get(language, "English")
    labels = SPECIALIST_LABELS.get(name, SPECIALIST_LABELS["General Physician"])
    return labels.get(normalized_language, labels["English"])


def cluster_priority_resolver(scored_clusters, active_symptoms):
    if not scored_clusters:
        return None

    ent_symptoms = {"sore throat", "ear pain", "diminished hearing", "ringing in ear", "nasal congestion", "runny nose", "hoarse voice", "snoring", "sleep apnea"}
    respiratory_danger_context = {"shortness of breath", "wheezing", "hemoptysis", "coughing up sputum"}
    gynecology_priority = {"painful menstruation", "heavy menstrual flow", "irregular periods", "spotting or bleeding during pregnancy", "vaginal discharge", "vaginal pain", "pelvic pain"}

    ent_count = len(active_symptoms.intersection(ent_symptoms))
    respiratory_context_count = len(active_symptoms.intersection(respiratory_danger_context))

    for row in scored_clusters:
        if row["cluster"] == "ENT" and ent_count >= 3 and respiratory_context_count == 0:
            row["score"] += 4
            row["reason"] = "ENT majority resolved over isolated breathing symptom"
        if row["cluster"] == "Gynecology" and active_symptoms.intersection(gynecology_priority):
            row["score"] += 3
            row["reason"] = "Gynecology-specific symptom resolved mixed complaint"

    scored_clusters.sort(
        key=lambda row: (
            row["score"],
            row.get("priority_matched", 0),
            row["matched"],
            row["red_matched"],
            row["cluster"] in {"Gynecology", "Urology", "Ophthalmology", "ENT", "Orthopedics"},
        ),
        reverse=True,
    )
    return scored_clusters[0]


@st.cache_data
def load_specialist_lookup():
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modules", "specialist_lookup.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_specialist_concerns(symptoms):
    active = set(get_active_symptom_keys(symptoms))
    lookup = load_specialist_lookup()
    concerns = []
    generic_low_specificity = {"headache", "weakness", "dizziness", "nausea", "vomiting", "fatigue", "cough"}

    for cluster, info in lookup.items():
        matched = active.intersection(set(info.get("symptoms", [])))
        red_matched = active.intersection(set(info.get("red_flags", [])))
        priority_matched = active.intersection(set(info.get("priority_symptoms", [])))
        if not matched:
            continue

        generic_only_penalty = 0.5 if matched.issubset(generic_low_specificity) and not red_matched else 0
        concerns.append({
            "cluster": cluster,
            "specialist": info["specialist"],
            "score": len(matched) + (5 * len(red_matched)) + (2 * len(priority_matched)) - generic_only_penalty,
            "matched": len(matched),
            "priority_matched": len(priority_matched),
            "red_matched": len(red_matched),
            "symptoms": sorted(matched),
        })

    selected = cluster_priority_resolver(concerns, active)
    concerns.sort(
        key=lambda row: (
            row["score"],
            row.get("priority_matched", 0),
            row["matched"],
            row["red_matched"],
        ),
        reverse=True,
    )

    if selected:
        concerns = [selected] + [
            row for row in concerns
            if row["cluster"] != selected["cluster"]
        ]

    return concerns


def format_additional_concerns(symptoms, language, primary_specialist=None, limit=3):
    concerns = build_specialist_concerns(symptoms)
    lines = []
    primary_plain = str(primary_specialist or "").replace("Emergency ", "")
    active_count = len(get_active_symptom_keys(symptoms))
    minimum_secondary_score = 1 if active_count >= 4 else 1.5

    for concern in concerns:
        label = specialist_label(concern["specialist"], language)
        if primary_plain and label == primary_plain:
            continue
        if concern["cluster"] == "Orthopedics" and concern["matched"] < 2:
            continue
        if concern["score"] < minimum_secondary_score and concern.get("priority_matched", 0) == 0:
            continue

        symptom_text = ", ".join(
            get_symptom_display(symptom, language)
            for symptom in concern["symptoms"][:4]
        )
        if language == "English":
            lines.append(f"{label}: possible {concern['cluster']} concern ({symptom_text})")
        else:
            lines.append(f"{label}: সম্ভাব্য {concern['cluster']} সমস্যা ({symptom_text})")

        if len(lines) >= limit:
            break

    return lines


def get_specialist_referral_clustered(triage_result, symptoms, language):
    color = normalize_color(triage_result.get("color", "gray"))
    active = set(get_active_symptom_keys(symptoms))

    if color == "green":
        return None, None, None

    source = str(triage_result.get("source", "")).lower()
    if "pcos" in source or "hormonal disorder" in source:
        return specialist_label("Gynecologist", language), specialist_label("General Physician", language), "Gynecologist"

    scored = build_specialist_concerns(symptoms)

    if not scored:
        if symptoms.get("ispregnant", 2) == 1:
            return specialist_label("Gynecologist", language), specialist_label("General Physician", language), "Gynecologist"
        if symptoms.get("age", 30) < 13:
            return specialist_label("Pediatrician", language), specialist_label("General Physician", language), "Pediatrician"
        return specialist_label("General Physician", language), None, "General Physician"

    selected = scored[0]
    specialist_name = selected["specialist"]
    emergency_note = ""

    true_emergency = color == "red" and selected["red_matched"] > 0
    if true_emergency:
        emergency_note = "Emergency " if language == "English" else "জরুরি অবস্থা "

    if symptoms.get("ispregnant", 2) == 1 and selected["score"] <= 1:
        specialist_name = "Gynecologist"
    elif symptoms.get("age", 30) < 13 and selected["score"] <= 1:
        specialist_name = "Pediatrician"

    return emergency_note + specialist_label(specialist_name, language), specialist_label("General Physician", language), specialist_name

def render_recommendation_card(text):
    """UI helper: same visual card style used across the app."""
    st.markdown(f'<div class="gd-recommend-card">{text}</div>', unsafe_allow_html=True)


def render_doctor_suggestions(specialist_name, language):
    doctors = find_doctors(specialist_name, language, limit=5)
    if not doctors:
        return

    heading = "👨‍⚕️Some Recommended Specialists" if language == "English" else "👨‍⚕️ কিছু প্রস্তাবিত বিশেষজ্ঞ"
    st.markdown(f'<div class="gd-card-heading">{heading}</div>', unsafe_allow_html=True)

    for doc in doctors:
        st.markdown(f"""
        <div class="gd-recommend-card">
            <a href="{doc['profile_url']}" target="_blank" style="text-decoration:none;font-weight:700;">{doc['name']}</a><br>
            <small>{doc['hospital']} — {doc['speciality']}</small>
        </div>
        """, unsafe_allow_html=True)

    search_label = "🔍 See more nearby" if language == "English" else "🔍 আরও দেখুন"
    st.markdown(f'<a href="{google_search_url(specialist_name)}" target="_blank">{search_label}</a>', unsafe_allow_html=True)