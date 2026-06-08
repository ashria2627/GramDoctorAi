import os
import math
import json
import re
from io import BytesIO
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from modules.FIRSTAID import get_first_aid
from modules.model_backend import load_model_and_features, predict_triage
from modules.BanglaSymptoms import extract_bangla_symptoms
from modules.gemini_helper import generate_ai_response
from modules.FIRSTAID import SYMPTOM_FIRST_AID,SPECIAL_FIRST_AID
from modules.triage_rules import apply_bd_rules
from modules.offline_detector import detect_local_emergency, detect_local_emergencies
from modules.Followup import FOLLOWUP_GROUPS, detect_followup_categories
from modules.symptom_normalizer import normalize_symptom_input
from gtts import gTTS

try:
    from streamlit_mic_recorder import speech_to_text
except Exception:
    speech_to_text = None
try:
    from streamlit_js_eval import get_geolocation
except Exception:
    get_geolocation = None

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
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(45deg, #0F97A6,#B755D8, #F5F9FA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0 !important;
}



/*Sidebar*/
.css-1d391kg, [data-testid="stSidebar"] {
    background-color: #161B22 !important;
    border-right: 2px solid #21262D !important;
}
/* Warning box " replace ugly yellow */
.stAlert {  
    border: 2px solid #FFFD8A !important;
    border-left: 6px solid #F0883E !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    margin : 0.9rem 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    border-radius: 10px;
    padding:5px;
    gap: 5px;
    margin: auto !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.75rem !important;
    border-radius: 8px;
    color: #77A9B6;
    font-weight: 600;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    font-size: 1.5rem !important;
    background-color: #18768C !important;
    color: #E9F8FB !important;
}

/* Inputs */
.stSelectbox > div, .stNumberInput > div, .stTextArea > div {

    background-color: #161B22 !important;
    border: 2px solid #A3E4E6 !important;
    border-radius: 8px !important;
    margin: auto !important;
}

/* Section headers */
h2 {
    color:   #51D0DB !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin: 16px 0 !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid #9EE5EB !important;
}
h3 {
    color:  #26CBE0 !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    margin: 5px 0 !important;
    padding-bottom: 5px !important;
    
}
p {
    font-size: 1.1rem !important;
    font-weight: 400 !important;    
}

/* Multiselect */
.stMultiSelect > div {
    background-color: #161B22 !important;
    border: 2px solid #A3E4E6 !important;
    border-radius: 8px !important;
    margin-bottom : 2rem  !important;
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
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    background-color: #33B9BD !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 2rem !important;
    margin: 2rem 0 !important;
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
        "patient_form": "Patient Form",
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
        "text_placeholder": "Example: fever, vomiting, headache or জ্বর, বমি, মাথাব্যথা",
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
        "use_device_location": "Turn on device location for better experience",
        "location_unavailable": "Device location is unavailable. Showing hospitals from selected area.",
        "location_found": "Device location detected. Hospitals are sorted by distance.",
        "distance": "Distance",
        "beds": "Beds",
        'search':'Search and click',
        'subwrite':'write your symptoms',
        'write':'Write / record / select / upload your symptoms',
         "recommended_hospitals": "Recommended Hospitals",
          "no_symptoms": "No specific symptom detected from the current input.",
        "refer_to": "Refer to:",
        "alternate_referral": "If not available, see:",
        'follow-up':"Follow-up Questions",
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
        "patient_form": "রোগীর ফর্ম",
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
        "use_device_location": "আরও ভালো অভিজ্ঞতার জন্য ডিভাইস লোকেশন চালু করুন",
        "location_unavailable": "ডিভাইস লোকেশন পাওয়া যায়নি। নির্বাচিত এলাকার হাসপাতাল দেখানো হচ্ছে।",
        "location_found": "ডিভাইস লোকেশন পাওয়া গেছে। দূরত্ব অনুযায়ী হাসপাতাল সাজানো হয়েছে।",
        "distance": "দূরত্ব",
        "beds": "শয্যা",
        'search':'অনুসন্ধান করে ক্লিক করুন',
        "subwrite":'আপনার উপসর্গ লিখুন',
        "write":'আপনার উপসর্গ লিখুন, রেকর্ড করুন, নির্বাচন করুন অথবা আপলোড করুন',
          "refer_to": "রেফার করুন:",
        "alternate_referral": "না পেলে বিকল্প হিসেবে দেখান:",
        "recommended_hospitals": "প্রস্তাবিত হাসপাতাল",
        'follow-up':"পর্যবেক্ষণ",
    }
}


