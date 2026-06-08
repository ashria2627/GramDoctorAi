import os
from io import BytesIO

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from modules.model_backend import load_model_and_features, predict_triage
from modules.BanglaSymptoms import extract_bangla_symptoms
from modules.gemini_helper import generate_ai_response

try:
    from streamlit_mic_recorder import speech_to_text
except Exception:
    speech_to_text = None


st.set_page_config(
    page_title="GramDoctor AI",
    page_icon="🩺",
    layout="centered"
)


TEXTS = {
    "English": {
        "title": "GramDoctor AI",
        "subtitle": "Bangla AI Triage and Referral Assistant",
        "warning": (
            "This tool does not provide a final diagnosis. "
            "It only gives triage guidance. "
            "For emergency symptoms, seek immediate medical care."
        ),
        "sidebar_title": "How to Use",
        "sidebar_help": """
1. Select language from the top dropdown.
2. Enter patient age, sex, and pregnancy status.
3. Type symptoms in Bangla or English.
4. Optionally upload a text note.
5. Use voice input if needed.
6. Select symptoms manually if needed.
7. Click Check Triage.
8. Open the Result tab.
9. Generate AI explanation and referral note.
10. Download the referral note as PDF.
""",
        "demo_title": "Demo Cases",
        "demo_cases": """
**Green case:**  
cough, blocked nose

**Orange case:**  
fever, vomiting, weakness

**Red case:**  
chest pain, sweating, shortness of breath

**Gray case:**  
today the weather is good
""",
        "tab_form": "Patient Form",
        "tab_result": "Result",
        "patient_info": "Patient Information",
        "age": "Age",
        "sex": "Sex",
        "male": "Male",
        "female": "Female",
        "pregnancy": "Pregnancy Status",
        "not_applicable": "Not applicable",
        "no": "No",
        "yes": "Yes",
        "text_input": "Describe symptoms in Bangla or English",
        "text_placeholder": "Example: fever, vomiting, headache or আমার জ্বর, বমি, মাথা ব্যথা হচ্ছে",
        "upload_note": "Optional: Upload patient symptom note",
        "uploaded_preview": "Uploaded note preview",
        "voice_input": "Voice input",
        "voice_help": "Click the microphone and speak symptoms. Works best in Chrome.",
        "voice_unavailable": "Voice input package not installed or unavailable.",
        "clear_voice": "Clear voice text",
        "symptoms": "Symptoms",
        "check_triage": "Check Triage",
        "triage_done": "Triage completed. Open the Result tab.",
        "triage_result": "Triage Result",
        "no_result": "No result yet. Fill the patient form first.",
        "decision_source": "Decision source:",
        "reason": "Reason:",
        "detected_symptoms": "Detected Symptoms",
        "no_symptoms": "No specific symptom detected from the current input.",
        "generate_ai": "Generate AI Explanation",
        "generating": "Generating AI explanation...",
        "ai_title": "AI Explanation and Referral Note",
        "download_pdf": "Download Referral Note PDF",
        "pdf_filename": "gramdoctor_referral_note.pdf",
    },
    "বাংলা": {
        "title": "GramDoctor AI",
        "subtitle": "বাংলা AI ট্রায়াজ ও রেফারেল সহকারী",
        "warning": (
            "এই টুল চূড়ান্ত রোগ নির্ণয় করে না। "
            "এটি শুধু প্রাথমিক ট্রায়াজ ও রেফারেল গাইডেন্স দেয়। "
            "জরুরি লক্ষণ থাকলে দ্রুত চিকিৎসা নিন।"
        ),
        "sidebar_title": "ব্যবহার করার নিয়ম",
        "sidebar_help": """
১. উপরের ড্রপডাউন থেকে ভাষা নির্বাচন করুন।
২. রোগীর বয়স, লিঙ্গ এবং গর্ভাবস্থার তথ্য দিন।
৩. বাংলা বা ইংরেজিতে লক্ষণ লিখুন।
৪. চাইলে টেক্সট নোট আপলোড করুন।
৫. প্রয়োজন হলে ভয়েস ইনপুট ব্যবহার করুন।
৬. চাইলে ম্যানুয়ালি লক্ষণ সিলেক্ট করুন।
৭. ট্রায়াজ চেক করুন।
৮. Result ট্যাবে ফলাফল দেখুন।
৯. AI explanation ও referral note তৈরি করুন।
১০. Referral note PDF হিসেবে ডাউনলোড করুন।
""",
        "demo_title": "ডেমো কেস",
        "demo_cases": """
**Green case:**  
কাশি, নাক বন্ধ

**Orange case:**  
জ্বর, বমি, দুর্বলতা

**Red case:**  
বুকে তীব্র ব্যথা, ঘাম, শ্বাসকষ্ট

**Gray case:**  
আজ আবহাওয়া ভালো
""",
        "tab_form": "রোগীর ফর্ম",
        "tab_result": "ফলাফল",
        "patient_info": "রোগীর তথ্য",
        "age": "বয়স",
        "sex": "লিঙ্গ",
        "male": "পুরুষ",
        "female": "নারী",
        "pregnancy": "গর্ভাবস্থার অবস্থা",
        "not_applicable": "প্রযোজ্য নয়",
        "no": "না",
        "yes": "হ্যাঁ",
        "text_input": "বাংলা বা ইংরেজিতে লক্ষণ লিখুন",
        "text_placeholder": "যেমন: আমার জ্বর, বমি, মাথা ব্যথা হচ্ছে",
        "upload_note": "ঐচ্ছিক: রোগীর লক্ষণের টেক্সট নোট আপলোড করুন",
        "uploaded_preview": "আপলোড করা নোট প্রিভিউ",
        "voice_input": "ভয়েস ইনপুট",
        "voice_help": "মাইক্রোফোনে ক্লিক করে লক্ষণ বলুন। Chrome ব্রাউজারে ভালো কাজ করে।",
        "voice_unavailable": "Voice input package ইনস্টল নেই অথবা কাজ করছে না।",
        "clear_voice": "ভয়েস টেক্সট মুছে ফেলুন",
        "symptoms": "লক্ষণসমূহ",
        "check_triage": "ট্রায়াজ চেক করুন",
        "triage_done": "ট্রায়াজ সম্পন্ন হয়েছে। Result ট্যাবে যান।",
        "triage_result": "ট্রায়াজ ফলাফল",
        "no_result": "এখনো কোনো ফলাফল নেই। আগে রোগীর ফর্ম পূরণ করুন।",
        "decision_source": "সিদ্ধান্তের উৎস:",
        "reason": "কারণ:",
        "detected_symptoms": "সনাক্ত হওয়া লক্ষণ",
        "no_symptoms": "বর্তমান ইনপুট থেকে নির্দিষ্ট কোনো লক্ষণ পাওয়া যায়নি।",
        "generate_ai": "AI ব্যাখ্যা তৈরি করুন",
        "generating": "AI ব্যাখ্যা তৈরি হচ্ছে...",
        "ai_title": "AI ব্যাখ্যা ও রেফারেল নোট",
        "download_pdf": "Referral Note PDF ডাউনলোড করুন",
        "pdf_filename": "gramdoctor_referral_note.pdf",
    }
}


