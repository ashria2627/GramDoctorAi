import re

from modules.BanglaSymptoms import SYMPTOMS as BANGLA_SYMPTOMS

try:
    from rapidfuzz import fuzz, process
except Exception:
    fuzz = None
    process = None


ENGLISH_SYNONYMS = {
    "fever": "fever",
    "temperature": "fever",
    "high temperature": "fever",
    "cough": "cough",
    "coughing": "cough",
    "sneezing": "cough",
    "headache": "headache",
    "head ache": "headache",
    "head hurts": "headache",
    "cephalgia": "headache",
    "vomiting": "vomiting",
    "vomit": "vomiting",
    "throwing up": "vomiting",
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
    "difficulty breathing": "difficulty breathing",
    "airway issue": "difficulty breathing",
    "mouth breathing": "difficulty breathing",
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
    "throat pain": "sore throat",
    "runny nose": "nasal congestion",
    "blocked nose": "nasal congestion",
    "stuffy nose": "nasal congestion",
    "nasal congestion": "nasal congestion",
    "ear pain": "ear pain",
    "earache": "ear pain",
    "hearing loss": "diminished hearing",
    "less hearing": "diminished hearing",
    "snoring": "snoring",
    "sleep apnea": "sleep apnea",
    "obstructive sleep apnea": "sleep apnea",
    "blood in stool": "blood in stool",
    "painful urination": "painful urination",
    "burning urination": "painful urination",
    "jaundice": "jaundice",
    "nosebleed": "nosebleed",
}


def _candidate_phrases(text):
    lowered = text.lower()
    phrases = set(re.findall(r"[a-z][a-z\s-]{2,}", lowered))
    words = re.findall(r"[a-z]+", lowered)

    for size in (1, 2, 3, 4):
        for idx in range(0, max(len(words) - size + 1, 0)):
            phrases.add(" ".join(words[idx:idx + size]))

    return phrases


def normalize_symptom_input(text, feature_cols, min_score=88):
    extracted = {}

    if not text:
        return extracted

    feature_set = set(feature_cols)

    for phrase, feature_name in {**BANGLA_SYMPTOMS, **ENGLISH_SYNONYMS}.items():
        if phrase and phrase.lower() in text.lower() and feature_name in feature_set:
            extracted[feature_name] = 1

    for feature in feature_cols:
        if feature in ["age", "sex-no", "ispregnant"]:
            continue
        if feature.lower() in text.lower():
            extracted[feature] = 1

    if process is None or fuzz is None:
        return extracted

    choices = {
        phrase: feature
        for phrase, feature in ENGLISH_SYNONYMS.items()
        if feature in feature_set
    }

    for phrase in _candidate_phrases(text):
        match = process.extractOne(
            phrase,
            choices.keys(),
            scorer=fuzz.WRatio
        )
        if match and match[1] >= min_score:
            extracted[choices[match[0]]] = 1

    return extracted