def show_triage_card(color, language):
    if color == "green":
        if language == "বাংলা":
            st.success("GREEN — বাসায় পর্যবেক্ষণ")
            st.markdown("""
            **অর্থ:** বর্তমান তথ্য অনুযায়ী লক্ষণগুলো কম ঝুঁকিপূর্ণ মনে হচ্ছে। আপনি যদি এখনও ***ফলো-আপ*** প্রশ্নগুলোর উত্তর না দিয়ে থাকেন, তবে অনুগ্রহ করে তা দিয়ে দিন, যাতে আপনি আপনার বর্তমান অবস্থার জন্য নিখুঁত সুপারিশ পেতে পারেন।
             
            **করণীয়:** বিশ্রাম, পর্যাপ্ত পানি এবং লক্ষণ পর্যবেক্ষণ।  
            
            **চিকিৎসা নিন যদি:** লক্ষণ বাড়ে, জ্বর থাকে, বা বিপদ সংকেত দেখা যায়।
            """)
        else:
            st.success("GREEN — Home care / observe")
            st.markdown("""
            **Meaning:** Current symptoms appear low risk based on triage input. If you have not yet answered ***follow-up*** questions ,please do so you get perfect recommendation for your current condition.  
             
            **Recommended action:** Rest, drink fluids, and monitor symptoms.  
            
            **Seek care if:** symptoms worsen, fever persists, or danger signs appear.
            """)

    elif color == "orange":
        if language == "বাংলা":
            st.warning("ORANGE - পর্যবেক্ষণে রাখুন। উপসর্গ বেড়ে গেলে বা অবস্থার অবনতি হলে ১–২ দিনের মধ্যে চিকিৎসকের পরামর্শ নিন।  ")
            st.markdown("""
            **অর্থ:** লক্ষণগুলো চিকিৎসকের মূল্যায়ন প্রয়োজন হতে পারে। আপনি যদি এখনও ***ফলো-আপ*** প্রশ্নগুলোর উত্তর না দিয়ে থাকেন, তবে অনুগ্রহ করে তা দিয়ে দিন, যাতে আপনি আপনার বর্তমান অবস্থার জন্য নিখুঁত সুপারিশ পেতে পারেন। 
            
            **করণীয়:** **২৪-৪৮ ঘণ্টার** মধ্যে ডাক্তার, ক্লিনিক বা উপজেলা স্বাস্থ্য কমপ্লেক্সে যান। 
             
            **জরুরি চিকিৎসা নিন যদি:** দুর্বলতা, পানিশূন্যতা, তীব্র ব্যথা বা শ্বাসকষ্ট বাড়ে।
            """)
        else:
            st.warning("ORANGE — Observe and if worsen Visit doctor within 1-2 days")
            st.markdown("""
            **Meaning:** Symptoms need medical review but may not be an immediate emergency. If you have not yet answered  ***follow-up questions*** ,please do so you get perfect recommendation for your current condition.
            
            **Recommended action:** Visit a local doctor, clinic, or Upazila Health Complex within **24-48 hours.**
            
            **Seek urgent care if:** weakness, dehydration, severe pain, or breathing difficulty worsens.
            """)

    elif color == "red":
        if language == "বাংলা":
            st.error("RED — এখনই জরুরি চিকিৎসা নিন")
            st.markdown("""
            **অর্থ:** জরুরি বিপদ সংকেত থাকতে পারে।
              
            **করণীয়:** এখনই নিকটস্থ হাসপাতাল বা ***জরুরি বিভাগে যান।*** 
            
            **করবেন না:** বাসায় অপেক্ষা করবেন না বা চিকিৎসা নিতে দেরি করবেন না।
            """)
        else:
            st.error("RED — Emergency care now")
            st.markdown("""
            **Meaning:** Emergency red-flag silent symptoms may be present. 
             
            **Recommended action:** Go to the nearest ***emergency department immediately.***
             
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
    return normalize_symptom_input(text, feature_cols)


BANGLA_FEATURES = {
    "sharp abdominal pain": "পেটে ব্যথা",
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
    "nosebleed": "নাক দিয়ে রক্ত পড়া",
    "sneezing": "হাঁচি",
}


EXTRA_DISPLAY_SYMPTOMS = {
    "sneezing": {
        "English": "Sneezing",
        "বাংলা": "হাঁচি",
        "terms": [
            "sneezing",
            "sneeze",
            "sneezes",
            "হাঁচি",
            "হাচি",
            "হাঁচি হচ্ছে",
            "হাচি হচ্ছে",
            "অনেক হাঁচি",
            "বারবার হাঁচি",
            "hachi",
            "hanchi",
            "haci",
        ],
    },
}


def detect_extra_display_symptoms(text):
    if not text:
        return []

    lowered = text.lower()
    found = []
    for symptom, info in EXTRA_DISPLAY_SYMPTOMS.items():
        for term in info["terms"]:
            term_text = term.lower().strip()
            if term_text and re.search(rf"(?<![a-z0-9]){re.escape(term_text)}(?![a-z0-9])", lowered):
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


def format_prediction_driver(item, triage_color=None):
    feature = str(item.get("feature", "This factor")).replace("_", " ").title()
    impact = float(item.get("impact", 0))

    if abs(impact) < 0.0001:
        return None

    direction = "increased" if impact > 0 else "reduced"
    target = f" the {triage_color} result" if triage_color else " this triage result"
    return f"{feature} {direction} confidence in{target}."


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

    section("Prediction Drivers")
    explanation = triage_result.get("explanation") or []
    explanation_lines = [
        format_prediction_driver(item, triage_result.get("color"))
        for item in explanation
    ]
    explanation_lines = [line for line in explanation_lines if line]
    if explanation_lines:
        write_lines([f"- {line}" for line in explanation_lines])
    else:
        write_lines("No SHAP explanation available for this decision.")

    section("Recommended Specialist")
    write_lines(referral or "General Physician")

    section("First Aid Steps")
    if first_aid:
        steps = first_aid.get("steps_en") or first_aid.get("steps") or []
        write_lines([f"- {step}" for step in steps[:6]] or "No first aid steps available.")
    else:
        write_lines("No first aid steps available.")

    

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

@st.cache_data
def load_specialist_lookup():
    path = os.path.join(os.path.dirname(__file__), "modules", "specialist_lookup.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_specialist_referral_clustered(triage_result, symptoms, language):
    color = normalize_color(triage_result.get("color", "gray"))
    active = set(get_active_symptom_keys(symptoms))

    if color == "green":
        return None, None

    scored = build_specialist_concerns(symptoms)

    if not scored:
        if symptoms.get("ispregnant", 2) == 1:
            return specialist_label("Gynecologist", language), specialist_label("General Physician", language)
        if symptoms.get("age", 30) < 13:
            return specialist_label("Pediatrician", language), specialist_label("General Physician", language)
        return specialist_label("General Physician", language), None

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

    return emergency_note + specialist_label(specialist_name, language), specialist_label("General Physician", language)

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


if "referral" not in st.session_state:
    st.session_state.referral = None

if "alternate_referral" not in st.session_state:
    st.session_state.alternate_referral = None
    
if "first_aid" not in st.session_state:
    st.session_state.first_aid = None

if "detected_special" not in st.session_state:
    st.session_state.detected_special = "none"

if "extra_symptoms" not in st.session_state:
    st.session_state.extra_symptoms = []

tab1, tab2,tab3 = st.tabs([t["patient_form"],t['follow-up'],t['tab_result']])


with tab1:
    st.header(t["patient_info"])

    col1, col2, col3 = st.columns(3)

    with col1:
     age = st.number_input(
        t["age"],
        min_value=0,
        max_value=120,
        value=21
    )

    with col2:
     sex_display = st.selectbox(
        t["sex"],
        [t["male"], t["female"]]
    )
    with col3:
      if sex_display == t["male"]:
        pregnancy_display = t["not_applicable"]

        st.selectbox(
            t["pregnancy"],
            [t["not_applicable"]],
            disabled=True
        )
      else:
        pregnancy_display = st.selectbox(
            t["pregnancy"],
            [t["no"], t["yes"]]
        )

  
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
      with st.spinner("Analyzing symptoms..." if language=="English" else "লক্ষণ বিশ্লেষণ হচ্ছে..."):
        
        symptoms = {}

        symptoms["age"] = int(age)
        symptoms["sex-no"] = 1 if sex_display == t["female"] else 0

        if sex_display == t["male"]:
             symptoms["ispregnant"] = 2   # Not Applicable
        else:
             symptoms["ispregnant"] = 1 if pregnancy_display == t["yes"] else 0
 
        for symptom_name, value in selected_symptoms.items():
            symptoms[symptom_name] = value

        combined_text = f"{bangla_text}\n{uploaded_text}\n{st.session_state.voice_text}".strip()
        st.session_state.extra_symptoms = detect_extra_display_symptoms(combined_text)

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

        # symptom detection
        local_specials = detect_local_emergencies(combined_text, SPECIAL_FIRST_AID)
        local_special = local_specials[0] if local_specials else None

        if local_special:
           special = local_special
        else:
           from modules.gemini_helper import detect_special_emergency
           special = detect_special_emergency(combined_text)

        if active_symptom_count > 0:
            result = predict_triage(symptoms, model, feature_cols)
        else:
            result = create_gray_result(language)

        if special.get("found"):
            color_messages = {
                "red": "Possible {cond} detected. This needs urgent medical attention.",
                "orange": "Possible {cond} detected. Please visit a doctor within 1-2 days.",
                "green": "Possible {cond} detected. This can usually be managed at home, but watch for worsening.",
            }
            color_messages_bn = {
                "red": "সম্ভাবনা: {cond}। এটি জরুরি চিকিৎসা প্রয়োজন।",
                "orange": "সম্ভাবনা: {cond}। ১-২ দিনের মধ্যে ডাক্তার দেখান।",
                "green": "সম্ভাবনা: {cond}। বাড়িতে যত্ন নেওয়া যায়, কিন্তু অবস্থা খারাপ হলে ডাক্তার দেখান।",
            }

            cond = ", ".join(item["condition"] for item in local_specials) if local_specials else special["condition"]
            special_color = special["color"]
            if any(item.get("color") == "red" for item in local_specials):
                special_color = "red"

            order = ["green", "orange", "red"]
            current_color = result.get("color", "green")
            if current_color not in order:
                current_color = "green"

            
            if order.index(special_color) >= order.index(current_color):
                if language == "বাংলা":
                    message = color_messages_bn[special_color].format(cond=cond)
                else:
                    message = color_messages[special_color].format(cond=cond)

                result = {
                    "color": special_color,
                    "source": "Special emergency detection",
                    "message": message,
                    "confidence": None
                }

            st.session_state.detected_special = special
            st.session_state.detected_specials = local_specials or [special]
        else:
            st.session_state.detected_special = None
            st.session_state.detected_specials = []
        
        
        st.session_state.symptoms = symptoms
        st.session_state.triage_result = result
        st.session_state.original_triage_color = result["color"]
        st.session_state.original_triage_message = result["message"]
        st.session_state.original_triage_source = result["source"]
        detected_special=st.session_state.get("detected_special")
        st.session_state.followup_categories = detect_followup_categories(symptoms, FOLLOWUP_GROUPS,language,detected_special)               
        st.session_state.ai_response = None
        st.session_state.first_aid = None
        st.session_state.tts_audio = None
        if st.session_state.get("detected_special") and st.session_state.detected_special.get("found"):
            st.session_state.referral = (
                "Emergency Department"
                if language == "English"
                else "জরুরি বিভাগ"
            )

            st.session_state.alternate_referral = (
                "General Physician"
                if language == "English"
                else "জেনারেল ফিজিশিয়ান"
            )
        else:
            st.session_state.referral = None
            st.session_state.alternate_referral = None
        st.success(t["triage_done"])

with tab2:
    cats = st.session_state.get("followup_categories", [])
    if not cats:
        st.info("No follow-up needed yet." if language=="English" else "এখনো ফলো-আপ প্রয়োজন নেই।")
    else:
        followup_answers = {}
        for cat_idx, cat in enumerate(cats):
            st.subheader(('Probable 'if language=="English" else "সম্ভাব্য ")+cat.title())
            # st.write("DEBUG cats:", cats)
            qs = FOLLOWUP_GROUPS[cat]["questions_bn" if language=="বাংলা" else "questions_en"]
            for i, q in enumerate(qs):
                 key = f"fu_{cat_idx}_{cat}_{i}"
                 followup_answers[key] = st.text_input(q, key=key)
        if st.button("Update Triage" if language=="English" else "ট্রায়াজ আপডেট করুন"):
          with st.spinner("Updating triage..." if language=="English" else "ট্রায়াজ আপডেট হচ্ছে..."):
            for k, v in followup_answers.items():
                 st.session_state.symptoms[k] = v
            
            st.session_state.followup_answers = followup_answers
            result = predict_triage(st.session_state.symptoms, model, feature_cols)
            result = apply_bd_rules(st.session_state.symptoms, result, followup_answers, language)
            from modules.FIRSTAID import get_first_aid_from_followup
            st.session_state.first_aid = get_first_aid_from_followup(
    followup_answers,
    language,
    symptoms=st.session_state.symptoms,
    triage_color=st.session_state.triage_result["color"]
)
            st.session_state.triage_result = result
            st.session_state.tts_audio = None
            st.success("Updated! Check Result tab." if language=="English" else "আপডেট হয়েছে! Result ট্যাব দেখুন।")


with tab3:
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
            referral, alternate_referral = get_specialist_referral_clustered(
                result,
                st.session_state.symptoms,
                language
            )
        show_triage_card(color, language)
        special = st.session_state.get("detected_special")
        special_events = st.session_state.get("detected_specials", [])

        if result["source"] == "Special emergency detection" and special_events:
            steps_en = []
            steps_bn = []
            for event in special_events:
                steps_en.append(f"{event['condition']}:")
                steps_en.extend(event.get("advice_en", []))
                steps_bn.append(f"{event['condition']}:")
                steps_bn.extend(event.get("advice_bn", []))
            first_aid = {
                "condition": "Multiple Injury/Event First Aid" if len(special_events) > 1 else special_events[0]["condition"],
                "steps_en": steps_en,
                "steps_bn": steps_bn,
            }
        else:
            first_aid = st.session_state.get("first_aid") or get_first_aid(st.session_state.symptoms, language)
        label = f"🩹 First Aid: {first_aid['condition']}" if language == "English" else f"🩹 প্রাথমিক চিকিৎসা: {first_aid['condition']}"
        with st.expander(label, expanded=color == "red"):
            if "steps_en" in first_aid:
                     steps = first_aid["steps_bn"] if language == "বাংলা" else first_aid["steps_en"]
            else:
                     steps = first_aid["steps"]

            for i, step in enumerate(steps, 1):
                       st.markdown(f"**{i}.** {step}")
         
        st.write(t["decision_source"], result["source"])
        st.write(t["reason"], result["message"])
        confidence = result.get("confidence")
        if confidence is not None:
            st.progress(min(max(float(confidence) / 100, 0), 1), text=f"Model Confidence: {confidence}%")
            if confidence < 60:
                st.warning("Low confidence - please consult a doctor." if language == "English" else "Low confidence - অনুগ্রহ করে ডাক্তারের পরামর্শ নিন। ")
        explanation = result.get("explanation") or []
        explanation_lines = [
            format_prediction_driver(item, result.get("color"))
            for item in explanation
        ]
        explanation_lines = [line for line in explanation_lines if line]
        if explanation_lines:
            st.caption("Top prediction drivers")
            for line in explanation_lines:
                st.write(f"- {line}")
        st.divider()
        if st.button('listen result', key="listen_result_button"):
          st.session_state.tts_audio = None  # force regenerate

        if st.session_state.get("tts_audio") is None and st.session_state.get("triage_result"):
          try:
             summary_text = get_tts_summary_bangla(
              st.session_state.triage_result,
              st.session_state.symptoms,
              st.session_state.get("referral"),
              st.session_state.get("alternate_referral")
            )
             st.session_state.tts_audio = create_tts_audio(summary_text)
          except Exception as e:
               st.error(f"TTS error: {e}")  

        if st.session_state.get("tts_audio"):
              st.audio(st.session_state.tts_audio, format="audio/mp3")
        st.divider()
        if referral:
            st.markdown(f"**{t['refer_to']} {referral}**")

        if alternate_referral:
            st.markdown(f"**{t['alternate_referral']} {alternate_referral}**")

        concern_lines = format_additional_concerns(
            st.session_state.symptoms,
            language,
            primary_specialist=referral,
        )
        if concern_lines and not special_events:
            st.markdown("**Additional possible concerns:**" if language == "English" else "**অতিরিক্ত সম্ভাব্য সমস্যা:**")
            for line in concern_lines:
                st.write(f"- {line}")

        
      
        active_symptoms = [
    BANGLA_FEATURES.get(symptom, symptom)
    if language == "বাংলা"
    else symptom
    for symptom, value in st.session_state.symptoms.items()
    if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
]
        for extra_symptom in st.session_state.get("extra_symptoms", []):
            active_symptoms.append(
                BANGLA_FEATURES.get(extra_symptom, extra_symptom)
                if language == "বাংলা"
                else EXTRA_DISPLAY_SYMPTOMS.get(extra_symptom, {}).get("English", extra_symptom.replace("_", " ").title())
            )

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

                pdf_buffer = create_structured_referral_pdf(
                    st.session_state.ai_response,
                    st.session_state.triage_result,
                    st.session_state.symptoms,
                    referral=referral,
                    first_aid=first_aid,
                    
                )

                st.download_button(
                    label=t["download_pdf"],
                    data=pdf_buffer,
                    file_name=t["pdf_filename"],
                    mime="application/pdf"
                )