def show_triage_card(color, language):
    if color == "green":
        if language == "বাংলা":
            st.success("GREEN — বাসায় পর্যবেক্ষণ")
            st.markdown("""
            **অর্থ:** বর্তমান তথ্য অনুযায়ী লক্ষণগুলো কম ঝুঁকিপূর্ণ মনে হচ্ছে। 
             
            **করণীয়:** বিশ্রাম, পর্যাপ্ত পানি এবং লক্ষণ পর্যবেক্ষণ।  
            
            **চিকিৎসা নিন যদি:** লক্ষণ বাড়ে, জ্বর থাকে, বা বিপদ সংকেত দেখা যায়।
            """)
        else:
            st.success("GREEN — Home care / observe")
            st.markdown("""
            **Meaning:** Current symptoms appear low risk based on triage input. 
             
            **Recommended action:** Rest, drink fluids, and monitor symptoms.  
            
            **Seek care if:** symptoms worsen, fever persists, or danger signs appear.
            """)

    elif color == "orange":
        if language == "বাংলা":
            st.warning("পর্যবেক্ষণে রাখুন। উপসর্গ বেড়ে গেলে বা অবস্থার অবনতি হলে ১–২ দিনের মধ্যে চিকিৎসকের পরামর্শ নিন।")
            st.markdown("""
            **অর্থ:** লক্ষণগুলো চিকিৎসকের মূল্যায়ন প্রয়োজন হতে পারে।  
            
            **করণীয়:** ২৪-৪৮ ঘণ্টার মধ্যে ডাক্তার, ক্লিনিক বা উপজেলা স্বাস্থ্য কমপ্লেক্সে যান। 
             
            **জরুরি চিকিৎসা নিন যদি:** দুর্বলতা, পানিশূন্যতা, তীব্র ব্যথা বা শ্বাসকষ্ট বাড়ে।
            """)
        else:
            st.warning("ORANGE — Observe and if worsen Visit doctor within 1-2 days")
            st.markdown("""
            **Meaning:** Symptoms need medical review but may not be an immediate emergency.  
            
            **Recommended action:** Visit a local doctor, clinic, or Upazila Health Complex within 24-48 hours.  
            **Seek urgent care if:** weakness, dehydration, severe pain, or breathing difficulty worsens.
            """)

    elif color == "red":
        if language == "বাংলা":
            st.error("RED — এখনই জরুরি চিকিৎসা নিন")
            st.markdown("""
            **অর্থ:** জরুরি বিপদ সংকেত থাকতে পারে।
              
            **করণীয়:** এখনই নিকটস্থ হাসপাতাল বা জরুরি বিভাগে যান।  
            
            **করবেন না:** বাসায় অপেক্ষা করবেন না বা চিকিৎসা নিতে দেরি করবেন না।
            """)
        else:
            st.error("RED — Emergency care now")
            st.markdown("""
            **Meaning:** Emergency red-flag silent symptoms may be present. 
             
            **Recommended action:** Go to the nearest emergency department immediately. 
             
            **Do not:** wait at home or delay medical care.
            """)

    elif color == "gray":
        if language == "বাংলা":
            st.info("GRAY — লক্ষণ বোঝা যায়নি")
            st.markdown("""
            আপনি কি কোনো লক্ষণ বোঝাতে চেয়েছেন?  
            
            অনুগ্রহ করে স্পষ্টভাবে লক্ষণ লিখুন বা বলুন, যেমন: জ্বর, বমি, কাশি, শ্বাসকষ্ট।
            """)
        else:
            st.info("GRAY — Symptom unclear")
            st.markdown("""
            No recognized symptom was detected from the input.  
             
            Are you trying to describe a symptom?  
            
            Please write or speak symptoms clearly, for example: fever, vomiting, cough, shortness of breath.
            """)

    else:
        st.info(f"Unknown triage result: {color}")


def extract_english_symptoms(text, feature_cols):
    extracted = {}

    if not text:
        return extracted

    lowered_text = text.lower()

    english_map = {
        "fever": "fever",
        "cough": "cough",
        "headache": "headache",
        "head ache": "headache",
        "vomiting": "vomiting",
        "vomit": "vomiting",
        "nausea": "nausea",
        "weakness": "weakness",
        "weak": "weakness",
        "dizziness": "dizziness",
        "dizzy": "dizziness",
        "chest pain": "sharp chest pain",
        "sharp chest pain": "sharp chest pain",
        "breathlessness": "shortness of breath",
        "shortness of breath": "shortness of breath",
        "breathing problem": "shortness of breath",
        "difficulty breathing": "shortness of breath",
        "abdominal pain": "sharp abdominal pain",
        "stomach pain": "sharp abdominal pain",
        "belly pain": "sharp abdominal pain",
        "diarrhea": "diarrhea",
        "loose motion": "diarrhea",
        "sweating": "sweating",
        "sweat": "sweating",
        "seizure": "seizures",
        "seizures": "seizures",
        "convulsion": "seizures",
        "fainting": "fainting",
        "faint": "fainting",
        "sore throat": "sore throat",
        "runny nose": "nasal congestion",
        "blocked nose": "nasal congestion",
        "nasal congestion": "nasal congestion",
        "blood in stool": "blood in stool",
        "painful urination": "painful urination",
        "burning urination": "painful urination",
        "jaundice": "jaundice",
        "nosebleed": "nosebleed",
    }

    for phrase, feature_name in english_map.items():
        if phrase in lowered_text and feature_name in feature_cols:
            extracted[feature_name] = 1

    for feature in feature_cols:
        if feature in ["age", "sex-no", "ispregnant"]:
            continue

        if feature.lower() in lowered_text:
            extracted[feature] = 1

    return extracted


