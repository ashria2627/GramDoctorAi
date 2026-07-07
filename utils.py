

import re
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from gtts import gTTS
import streamlit as st
from modules.symptom_normalizer import normalize_symptom_input
from i18n import BANGLA_FEATURES, EXTRA_DISPLAY_SYMPTOMS
from components.result_card import normalize_color, get_active_symptom_keys, format_prediction_driver
from modules.text_negation import is_symptom_negated

def extract_english_symptoms(text, feature_cols):
    return normalize_symptom_input(text, feature_cols)


from modules.text_negation import is_symptom_negated

def detect_extra_display_symptoms(text):
    if not text:
        return []

    lowered = text.lower()
    found = []
    for symptom, info in EXTRA_DISPLAY_SYMPTOMS.items():
        for term in info["terms"]:
            term_text = term.lower().strip()
            if not term_text:
                continue
            pattern = rf"(?<![a-z0-9]){re.escape(term_text)}(?![a-z0-9])"
            if re.search(pattern, lowered) and not is_symptom_negated(lowered, term_text):
                found.append(symptom)
                break
    return found



def create_gray_result(language):
    if language == "বাংলা":
        message = "ইনপুট থেকে কোনো পরিচিত লক্ষণ পাওয়া যায়নি। ব্যবহারকারী সম্ভবত অন্য কিছু বোঝাতে চেয়েছেন।"
    else:
        message = "No recognized symptom was found in the input. The user may be trying to describe something else."

    return {
        "color": "gray",
        "source": "Input validation",
        "message": message,
        "confidence": None
    }


def wrap_text(text, max_chars=90):
    lines = []

    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()

        if not paragraph:
            lines.append("")
            continue

        while len(paragraph) > max_chars:
            split_at = paragraph.rfind(" ", 0, max_chars)

            if split_at == -1:
                split_at = max_chars

            lines.append(paragraph[:split_at])
            paragraph = paragraph[split_at:].strip()

        lines.append(paragraph)

    return lines


def extract_english_referral_note(ai_response):
    if not ai_response:
        return "No referral note generated."

    markers = [
        "Referral Note English:",
        "English Referral Note:",
        "Referral Note:"
    ]

    for marker in markers:
        if marker in ai_response:
            note = ai_response.split(marker, 1)[1].strip()

            stop_markers = [
                "Referral Note Bangla:",
                "Bangla Referral Note:",
                "Bangla Explanation:",
                "Immediate Advice:",
                "What Not To Do:"
            ]

            for stop_marker in stop_markers:
                if stop_marker in note:
                    note = note.split(stop_marker, 1)[0].strip()

            return note

    return ai_response


def create_structured_referral_pdf(ai_response, triage_result, symptoms, referral=None, first_aid=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    def ensure_space(required=60):
        nonlocal y
        if y < required:
            pdf.showPage()
            y = height - 50

    def section(title):
        nonlocal y
        ensure_space(80)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, title)
        y -= 18
        pdf.setFont("Helvetica", 10)

    def write_lines(lines, left=60, max_chars=90):
        nonlocal y
        if isinstance(lines, str):
            lines = [lines]
        for item in lines:
            for line in wrap_text(str(item), max_chars=max_chars):
                ensure_space()
                pdf.drawString(left, y, line)
                y -= 13

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "GramDoctor AI - Structured Referral Report")
    y -= 30

    section("Patient Info")
    sex_label = {0: "Male", 1: "Female"}.get(symptoms.get("sex-no"), "Unknown")
    pregnancy_label = {0: "No", 1: "Yes", 2: "N/A"}.get(symptoms.get("ispregnant"), "Unknown")
    write_lines([
        f"Age: {symptoms.get('age', 'unknown')}",
        f"Sex: {sex_label}",
        f"Pregnancy: {pregnancy_label}",
    ])

    active_symptoms = [
        symptom
        for symptom, value in symptoms.items()
        if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
    ]

    section("Symptoms Detected")
    write_lines([f"- {symptom}" for symptom in active_symptoms[:25]] or "- No specific symptom detected")

    section("Triage Level and Reasoning")
    write_lines([
        f"Triage Level: {triage_result.get('color', 'unknown').upper()}",
        f"Decision Source: {triage_result.get('source', 'unknown')}",
        f"Reason: {triage_result.get('message', '')}",
    ])

    section("Confidence Score")
    confidence = triage_result.get("confidence")
    if confidence is None:
        write_lines("Rule-based decision; model confidence not applicable.")
    else:
        write_lines(f"Model Confidence: {confidence}%")


    section("Recommended Specialist")
    write_lines(referral or "General Physician")
   

    section("Follow-up Advice")
    write_lines(extract_english_referral_note(ai_response))

    ensure_space(80)
    pdf.setFont("Helvetica-Oblique", 9)
    disclaimer = (
        "Disclaimer: This tool does not provide a final diagnosis. "
        "It supports triage and referral guidance only."
    )
    write_lines(disclaimer, left=50, max_chars=95)

    pdf.save()
    buffer.seek(0)
    return buffer


def get_tts_summary_bangla(triage_result, symptoms, referral, alternate_referral=None):
    color = normalize_color(triage_result.get("color", "gray"))
    active = get_active_symptom_keys(symptoms)

    bangla_color = {
        "green": "গ্রিন",
        "orange": "অরেঞ্জ",
        "red": "রেড",
        "gray": "গ্রে",
    }.get(color, "গ্রে")

    bangla_action = {
        "green": "বাসায় বিশ্রাম নিন এবং লক্ষণ পর্যবেক্ষণ করুন।",
        "orange": "এক থেকে দুই দিনের মধ্যে ডাক্তার দেখান।",
        "red": "এখনই জরুরি বিভাগে যান।",
        "gray": "স্পষ্ট করে লক্ষণ লিখুন বা বলুন।",
    }.get(color, "স্পষ্ট করে লক্ষণ লিখুন বা বলুন।")

    symptom_items = []

    if active:
        symptom_items.extend([BANGLA_FEATURES.get(s, s) for s in active[:6]])

    for extra_symptom in st.session_state.get("extra_symptoms", []):
        symptom_items.append(BANGLA_FEATURES.get(extra_symptom, extra_symptom.replace("_", " ")))

    if symptom_items:
        symptom_text = ", ".join(symptom_items[:8])
    else:
        symptom_text = "কোনো নির্দিষ্ট লক্ষণ পাওয়া যায়নি"

    summary = (
        f"আপনার ট্রায়াজ ফলাফল {bangla_color}. "
        f"সনাক্ত হওয়া লক্ষণ: {symptom_text}. "
    
    )

    if referral:
        summary += f"রেফার করুন: {referral}. "

    if alternate_referral:
        summary += f"না পেলে বিকল্প হিসেবে দেখান: {alternate_referral}. "

    summary += bangla_action

    return summary


def create_tts_audio(text):
    buffer = BytesIO()
    tts = gTTS(text=text, lang="bn")
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer
