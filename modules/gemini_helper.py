import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

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

    prompt = f"""
You are GramDoctor AI, a rural Bangladesh triage and referral assistant.

IMPORTANT SAFETY RULE:
If any symptom indicates emergency danger (e.g. breathing difficulty, chest pain, fainting, seizures), treat it as high priority even if system output suggests otherwise.

Rules:
- Do not give a final diagnosis.
- Do not prescribe medicine.
- Do not claim patient is safe in emergency cases.
- Use simple Bangla for patient explanation.
- Referral note must be in English and Bangla.
- Keep response short and structured.

Patient data:
Age: {symptoms.get("age", "unknown")}
Sex code: {symptoms.get("sex-no", "unknown")}
Pregnancy code: {symptoms.get("ispregnant", "unknown")}
Active symptoms: {active_symptoms}

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