def create_gray_result(language):
    if language == "বাংলা":
        message = "ইনপুট থেকে কোনো পরিচিত লক্ষণ পাওয়া যায়নি। ব্যবহারকারী সম্ভবত অন্য কিছু বোঝাতে চেয়েছেন।"
    else:
        message = "No recognized symptom was found in the input. The user may be trying to describe something else."

    return {
        "color": "gray",
        "source": "Input validation",
        "message": message
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


def create_referral_pdf(ai_response, triage_result, symptoms):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "GramDoctor AI - Referral Note")
    y -= 35

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Triage Level: {triage_result.get('color', 'unknown').upper()}")
    y -= 18
    pdf.drawString(50, y, f"Decision Source: {triage_result.get('source', 'unknown')}")
    y -= 18

    reason = triage_result.get("message", "")
    for line in wrap_text(f"Reason: {reason}", max_chars=90):
        pdf.drawString(50, y, line)
        y -= 14

    y -= 15

    active_symptoms = [
        symptom for symptom, value in symptoms.items()
        if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
    ]

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Detected Symptoms:")
    y -= 18

    pdf.setFont("Helvetica", 10)

    if active_symptoms:
        for symptom in active_symptoms[:25]:
            pdf.drawString(65, y, f"- {symptom}")
            y -= 14

            if y < 60:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50
    else:
        pdf.drawString(65, y, "- No specific symptom detected")
        y -= 18

    y -= 15

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Referral Note:")
    y -= 20

    pdf.setFont("Helvetica", 10)

    english_note = extract_english_referral_note(ai_response)

    for line in wrap_text(english_note, max_chars=90):
        if y < 60:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 50

        pdf.drawString(50, y, line)
        y -= 14

    y -= 20

    if y < 80:
        pdf.showPage()
        pdf.setFont("Helvetica", 10)
        y = height - 50

    pdf.setFont("Helvetica-Oblique", 9)
    disclaimer = (
        "Disclaimer: This tool does not provide a final diagnosis. "
        "It supports triage and referral guidance only."
    )

    for line in wrap_text(disclaimer, max_chars=95):
        pdf.drawString(50, y, line)
        y -= 12

    pdf.save()
    buffer.seek(0)
    return buffer


@st.cache_resource
def load_resources():
    return load_model_and_features()


model, feature_cols = load_resources()


language = st.selectbox(
    "Language / ভাষা",
    ["English", "বাংলা"],
    index=0,
    key="language_selector"
)

t = TEXTS[language]


st.title(t["title"])
st.subheader(t["subtitle"])
st.warning(t["warning"])


st.sidebar.title(t["sidebar_title"])
st.sidebar.markdown(t["sidebar_help"])

st.sidebar.divider()
st.sidebar.title(t["demo_title"])
st.sidebar.markdown(t["demo_cases"])


if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if "symptoms" not in st.session_state:
    st.session_state.symptoms = None

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""


tab1, tab2 = st.tabs([t["tab_form"], t["tab_result"]])


