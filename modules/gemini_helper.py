import os
from dotenv import load_dotenv
from google import genai
from modules.Followup import FOLLOWUP_GROUPS
import streamlit as st
import json

load_dotenv()


def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")  

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def get_active_symptoms(symptoms):
    active = []

    for key, value in symptoms.items():
        if value == 1:
            active.append(key)

    if not active:
        return "No major symptoms selected."

    return ", ".join(active)


def get_fallback_response(triage_result, error_message):
    color = triage_result["color"]

    if color == "green":
        fallback = """
Bangla Explanation:
আপনার দেওয়া তথ্য অনুযায়ী লক্ষণগুলো আপাতত কম ঝুঁকিপূর্ণ মনে হচ্ছে। তবে এটি কোনো চূড়ান্ত রোগ নির্ণয় নয়।

Immediate Advice:
বাসায় বিশ্রাম নিন, পর্যাপ্ত পানি পান করুন এবং লক্ষণ পর্যবেক্ষণ করুন। লক্ষণ বাড়লে চিকিৎসকের পরামর্শ নিন।

What Not To Do:
লক্ষণ খারাপ হলে বা নতুন বিপদজনক লক্ষণ দেখা দিলে বাসায় অপেক্ষা করবেন না।

Referral Note:
Patient currently has low-risk symptoms based on triage input. Home observation advised with medical follow-up if symptoms worsen.
"""

    elif color == "orange":
        fallback = """
Bangla Explanation:
আপনার লক্ষণগুলো চিকিৎসকের মূল্যায়ন প্রয়োজন হতে পারে। এটি জরুরি অবস্থা নাও হতে পারে, তবে দেরি করা উচিত নয়।

Immediate Advice:
১–২ দিনের মধ্যে নিকটস্থ ডাক্তার, ক্লিনিক বা উপজেলা স্বাস্থ্য কমপ্লেক্সে যান।

What Not To Do:
নিজে নিজে অ্যান্টিবায়োটিক, ব্যথার ওষুধ বা ঝুঁকিপূর্ণ ওষুধ খাবেন না।

Referral Note:
Patient symptoms require non-emergency medical evaluation within 24–48 hours. Clinical review is advised.
"""

    else:
        fallback = """
Bangla Explanation:
আপনার লক্ষণগুলোর মধ্যে জরুরি বিপদ সংকেত থাকতে পারে। দ্রুত চিকিৎসা নেওয়া প্রয়োজন।

Immediate Advice:
এখনই নিকটস্থ হাসপাতাল বা জরুরি বিভাগে যান।

What Not To Do:
বাসায় অপেক্ষা করবেন না এবং চিকিৎসা নিতে দেরি করবেন না।

Referral Note:
Patient has emergency-level triage features. Immediate emergency medical evaluation is recommended.
"""

    return fallback + f"\n\nTechnical note: Gemini unavailable. {error_message}"


def generate_ai_response(symptoms, triage_result):
    client = get_gemini_client()

    if client is None:
        return "Gemini API key missing. Please add GEMINI_API_KEY to your .env file."

    active_symptoms = get_active_symptoms(symptoms)
    color = triage_result["color"]
    followup_text = "\n".join(f"{k}: {v}" for k,v in symptoms.items() if k.split("_")[0] in FOLLOWUP_GROUPS and v)
    prompt = f"""
You are GramDoctor AI, a rural Bangladesh triage and referral assistant.

IMPORTANT SAFETY RULE:
If any symptom indicates emergency danger (e.g. breathing difficulty, chest pain, fainting, seizures), treat it as high priority even if system output suggests otherwise.

Rules:
- Do not give a final diagnosis.
- Do not prescribe medicine.
- Do not claim patient is safe in emergency cases.

- If triage signal is RED OR emergency injury/event is present (e.g. snake bite, dog bite, animal bite, burn, poison, drowning, chest pain, breathing difficulty,appendicitis):
  → Generate possible diseases or differential diagnosis
  → Speculate medical conditions
  → Provide:
     • immediate danger explanation
     • simple first aid (if safe)
     • urgent instruction to go to hospital immediately

- Use simple Bangla for patient explanation.
- Referral note must be in English and Bangla.
- Keep response short and structured.

Patient data:
Age: {symptoms.get("age", "unknown")}
Sex code: {symptoms.get("sex-no", "unknown")}
Pregnancy code: {symptoms.get("ispregnant", "unknown")}
Active symptoms: {active_symptoms}
Additional details : {followup_text}
System triage signal: {color}
System notes: {triage_result["message"]}

Return exactly in this format:

Bangla Explanation:
...

Immediate Advice:
...

What Not To Do:
...

Possible diagnosis (not final):
...

Referral Note Bangla:
...

Referral Note English:
...
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return get_fallback_response(triage_result, str(e))


def detect_special_emergency(text):
    """
    Handles symptoms/events NOT in our dataset (animal bites, burns, falls,
    insect stings, wounds, etc.) by asking Gemini to classify the situation.
    Works for free-text input in Bangla or English (typed, voice-transcribed,
    or extracted from an uploaded file).

    Returns a dict:
        {
            "found": bool,
            "condition": str,        # short condition name, e.g. "Dog Bite"
            "color": "red"/"orange"/"green",
            "advice_en": [list of first aid steps in English],
            "advice_bn": [list of first aid steps in Bangla],
        }
    or {"found": False} if nothing relevant was detected (true gray case).
    """

    if not text or not text.strip():
        return {"found": False}

    client = get_gemini_client()
    if client is None:
        return {"found": False}

    prompt = f"""You are a medical triage assistant for rural Bangladesh.

Patient text (Bangla or English, possibly from voice or a note): "{text}"

Some words in this text may already match our structured symptom dataset
(like fever, vomiting, etc.) — ignore those. Your job is ONLY to check if the
text ALSO describes an injury or event NOT covered by simple symptoms, such as:
animal/dog/cat/snake bite, insect/bee/wasp sting, burn, cut/wound, fall,
drowning, poisoning, electric shock, drug overdose, needle/injection injury.

If such an injury/event IS mentioned (even alongside other symptoms like fever),
respond with ONLY this JSON:
{{
  "found": true,
  "condition": "...",
  "color": "red"/"orange"/"green",
  "advice_en": [...],
  "advice_bn": [...]
}}

If NO such injury/event is mentioned at all (only ordinary symptoms like fever, cough, etc.), respond with ONLY:
{{"found": false}}
Triage color rules:
- "red": severe/venomous animal bite, deep wound with heavy bleeding, severe burn, drowning, poisoning, electric shock, suspected rabies exposure, fall with suspected fracture or head injury
- "orange": moderate injury needing a doctor within 1-2 days (small animal bite needing rabies vaccine check, moderate burn, deep cut, insect sting with swelling)
- "green": minor injury manageable at home (small scratch, minor bruise, small insect bite with no allergic reaction)

advice_en and advice_bn must be practical first-aid steps a family member can do right now,
and must end with guidance on whether/when to seek medical care.

If the text does not describe any medical event or injury at all, respond with ONLY:
{{"found": false}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        data = json.loads(raw)

        if not data.get("found"):
            return {"found": False}

        color = str(data.get("color", "orange")).strip().lower()
        if color not in ("red", "orange", "green"):
            color = "orange"

        return {
            "found": True,
            "condition": data.get("condition", "Unidentified Injury"),
            "color": color,
            "advice_en": data.get("advice_en", []),
            "advice_bn": data.get("advice_bn", []),
        }

    except Exception as e:
      print(f"[Gemini Error] detect_special_emergency: {e}")
      return {"found": False}