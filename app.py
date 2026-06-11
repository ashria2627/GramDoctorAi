import os
from io import BytesIO

import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from modules.FIRSTAID import get_first_aid
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
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Anek+Bangla:wght@100..800&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');


/* Base */
html, body, p, span, div, label,
h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat','Anek Bangla', sans-serif;
}


.bangla, [lang="bn"] {
    font-family: 'Anek Bangla', sans-serif !important;
}

/* Title */
h1 { 
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(45deg, #0F97A6,#B755D8, #F5F9FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}



/*Sidebar*/
.css-1d391kg, [data-testid="stSidebar"] {
    background-color: #161B22 !important;
    border-right: 1px solid #21262D !important;
}
/* Warning box — replace ugly yellow */
.stAlert {
   
    border: 1px solid #FFFD8A !important;
    border-left: 6px solid #F0883E !important;
    border-radius: 8px !important;
    
    font-size: 0.85rem !important;
    margin : 0.8rem 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    border-radius: 10px;
    padding: 4px;
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #77A9B6;
    font-weight: 500;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background-color: #18768C !important;
    color: #E9F8FB !important;
}

/* Inputs */
.stSelectbox > div, .stNumberInput > div, .stTextArea > div {

    background-color: #161B22 !important;
    border: 2px solid #A3E4E6 !important;
    border-radius: 8px !important;
}

/* Section headers */
h2 {
    color:   #51D0DB !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    margin: 16px 0 !important;
    padding-bottom: 8px !important;
    border-bottom: 1px solid #9EE5EB !important;
}
h3 {
    color:  #26CBE0 !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin: 10px 0 !important;
    padding-bottom: 8px !important;
    
}
p {
    font-weight: 400 !important;    
}

/* Multiselect */
.stMultiSelect > div {
    background-color: #161B22 !important;
    border: 2px solid #A3E4E6 !important;
    border-radius: 8px !important;
}
.stMultiSelect span {
    background-color: #33B9BD !important;
    color: #EBF9FA !important;
    border-radius: 4px !important;
}

/* Success/Warning/Error cards */
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


div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label {
    margin: 12px 0 !important;
    display: block !important;
}
/* Normal button */
.stButton > button {
    background-color: #33B9BD !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
}

/* Hover */
.stButton > button:hover {
    background-color: #195A5C !important;
}

/* Clicked */
.stButton > button:active {
    background-color: #195A5C !important;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("assets/Hospitals_count_Upazilawise.csv")

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
        "pdf_filename": "gramdoctor_referral_note.pdf","division": "Select Division",
        "district": "Select District",
        "upazila": "Select Upazila",
        "hospitals": "Hospitals Found near you",
        "beds": "Beds",
        'search':'Search and click',
        'subwrite':'write your symptoms',
        'write':'Write / record / select / upload your symptoms',
         "recommended_hospitals": "Recommended Hospitals",
          "no_symptoms": "No specific symptom detected from the current input.",
        "refer_to": "Refer to:",
        "alternate_referral": "If not available, see:",
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
        "pdf_filename": "gramdoctor_referral_note.pdf", "division": "বিভাগ নির্বাচন করুন",
        "district": "জেলা নির্বাচন করুন",
        "upazila": "উপজেলা নির্বাচন করুন",
        "hospitals": "আপনার নিকটবর্তী হাসপাতালসমূহ",
        "beds": "শয্যা",
        'search':'অনুসন্ধান করে ক্লিক করুন',
        "subwrite":'আপনার উপসর্গ লিখুন',
        "write":'আপনার উপসর্গ লিখুন, রেকর্ড করুন, নির্বাচন করুন অথবা আপলোড করুন',
          "refer_to": "রেফার করুন:",
        "alternate_referral": "না পেলে বিকল্প হিসেবে দেখান:",
        "recommended_hospitals": "প্রস্তাবিত হাসপাতাল",
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


BANGLA_FEATURES = {
    "sharp abdominal pain": "তীব্র পেট ব্যথা",
    "vomiting": "বমি",
    "headache": "মাথা ব্যথা",
    "cough": "কাশি",
    "sharp chest pain": "তীব্র বুক ব্যথা",
    "nausea": "বমি বমি ভাব",
    "back pain": "পিঠ ব্যথা",
    "shortness of breath": "শ্বাসকষ্ট",
    "fever": "জ্বর",
    "dizziness": "মাথা ঘোরা",
    "nasal congestion": "নাক বন্ধ",
    "leg pain": "পায়ে ব্যথা",
    "skin swelling": "শরীর ফুলে যাওয়া",
    "depressive or psychotic symptoms": "মানসিক বিভ্রান্তি",
    "lower abdominal pain": "তলপেট ব্যথা",
    "sore throat": "গলা ব্যথা",
    "burning abdominal pain": "পেটে জ্বালাপোড়া",
    "skin rash": "ফুসকুড়ি",
    "arm pain": "হাতে ব্যথা",
    "weakness": "দুর্বলতা",
    "ear pain": "কানে ব্যথা",
    "diarrhea": "ডায়রিয়া",
    "loss of sensation": "অনুভূতি হারানো",
    "itching of skin": "চুলকানি",
    "abnormal involuntary movements": "অনিয়ন্ত্রিত শরীর নড়াচড়া",
    "pelvic pain": "শ্রোণী ব্যথা",
    "pain in eye": "চোখে ব্যথা",
    "chest tightness": "বুকে চাপ",
    "problems with movement": "নড়াচড়ায় সমস্যা",
    "diminished vision": "দৃষ্টিশক্তি কমে যাওয়া",
    "painful urination": "প্রস্রাবে ব্যথা",
    "retention of urine": "প্রস্রাব আটকে যাওয়া",
    "difficulty breathing": "শ্বাস নিতে কষ্ট",
    "knee pain": "হাঁটু ব্যথা",
    "blood in stool": "মলে রক্ত",
    "frequent urination": "ঘন ঘন প্রস্রাব",
    "delusions or hallucinations": "হ্যালুসিনেশন",
    "foot or toe pain": "পায়ের পাতা বা আঙুলে ব্যথা",
    "fainting": "অজ্ঞান হওয়া",
    "decreased appetite": "ক্ষুধামন্দা",
    "heartburn": "অম্বল",
    "itchiness of eye": "চোখ চুলকানো",
    "vaginal discharge": "যোনিপথে স্রাব",
    "blood in urine": "প্রস্রাবে রক্ত",
    "involuntary urination": "প্রস্রাব ধরে রাখতে না পারা",
    "chills": "কাঁপুনি",
    "irregular heartbeat": "অনিয়মিত হৃদস্পন্দন",
    "difficulty speaking": "কথা বলতে কষ্ট",
    "palpitations": "হৃদকম্পন",
    "eye redness": "চোখ লাল হওয়া",
    "leg swelling": "পা ফুলে যাওয়া",
    "allergic reaction": "অ্যালার্জি",
    "lip swelling": "ঠোঁট ফুলে যাওয়া",
    "difficulty in swallowing": "গিলতে কষ্ট",
    "foreign body sensation in eye": "চোখে কিছু আছে মনে হওয়া",
    "diminished hearing": "কম শুনতে পাওয়া",
    "cramps and spasms": "খিঁচুনি বা পেশির টান",
    "vaginal itching": "যোনিতে চুলকানি",
    "spots or clouds in vision": "চোখে ঝাপসা বা দাগ দেখা",
    "wheezing": "শ্বাসে সাঁ সাঁ শব্দ",
    "hand or finger swelling": "হাত বা আঙুল ফুলে যাওয়া",
    "swollen eye": "চোখ ফুলে যাওয়া",
    "double vision": "দুইটা দেখা",
    "rectal bleeding": "মলদ্বার দিয়ে রক্ত পড়া",
    "problems during pregnancy": "গর্ভাবস্থার সমস্যা",
    "seizures": "খিঁচুনি",
    "constipation": "কোষ্ঠকাঠিন্য",
    "sweating": "অতিরিক্ত ঘাম",
    "heavy menstrual flow": "অতিরিক্ত মাসিক রক্তপাত",
    "hoarse voice": "কণ্ঠস্বর বসে যাওয়া",
    "vomiting blood": "রক্তবমি",
    "pain of the anus": "মলদ্বারে ব্যথা",
    "white discharge from eye": "চোখ থেকে সাদা স্রাব",
    "eye burns or stings": "চোখে জ্বালা",
    "mouth ulcer": "মুখে ঘা",
    "vaginal pain": "যোনিতে ব্যথা",
    "sleepiness": "ঘুম ঘুম ভাব",
    "ringing in ear": "কানে ভোঁ ভোঁ শব্দ",
    "spotting or bleeding during pregnancy": "গর্ভাবস্থায় রক্তপাত",
    "coughing up sputum": "কফ ওঠা",
    "toothache": "দাঁত ব্যথা",
    "mouth pain": "মুখে ব্যথা",
    "hurts to breath": "শ্বাস নিলে ব্যথা",
    "pain in testicles": "অণ্ডকোষে ব্যথা",
    "throat feels tight": "গলা চেপে আসা",
    "painful sinuses": "সাইনাসে ব্যথা",
    "sinus congestion": "সাইনাস বন্ধ",
    "stomach bloating": "পেট ফাঁপা",
    "hemoptysis": "কাশির সাথে রক্ত",
    "painful menstruation": "মাসিকে ব্যথা",
    "blindness": "অন্ধত্ব",
    "swelling of scrotum": "অণ্ডথলি ফুলে যাওয়া",
    "itchy scalp": "মাথার ত্বকে চুলকানি",
    "throat swelling": "গলা ফুলে যাওয়া",
    "slurring words": "জড়িয়ে কথা বলা",
    "eyelid swelling": "চোখের পাতা ফুলে যাওয়া",
    "jaundice": "জন্ডিস",
    "nosebleed": "নাক দিয়ে রক্ত পড়া"
}



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
    BANGLA_FEATURES.get(symptom, symptom)
    if language == "বাংলা"
    else symptom
    for symptom, value in symptoms.items()
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

def get_recommended_hospitals(filtered_final, n=5):
    return (
        filtered_final
        .sort_values("No. of Bed", ascending=False)
        .head(n)[["Organization Name", "No. of Bed"]]
        .to_dict("records")
    )

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


def get_specialist_referral(triage_result, symptoms, language):
    color = normalize_color(triage_result.get("color", "gray"))
    active = set(get_active_symptom_keys(symptoms))

    if color == "green":
        return None, None

    specialists = {
        "Emergency": {
            "English": "Emergency Department",
            "বাংলা": "জরুরি বিভাগ"
        },
        "General Physician": {
            "English": "General Physician",
            "বাংলা": "জেনারেল ফিজিশিয়ান"
        },
        "Cardiologist": {
            "English": "Cardiologist",
            "বাংলা": "কার্ডিওলজিস্ট / হৃদরোগ বিশেষজ্ঞ"
        },
        "Neurologist": {
            "English": "Neurologist",
            "বাংলা": "নিউরোলজিস্ট / স্নায়ুরোগ বিশেষজ্ঞ"
        },
        "Pulmonologist": {
            "English": "Pulmonologist",
            "বাংলা": "পালমোনোলজিস্ট / বক্ষব্যাধি বিশেষজ্ঞ"
        },
        "Gastroenterologist": {
            "English": "Gastroenterologist",
            "বাংলা": "পরিপাকতন্ত্র বিশেষজ্ঞ"
        },
        "Hepatologist":{
            "English":"Hepatologist",
            'বাংলা':'হেপাটোলজিস্ট / লিভার বিশেষজ্ঞ'
        },
        "Urologist": {
            "English": "Urologist",
            "বাংলা": "ইউরোলজিস্ট / মূত্ররোগ বিশেষজ্ঞ"
        },
        "Endocrinologist": {
            "English": "Endocrinologist",
            "বাংলা": "এন্ডোক্রাইনোলজিস্ট / হরমোন ও ডায়াবেটিস বিশেষজ্ঞ"
        },
        "Dermatologist": {
            "English": "Dermatologist",
            "বাংলা": "ডার্মাটোলজিস্ট / চর্মরোগ বিশেষজ্ঞ"
        },
        "ENT Specialist": {
            "English": "ENT Specialist",
            "বাংলা": "নাক-কান-গলা বিশেষজ্ঞ"
        },
        "Ophthalmologist": {
            "English": "Ophthalmologist",
            "বাংলা": "অফথালমোলজিস্ট / চক্ষু বিশেষজ্ঞ"
        },
        "Dentist": {
            "English": "Dentist",
            "বাংলা": "দন্ত চিকিৎসক"
        },
        "Gynecologist": {
            "English": "Gynecologist / Obstetrician",
            "বাংলা": "প্রসূতি ও স্ত্রীরোগ বিশেষজ্ঞ"
        },
        "Pediatrician": {
            "English": "Pediatrician",
            "বাংলা": "শিশু বিশেষজ্ঞ"
        },
        "Orthopedic Specialist": {
            "English": "Orthopedic Specialist",
            "বাংলা": "হাড়-জোড়া বিশেষজ্ঞ"
        },
        "Psychiatrist": {
            "English": "Psychiatrist",
            "বাংলা": "মানসিক রোগ বিশেষজ্ঞ"
        },
        "Nephrologist": {
            "English": "Nephrologist",
            "বাংলা": "নেফ্রোলজিস্ট / কিডনি বিশেষজ্ঞ"
        },
        "General Surgeon": {
            "English": "General Surgeon",
            "বাংলা": "জেনারেল সার্জন"
        },
    }

    def doctor(name):
        return specialists[name][language]

    general_physician = doctor("General Physician")

    emergency_note = ""

    if color == "red":
      emergency_note = (
        "⚠️ Emergency "
        if language == "English"
        else
        "⚠️ জরুরি অবস্থা "
    )

    cardiac_symptoms = {
        "sharp chest pain", "chest pain", "chest tightness",
        "palpitations", "irregular heartbeat", "sweating", "arm pain"
    }

    neuro_symptoms = {
        "headache", "seizures", "fainting", "slurring words",
        "blindness", "diminished vision", "weakness", "loss of sensation"
    }

    respiratory_symptoms = {
        "cough", "shortness of breath", "wheezing",
        "coughing up sputum", "hemoptysis"
    }

    gi_symptoms = {
        "sharp abdominal pain", "lower abdominal pain", "vomiting",
        "nausea", "diarrhea", "burning abdominal pain", "blood in stool"
    }

    urinary_symptoms = {
        "painful urination", "frequent urination",
        "blood in urine", "involuntary urination"
    }

    kidney_symptoms = {
        "leg swelling", "facial swelling", "decreased urination"
    }

    endocrine_symptoms = {
        "increased thirst", "frequent urination", "weight gain",
        "weight loss", "fatigue", "excessive appetite"
    }

    skin_symptoms = {
        "skin rash", "itching of skin", "skin swelling",
        "acne", "skin lesion", "changes in skin color"
    }

    ent_symptoms = {
        "sore throat", "ear pain", "hearing loss",
        "nasal congestion", "runny nose", "hoarse voice"
    }

    eye_symptoms = {
        "eye pain", "redness in eye", "diminished vision", "blindness"
    }

    dental_symptoms = {
        "tooth pain", "gum pain", "mouth ulcer", "jaw pain"
    }

    gynae_symptoms = {
        "pelvic pain", "lower abdominal pain", "heavy menstrual flow",
        "irregular periods", "spotting or bleeding during pregnancy"
    }

    ortho_symptoms = {
        "back pain", "leg pain", "arm pain", "knee pain",
        "joint pain", "neck pain", "hip pain"
    }

    psych_symptoms = {
        "depressive or psychotic symptoms", "anxiety and nervousness",
        "insomnia", "low mood"
    }

    surgical_symptoms = {
        "sharp abdominal pain", "pain in testicles",
        "rectal bleeding", "vomiting blood"
    }

    if active.intersection(cardiac_symptoms):
        return emergency_note + doctor("Cardiologist"), general_physician

    if active.intersection(neuro_symptoms):
        return emergency_note + doctor("Neurologist"), general_physician

    if active.intersection(respiratory_symptoms):
        return emergency_note + doctor("Pulmonologist"), general_physician

    if active.intersection(gi_symptoms):
        return emergency_note + doctor("Gastroenterologist"), general_physician

    if active.intersection(urinary_symptoms):
        return emergency_note + doctor("Urologist"), general_physician

    if active.intersection(kidney_symptoms):
        return emergency_note + doctor("Nephrologist"), general_physician

    if active.intersection(endocrine_symptoms):
        return emergency_note + doctor("Endocrinologist"), general_physician

    if active.intersection(skin_symptoms):
        return emergency_note + doctor("Dermatologist"), general_physician

    if active.intersection(ent_symptoms):
        return emergency_note + doctor("ENT Specialist"), general_physician

    if active.intersection(eye_symptoms):
        return emergency_note + doctor("Ophthalmologist"), general_physician

    if active.intersection(dental_symptoms):
        return emergency_note + doctor("Dentist"), general_physician

    if symptoms.get("ispregnant", 2) == 1 or active.intersection(gynae_symptoms):
        return emergency_note + doctor("Gynecologist"), general_physician

    if symptoms.get("age", 30) < 13:
        return emergency_note + doctor("Pediatrician"), general_physician

    if active.intersection(ortho_symptoms):
        return emergency_note + doctor("Orthopedic Specialist"), general_physician

    if active.intersection(psych_symptoms):
        return emergency_note + doctor("Psychiatrist"), general_physician

    if active.intersection(surgical_symptoms):
        return emergency_note + doctor("General Surgeon"), general_physician

    return general_physician, None


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
if "filtered_final" not in st.session_state:
    st.session_state.filtered_final = None
if "referral" not in st.session_state:
    st.session_state.referral = None

if "alternate_referral" not in st.session_state:
    st.session_state.alternate_referral = None
    
if "first_aid" not in st.session_state:
    st.session_state.first_aid = None
    
tab1, tab2 = st.tabs([t["tab_form"], t["tab_result"]])


with tab1:
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
    divisions = sorted(df["Division"].dropna().unique())
    division = col1.selectbox(t["division"], divisions)

    filtered_division = df[df["Division"] == division]

# District
    districts = sorted(filtered_division["District"].dropna().unique())
    district = col2.selectbox(t["district"], districts)

    filtered_district = filtered_division[filtered_division["District"] == district]

# Upazila
    upazilas = sorted(filtered_district["Upazila"].dropna().unique())
    upazila = col3.selectbox(t["upazila"], upazilas)

    filtered_final = filtered_district[filtered_district["Upazila"] == upazila]
    st.subheader(t["hospitals"])
    for _, row in filtered_final.iterrows():
      st.write(f"🏥 {row['Organization Name']}")
  
    st.header(t['write'])
    st.subheader(t['subwrite'])
    bangla_text = st.text_area(
        t["text_input"],
        placeholder=t["text_placeholder"]
    )
    

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

    sorted_symptoms = sorted(symptom_features)

    symptom_options = {
    (
        BANGLA_FEATURES.get(symptom, symptom.title())
        if language == "বাংলা"
        else symptom.title()
    ): symptom
    for symptom in sorted_symptoms
     }

    selected_labels = st.multiselect(
     t['search'],
     options=symptom_options.keys()
    )

    selected_symptoms = {
    symptom: symptom in [symptom_options[label] for label in selected_labels]
    for symptom in sorted_symptoms
     }

    uploaded_file = st.file_uploader(
        t["upload_note"],
        type=["txt"]
    )

    uploaded_text = ""

    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8")
        st.text_area(t["uploaded_preview"], uploaded_text, height=150)

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
        st.session_state.first_aid = get_first_aid(symptoms,language)
        st.session_state.ai_response = None
        st.session_state.first_aid = None
        st.session_state.referral = None
        st.session_state.alternate_referral = None
        st.success(t["triage_done"])


with tab2:
    st.header(t["triage_result"])

    if st.session_state.triage_result is None:
        st.info(t["no_result"])

    else:
        result = st.session_state.triage_result
        color = normalize_color(result["color"])
        
        
        if st.session_state.referral:
            referral = st.session_state.referral
            alternate_referral = st.session_state.alternate_referral
        else:
            referral, alternate_referral = get_specialist_referral(
                result,
                st.session_state.symptoms,
                language
            )
        show_triage_card(color, language)
        first_aid = get_first_aid(st.session_state.symptoms, language)
        label = f"🩹 First Aid: {first_aid['condition']}" if language == "English" else f"🩹 প্রাথমিক চিকিৎসা: {first_aid['condition']}"
        with st.expander(label, expanded=color == "red"):
             for i, step in enumerate(first_aid["steps"], 1):
                 st.markdown(f"**{i}.** {step}")
        
        st.write(t["decision_source"], result["source"])
        st.write(t["reason"], result["message"])
        st.divider()
        if referral:
            st.markdown(f"**{t['refer_to']} {referral}**")

        if alternate_referral:
            st.markdown(f"**{t['alternate_referral']} {alternate_referral}**")

        
        if result["color"] in ["red", "orange"]:
         if st.session_state.filtered_final is not None:

          hospitals = get_recommended_hospitals( st.session_state.filtered_final )
          st.subheader(t["recommended_hospitals"])

          for hospital in hospitals:
           st.write(
            f"🏥 {hospital['Organization Name']}"
        )
        active_symptoms = [
    BANGLA_FEATURES.get(symptom, symptom)
    if language == "বাংলা"
    else symptom
    for symptom, value in selected_symptoms.items()
    if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
]

        if active_symptoms:
            st.subheader(t["detected_symptoms"])
            for symptom in active_symptoms:
                 display_name = ( BANGLA_FEATURES.get(symptom, symptom)if language == "বাংলা" else symptom.title())
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