with tab1:
    st.header(t["patient_info"])

    age = st.number_input(
        t["age"],
        min_value=0,
        max_value=120,
        value=30
    )

    sex_display = st.selectbox(
        t["sex"],
        [t["male"], t["female"]]
    )

    pregnancy_display = st.selectbox(
        t["pregnancy"],
        [t["not_applicable"], t["no"], t["yes"]]
    )

    bangla_text = st.text_area(
        t["text_input"],
        placeholder=t["text_placeholder"]
    )

    uploaded_file = st.file_uploader(
        t["upload_note"],
        type=["txt"]
    )

    uploaded_text = ""

    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8")
        st.text_area(t["uploaded_preview"], uploaded_text, height=150)

    st.subheader(t["voice_input"])
    st.caption(t["voice_help"])

    if speech_to_text is not None:
        voice_result = speech_to_text(
            language="bn-BD" if language == "বাংলা" else "en-US",
            use_container_width=True,
            just_once=True,
            key="voice_input"
        )

        if voice_result:
            st.session_state.voice_text = voice_result

        if st.session_state.voice_text:
            st.success(st.session_state.voice_text)

            if st.button(t["clear_voice"], key="clear_voice_button"):
                st.session_state.voice_text = ""
                st.rerun()

    else:
        st.info(t["voice_unavailable"])

    st.header(t["symptoms"])

    manual_fields = ["age", "sex-no", "ispregnant"]

    symptom_features = [
        col for col in feature_cols
        if col not in manual_fields
    ]

    selected_symptoms = {}

    sorted_symptoms = sorted(symptom_features)

    cols = st.columns(4, gap="large")
    items_per_col = (len(sorted_symptoms) + 3) // 4

    for i, col in enumerate(cols):
      start = i * items_per_col
      end = start + items_per_col

      with col:
        for symptom in sorted_symptoms[start:end]:
            selected_symptoms[symptom] = st.checkbox(symptom.title())

    if st.button(t["check_triage"], type="primary", key="check_triage_button"):
        symptoms = {}

        symptoms["age"] = int(age)
        symptoms["sex-no"] = 1 if sex_display == t["female"] else 0

        if pregnancy_display == t["yes"]:
            symptoms["ispregnant"] = 1
        elif pregnancy_display == t["no"]:
            symptoms["ispregnant"] = 0
        else:
            symptoms["ispregnant"] = 2

        for symptom_name, value in selected_symptoms.items():
            symptoms[symptom_name] = value

        combined_text = f"{bangla_text}\n{uploaded_text}\n{st.session_state.voice_text}".strip()

        bangla_extracted = extract_bangla_symptoms(combined_text, feature_cols)
        english_extracted = extract_english_symptoms(combined_text, feature_cols)

        for symptom_name, value in bangla_extracted.items():
            symptoms[symptom_name] = value

        for symptom_name, value in english_extracted.items():
            symptoms[symptom_name] = value

        active_symptom_count = sum(
            value for key, value in symptoms.items()
            if key not in ["age", "sex-no", "ispregnant"]
        )

        if active_symptom_count == 0:
            result = create_gray_result(language)
        else:
            result = predict_triage(symptoms, model, feature_cols)

        st.session_state.symptoms = symptoms
        st.session_state.triage_result = result
        st.session_state.ai_response = None

        st.success(t["triage_done"])


with tab2:
    st.header(t["triage_result"])

    if st.session_state.triage_result is None:
        st.info(t["no_result"])

    else:
        result = st.session_state.triage_result
        color = result["color"]

        show_triage_card(color, language)

        st.write(t["decision_source"], result["source"])
        st.write(t["reason"], result["message"])

        active_symptoms = [
            symptom for symptom, value in st.session_state.symptoms.items()
            if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
        ]

        if active_symptoms:
            st.subheader(t["detected_symptoms"])
            for symptom in active_symptoms:
                st.write(f"- {symptom}")
        else:
            st.info(t["no_symptoms"])

        st.divider()

        if color == "gray":
            if language == "বাংলা":
                st.info("AI রেফারেল নোট তৈরি করার আগে স্পষ্ট লক্ষণ লিখুন বা বলুন।")
            else:
                st.info("Please enter or speak a clear symptom before generating an AI referral note.")

        else:
            if st.button(t["generate_ai"], key="generate_ai_button"):
                with st.spinner(t["generating"]):
                    ai_response = generate_ai_response(
                        st.session_state.symptoms,
                        st.session_state.triage_result
                    )

                st.session_state.ai_response = ai_response

            if st.session_state.ai_response:
                st.subheader(t["ai_title"])
                st.markdown(st.session_state.ai_response)

                pdf_buffer = create_referral_pdf(
                    st.session_state.ai_response,
                    st.session_state.triage_result,
                    st.session_state.symptoms
                )

                st.download_button(
                    label=t["download_pdf"],
                    data=pdf_buffer,
                    file_name=t["pdf_filename"],
                    mime="application/pdf"
                )