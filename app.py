from io import BytesIO

import pandas as pd
import streamlit as st
from gtts import gTTS
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from modules.model_backend import load_model_and_features, predict_triage
from modules.BanglaSymptoms import SYMPTOMS, extract_bangla_symptoms
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


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@100..800&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

html, body, p, span, div, label,
h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', 'Anek Bangla', sans-serif;
}

h1 { 
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #b81919,#D9705B, #CC998F);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}

.css-1d391kg, [data-testid="stSidebar"] {
    background-color: #161B22 !important;
    border-right: 1px solid #21262D !important;
}

.stAlert {
    background-color: #161B22 !important;
    border: 1px solid #30363D !important;
    border-left: 4px solid #F0883E !important;
    border-radius: 8px !important;
    color: #8B949E !important;
    font-size: 0.85rem !important;
    margin : 0.8rem 0;
}

.stRadio [role="radiogroup"] {
    display: flex;
    gap: 10px;
}

.stRadio label {
    background-color: #161B22;
    border-radius: 8px;
    padding: 6px 14px;
}

.stSelectbox > div, .stNumberInput > div, .stTextArea > div {
    background-color: #161B22 !important;
    border: 2px solid #821717 !important;
    border-radius: 8px !important;
}

h2 {
    color: #b81919 !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    margin: 16px 0 !important;
    padding-bottom: 8px !important;
    border-bottom: 1px solid #8A271E !important;
}

h3 {
    color: #b81919 !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin: 10px 0 !important;
    padding-bottom: 8px !important;
}

p {
    font-weight: 500 !important;    
}

.stMultiSelect > div {
    background-color: #161B22 !important;
    border: 2px solid #821717 !important;
    border-radius: 8px !important;
}

.stMultiSelect span {
    background-color: #821717 !important;
    color: #EBA4A4 !important;
    border-radius: 4px !important;
}

.stSuccess {
    background-color: #0D1117 !important;
    border: 1px solid #238636 !important;
    border-left: 4px solid #3DD68C !important;
    border-radius: 8px !important;
}

.stWarning {
    background-color: #0D1117 !important;
    border: 1px solid #9E6A03 !important;
    border-left: 4px solid #F0883E !important;
    border-radius: 8px !important;
}

.stError {
    background-color: #0D1117 !important;
    border: 1px solid #DA3633 !important;
    border-left: 4px solid #F85149 !important;
    border-radius: 8px !important;
}

.stButton > button {
    background-color: #AD0505 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
}

.stButton > button:hover {
    background-color: #570303 !important;
}

.stButton > button:active {
    background-color: #570303 !important;
}
</style>
""", unsafe_allow_html=True)


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
2. Enter age, sex, and pregnancy status.
3. Select your location to see nearby hospital names.
4. Type symptoms in Bangla or English.
5. Upload a text note if available.
6. Use voice input if the patient cannot type.
7. Search and select symptoms manually if needed.
8. Click Check Triage.
9. The app will automatically open the Result section.
10. Generate AI explanation, listen to Bangla summary, and download referral PDF.
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
        "form_page": "Patient Form",
        "result_page": "Result",
        "patient_info": "Patient Information",
        "age": "Age",
        "sex": "Sex",
        "male": "Male",
        "female": "Female",
        "pregnancy": "Pregnancy Status",
        "not_applicable": "Not applicable",
        "no": "No",
        "yes": "Yes",
        "division": "Select Division",
        "district": "Select District",
        "upazila": "Select Upazila",
        "hospitals": "Hospitals Found Near You",
        "write": "Write / record / select / upload your symptoms",
        "subwrite": "Write your symptoms",
        "text_input": "Describe symptoms in Bangla or English",
        "text_placeholder": "Example: fever, vomiting, headache or আমার জ্বর, বমি, মাথা ব্যথা হচ্ছে",
        "upload_note": "Optional: Upload patient symptom note",
        "uploaded_preview": "Uploaded note preview",
        "voice_input": "Voice input",
        "voice_help": "Click the microphone and speak symptoms. Works best in Chrome.",
        "voice_unavailable": "Voice input package not installed or unavailable.",
        "clear_voice": "Clear voice text",
        "symptoms": "Symptoms",
        "search": "Search and click symptoms",
        "check_triage": "Check Triage",
        "triage_result": "Triage Result",
        "no_result": "No result yet. Fill the patient form first.",
        "decision_source": "Decision source:",
        "reason": "Reason:",
        "detected_symptoms": "Detected Symptoms",
        "no_symptoms": "No specific symptom detected from the current input.",
        "refer_to": "Refer to:",
        "generate_ai": "Generate AI Explanation",
        "generating": "Generating AI explanation...",
        "ai_title": "AI Explanation and Referral Note",
        "listen_result": "Listen to Result",
        "tts_error": "Could not generate speech audio right now.",
        "download_pdf": "Download Referral Note PDF",
        "pdf_filename": "gramdoctor_referral_note.pdf",
        "recommended_hospitals": "Recommended Hospitals",
    },
    "বাংলা": {
        "title": "গ্রামডক্টর AI",
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
৩. কাছের হাসপাতালের নাম দেখতে লোকেশন নির্বাচন করুন।
৪. বাংলা বা ইংরেজিতে লক্ষণ লিখুন।
৫. চাইলে টেক্সট নোট আপলোড করুন।
৬. রোগী টাইপ করতে না পারলে ভয়েস ইনপুট ব্যবহার করুন।
৭. প্রয়োজন হলে সার্চ করে লক্ষণ সিলেক্ট করুন।
৮. ট্রায়াজ চেক করুন।
৯. অ্যাপ স্বয়ংক্রিয়ভাবে Result অংশে চলে যাবে।
১০. AI ব্যাখ্যা, Bangla voice summary এবং referral PDF তৈরি করুন।
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
        "form_page": "রোগীর ফর্ম",
        "result_page": "ফলাফল",
        "patient_info": "রোগীর তথ্য",
        "age": "বয়স",
        "sex": "লিঙ্গ",
        "male": "পুরুষ",
        "female": "নারী",
        "pregnancy": "গর্ভাবস্থার অবস্থা",
        "not_applicable": "প্রযোজ্য নয়",
        "no": "না",
        "yes": "হ্যাঁ",
        "division": "বিভাগ নির্বাচন করুন",
        "district": "জেলা নির্বাচন করুন",
        "upazila": "উপজেলা নির্বাচন করুন",
        "hospitals": "আপনার নিকটবর্তী হাসপাতালসমূহ",
        "write": "লক্ষণ লিখুন / রেকর্ড করুন / সিলেক্ট করুন / আপলোড করুন",
        "subwrite": "আপনার লক্ষণ লিখুন",
        "text_input": "বাংলা বা ইংরেজিতে লক্ষণ লিখুন",
        "text_placeholder": "যেমন: আমার জ্বর, বমি, মাথা ব্যথা হচ্ছে",
        "upload_note": "ঐচ্ছিক: রোগীর লক্ষণের টেক্সট নোট আপলোড করুন",
        "uploaded_preview": "আপলোড করা নোট প্রিভিউ",
        "voice_input": "ভয়েস ইনপুট",
        "voice_help": "মাইক্রোফোনে ক্লিক করে লক্ষণ বলুন। Chrome ব্রাউজারে ভালো কাজ করে।",
        "voice_unavailable": "Voice input package ইনস্টল নেই অথবা কাজ করছে না।",
        "clear_voice": "ভয়েস টেক্সট মুছে ফেলুন",
        "symptoms": "লক্ষণসমূহ",
        "search": "সার্চ করে লক্ষণ নির্বাচন করুন",
        "check_triage": "ট্রায়াজ চেক করুন",
        "triage_result": "ট্রায়াজ ফলাফল",
        "no_result": "এখনো কোনো ফলাফল নেই। আগে রোগীর ফর্ম পূরণ করুন।",
        "decision_source": "সিদ্ধান্তের উৎস:",
        "reason": "কারণ:",
        "detected_symptoms": "সনাক্ত হওয়া লক্ষণ",
        "no_symptoms": "বর্তমান ইনপুট থেকে নির্দিষ্ট কোনো লক্ষণ পাওয়া যায়নি।",
        "refer_to": "রেফার করুন:",
        "generate_ai": "AI ব্যাখ্যা তৈরি করুন",
        "generating": "AI ব্যাখ্যা তৈরি হচ্ছে...",
        "ai_title": "AI ব্যাখ্যা ও রেফারেল নোট",
        "listen_result": "ফলাফল শুনুন",
        "tts_error": "এখন ভয়েস অডিও তৈরি করা যায়নি।",
        "download_pdf": "Referral Note PDF ডাউনলোড করুন",
        "pdf_filename": "gramdoctor_referral_note.pdf",
        "recommended_hospitals": "প্রস্তাবিত হাসপাতাল",
    }
}


BANGLA_FEATURES = {}
for bangla_phrase, english_feature in SYMPTOMS.items():
    if english_feature not in BANGLA_FEATURES:
        BANGLA_FEATURES[english_feature] = bangla_phrase


@st.cache_data
def load_hospital_data():
    try:
        return pd.read_csv("assets/Hospitals_count_Upazilawise.csv")
    except Exception:
        return pd.DataFrame()


@st.cache_resource
def load_resources():
    return load_model_and_features()


def normalize_color(color):
    if not color:
        return "gray"

    color = str(color).lower().strip()

    if color == "grey":
        return "gray"

    return color


def get_symptom_display(symptom, language):
    if language == "বাংলা":
        return BANGLA_FEATURES.get(symptom, symptom)
    return symptom.title()


def get_active_symptom_keys(symptoms):
    if not symptoms:
        return []

    return [
        symptom for symptom, value in symptoms.items()
        if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
    ]


def show_triage_card(color, language):
    color = normalize_color(color)

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
            st.warning("ORANGE — ১-২ দিনের মধ্যে ডাক্তার দেখান")
            st.markdown("""
            **অর্থ:** লক্ষণগুলো চিকিৎসকের মূল্যায়ন প্রয়োজন হতে পারে।  
            **করণীয়:** ২৪-৪৮ ঘণ্টার মধ্যে ডাক্তার, ক্লিনিক বা উপজেলা স্বাস্থ্য কমপ্লেক্সে যান।  
            **জরুরি চিকিৎসা নিন যদি:** দুর্বলতা, পানিশূন্যতা, তীব্র ব্যথা বা শ্বাসকষ্ট বাড়ে।
            """)
        else:
            st.warning("ORANGE — Visit doctor within 1-2 days")
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
            **Meaning:** Emergency red-flag symptoms may be present.  
            **Recommended action:** Go to the nearest emergency department immediately.  
            **Do not:** wait at home or delay medical care.
            """)

    elif color == "gray":
        if language == "বাংলা":
            st.info("GRAY — লক্ষণ বোঝা যায়নি")
            st.markdown("""
            **অর্থ:** আপনার ইনপুট থেকে কোনো পরিচিত লক্ষণ পাওয়া যায়নি।  
            **প্রশ্ন:** আপনি কি কোনো লক্ষণ বোঝাতে চেয়েছেন?  
            **করণীয়:** অনুগ্রহ করে স্পষ্টভাবে লক্ষণ লিখুন বা বলুন, যেমন: জ্বর, বমি, কাশি, শ্বাসকষ্ট।
            """)
        else:
            st.info("GRAY — Symptom unclear")
            st.markdown("""
            **Meaning:** No recognized symptom was detected from the input.  
            **Question:** Are you trying to describe a symptom?  
            **Action:** Please write or speak symptoms clearly, for example: fever, vomiting, cough, shortness of breath.
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


def get_specialist_referral(triage_result, symptoms):
    color = normalize_color(triage_result.get("color", "gray"))
    active = set(get_active_symptom_keys(symptoms))

    cardiac_symptoms = {
        "sharp chest pain",
        "chest tightness",
        "palpitations",
        "irregular heartbeat",
        "sweating",
        "arm pain",
    }

    if color == "green":
        return None

    if color == "red":
        return "Emergency"

    if active.intersection(cardiac_symptoms):
        return "Cardiologist"

    if color == "gray":
        return "Clarify symptoms"

    return "General Physician"


def get_tts_summary_bangla(triage_result, symptoms, referral):
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

    bangla_referral = {
        "Emergency": "ইমার্জেন্সি",
        "Cardiologist": "কার্ডিওলজিস্ট",
        "General Physician": "জেনারেল ফিজিশিয়ান",
        "Clarify symptoms": "লক্ষণ স্পষ্ট করুন",
    }.get(referral, referral)

    if active:
        symptom_text = ", ".join([BANGLA_FEATURES.get(s, s) for s in active[:6]])
    else:
        symptom_text = "কোনো নির্দিষ্ট লক্ষণ পাওয়া যায়নি"

    summary = (
        f"আপনার ট্রায়াজ ফলাফল {bangla_color}. "
        f"সনাক্ত হওয়া লক্ষণ: {symptom_text}. "
    )

    if referral:
        summary += f"রেফার করুন: {bangla_referral}. "

    summary += bangla_action

    return summary


def create_tts_audio(text):
    buffer = BytesIO()
    tts = gTTS(text=text, lang="bn")
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer


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
                "What Not To Do:",
                "Possible diagnosis",
            ]

            for stop_marker in stop_markers:
                if stop_marker in note:
                    note = note.split(stop_marker, 1)[0].strip()

            return note

    return ai_response


def create_referral_pdf(ai_response, triage_result, symptoms, referral):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "GramDoctor AI - Referral Note")
    y -= 35

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Triage Level: {normalize_color(triage_result.get('color', 'unknown')).upper()}")
    y -= 18

    if referral:
        pdf.drawString(50, y, f"Refer to: {referral}")
        y -= 18

    pdf.drawString(50, y, f"Decision Source: {triage_result.get('source', 'unknown')}")
    y -= 18

    reason = triage_result.get("message", "")

    for line in wrap_text(f"Reason: {reason}", max_chars=90):
        pdf.drawString(50, y, line)
        y -= 14

    y -= 15

    active_symptoms = get_active_symptom_keys(symptoms)

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


def get_recommended_hospitals(filtered_final, n=5):
    if filtered_final is None or filtered_final.empty:
        return []

    return (
        filtered_final
        .sort_values("Organization Name", ascending=True)
        .head(n)[["Organization Name"]]
        .to_dict("records")
    )


model, feature_cols = load_resources()
df = load_hospital_data()


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


if "go_to_result" not in st.session_state:
    st.session_state.go_to_result = False

if "page_radio" not in st.session_state:
    st.session_state.page_radio = "form"

if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if "symptoms" not in st.session_state:
    st.session_state.symptoms = None

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "filtered_final" not in st.session_state:
    st.session_state.filtered_final = None

if "referral" not in st.session_state:
    st.session_state.referral = None


if st.session_state.go_to_result:
    st.session_state.page_radio = "result"
    st.session_state.go_to_result = False


page = st.radio(
    "",
    ["form", "result"],
    format_func=lambda x: t["form_page"] if x == "form" else t["result_page"],
    horizontal=True,
    key="page_radio",
    label_visibility="collapsed"
)


if page == "form":
    st.header(t["patient_info"])

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input(
            t["age"],
            min_value=0,
            max_value=120,
            value=30
        )

    with col2:
        sex_display = st.selectbox(
            t["sex"],
            [t["male"], t["female"]]
        )

    with col3:
        pregnancy_display = st.selectbox(
            t["pregnancy"],
            [t["not_applicable"], t["no"], t["yes"]]
        )

    filtered_final = pd.DataFrame()

    if not df.empty:
        divisions = sorted(df["Division"].dropna().unique())
        division = col1.selectbox(t["division"], divisions)

        filtered_division = df[df["Division"] == division]

        districts = sorted(filtered_division["District"].dropna().unique())
        district = col2.selectbox(t["district"], districts)

        filtered_district = filtered_division[filtered_division["District"] == district]

        upazilas = sorted(filtered_district["Upazila"].dropna().unique())
        upazila = col3.selectbox(t["upazila"], upazilas)

        filtered_final = filtered_district[filtered_district["Upazila"] == upazila]

        st.subheader(t["hospitals"])

        for _, row in filtered_final.iterrows():
            st.write(f"🏥 {row['Organization Name']}")

    st.header(t["write"])
    st.subheader(t["subwrite"])

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

    st.subheader(t["symptoms"])

    manual_fields = ["age", "sex-no", "ispregnant"]

    symptom_features = [
        col for col in feature_cols
        if col not in manual_fields
    ]

    sorted_symptoms = sorted(symptom_features, key=str.lower)

    symptom_options = {
        (
            get_symptom_display(symptom, language)
            if language == "বাংলা"
            else symptom.title()
        ): symptom
        for symptom in sorted_symptoms
    }

    selected_labels = st.multiselect(
        t["search"],
        options=list(symptom_options.keys())
    )

    selected_symptoms = {
        symptom: symptom in [symptom_options[label] for label in selected_labels]
        for symptom in sorted_symptoms
    }

    if st.button(t["check_triage"], type="primary", key="check_triage_button"):
        st.session_state.filtered_final = filtered_final

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

        active_symptom_count = len(get_active_symptom_keys(symptoms))

        if active_symptom_count == 0:
            result = create_gray_result(language)
        else:
            result = predict_triage(symptoms, model, feature_cols)

        result["color"] = normalize_color(result.get("color", "gray"))

        referral = get_specialist_referral(result, symptoms)

        st.session_state.symptoms = symptoms
        st.session_state.triage_result = result
        st.session_state.referral = referral
        st.session_state.ai_response = None
        st.session_state.go_to_result = True

        st.rerun()


if page == "result":
    st.header(t["triage_result"])

    if st.session_state.triage_result is None:
        st.info(t["no_result"])

    else:
        result = st.session_state.triage_result
        color = normalize_color(result["color"])
        referral = st.session_state.referral or get_specialist_referral(result, st.session_state.symptoms)

        show_triage_card(color, language)

        st.write(t["decision_source"], result["source"])
        st.write(t["reason"], result["message"])

        if referral:
            st.markdown(f"**{t['refer_to']} {referral}**")

        active_symptoms = get_active_symptom_keys(st.session_state.symptoms)

        if active_symptoms:
            st.subheader(t["detected_symptoms"])

            for symptom in active_symptoms:
                st.write(f"- {get_symptom_display(symptom, language)}")
        else:
            st.info(t["no_symptoms"])

        if color in ["red", "orange"] and st.session_state.filtered_final is not None:
            hospitals = get_recommended_hospitals(st.session_state.filtered_final)

            if hospitals:
                st.subheader(t["recommended_hospitals"])

                for hospital in hospitals:
                    st.write(f"🏥 {hospital['Organization Name']}")

        st.divider()

        if st.button(t["listen_result"], key="listen_result_button"):
            try:
                summary_text = get_tts_summary_bangla(result, st.session_state.symptoms, referral)
                audio_buffer = create_tts_audio(summary_text)
                st.audio(audio_buffer, format="audio/mp3")
            except Exception:
                st.error(t["tts_error"])

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
                    st.session_state.symptoms,
                    referral
                )

                st.download_button(
                    label=t["download_pdf"],
                    data=pdf_buffer,
                    file_name=t["pdf_filename"],
                    mime="application/pdf"
                )