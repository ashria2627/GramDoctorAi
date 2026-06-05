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


def generate_ai_response(symptoms, triage_result):
    client = get_gemini_client()

    if client is None:
        return "Gemini API key missing. Please add GEMINI_API_KEY to your .env file."

    active_symptoms = get_active_symptoms(symptoms)
    color = triage_result["color"]

    prompt = f"""
You are GramDoctor AI, a rural Bangladesh triage and referral assistant.

Rules:
- Do not give a final diagnosis.
- Do not prescribe medicine.
- Do not say the patient is safe if emergency symptoms are present.
- Use simple Bangla for patient-facing explanation.
- Referral note must be in professional English.
- Keep the response short, safe, and structured.

Patient data:
Age: {symptoms.get("age", "unknown")}
Sex code: {symptoms.get("sex-no", "unknown")}
Pregnancy code: {symptoms.get("ispregnant", "unknown")}
Active symptoms: {active_symptoms}

Triage result: {color}
Decision source: {triage_result["source"]}
Reason: {triage_result["message"]}

Return exactly in this format:

Bangla Explanation:
...

Immediate Advice:
...

What Not To Do:
...

Referral Note:
...
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text