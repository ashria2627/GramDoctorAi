import re

from modules.BanglaSymptoms import SYMPTOMS as BANGLA_SYMPTOMS
from modules.text_negation import is_symptom_negated, CLAUSE_SPLIT_PATTERN
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
    "headache": "headache",
    "head ache": "headache",
    "head hurts": "headache",
    "cephalgia": "headache",
    "vomiting": "vomiting",
    "vomitting": "vomiting",
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
    "abdominal pain": "sharp abdominal pain",
    "stomach pain": "sharp abdominal pain",
    "stomach ache": "sharp abdominal pain",
    "stomachache": "sharp abdominal pain",
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
    "black stool": "blood in stool",
    "tarry stool": "blood in stool",
    "vomiting blood": "vomiting blood",
    "blood vomit": "vomiting blood",
    "painful urination": "painful urination",
    "burning urination": "painful urination",
    "frequent urination": "frequent urination",
    "frequent urine": "frequent urination",
    "jaundice": "jaundice",
    "nosebleed": "nosebleed",
    "arm pain": "arm pain",
    "arms pain": "arm pain",
    "pain in arm": "arm pain",
    "pain in arms": "arm pain",
    "hand pain": "arm pain",
    "hands pain": "arm pain",
    "leg pain": "leg pain",
    "legs pain": "leg pain",
    "pain in leg": "leg pain",
    "pain in legs": "leg pain",
    "leg swelling": "leg swelling",
    "swelling of legs": "leg swelling",
    "palpitations": "palpitations",
    "heart racing": "palpitations",
    "chills": "chills",
    "constipation": "constipation",
    "itching": "itching of skin",
    "itching skin": "itching of skin",
    "confusion": "delusions or hallucinations",
    "confused": "delusions or hallucinations",
    "difficulty swallowing": "difficulty in swallowing",
    "trouble swallowing": "difficulty in swallowing",
    "numbness": "loss of sensation",
    "tingling": "loss of sensation",
    "hurts to breathe":"hurts to breath"
}


ROMANIZED_BANGLA_SYNONYMS = {
    "jor": "fever", "jhor": "fever", "jar": "fever", "gaye jor": "fever", "kapuni": "chills",
    "matha betha": "headache", "mathay betha": "headache", "matha batha": "headache", "matha ghora": "dizziness",
    "bomi": "vomiting", "bomi hocche": "vomiting", "bomi bomi": "nausea", "vomit hocche": "vomiting",
    "durbol": "weakness", "durbolota": "weakness", "shorir durbol": "weakness", "klanti": "weakness",
    "kashi": "cough", "kasi": "cough", "khushi": "cough", "kof": "coughing up sputum", "kof utha": "coughing up sputum",
    "shash kosto": "shortness of breath", "shash nite kosto": "difficulty breathing", "dom bondho": "shortness of breath", "hapani": "wheezing",
    "buk betha": "sharp chest pain", "buke betha": "sharp chest pain", "buk chap": "chest tightness", "buk dhorfor": "palpitations",
    "pet betha": "sharp abdominal pain", "pet byatha": "sharp abdominal pain", "tolpet betha": "lower abdominal pain", "pete jala": "burning abdominal pain",
    "patla paykhana": "diarrhea", "loose motion": "diarrhea", "dairia": "diarrhea", "paykhanay rokto": "blood in stool", "kalo paykhana": "blood in stool",
    "prosrabe jala": "painful urination", "prosrabe betha": "painful urination", "ghonoghon prosrab": "frequent urination", "prosrab bondho": "retention of urine",
    "kan betha": "ear pain", "kane betha": "ear pain", "kom shuni": "diminished hearing", "kane shobdo": "ringing in ear",
    "gola betha": "sore throat", "gola boshe geche": "hoarse voice", "gila kosto": "difficulty in swallowing", "nak bondho": "nasal congestion",
    "nak diye pani": "nasal congestion", "nak jhora": "nasal congestion", "nak diye rokto": "nosebleed", "nak daka": "snoring",
    "chokh betha": "pain in eye", "chokh lal": "eye redness", "kom dekhi": "diminished vision", "chokhe jhapsha": "diminished vision",
    "khichuni": "seizures", "fit": "seizures", "oggan": "fainting", "gyan hariyeche": "fainting",
    "hat betha": "arm pain", "pa betha": "leg pain", "hatu betha": "knee pain", "pith betha": "back pain",
    "chulkani": "itching of skin", "rash": "skin rash", "fuskuri": "skin rash", "fula": "skin swelling",
    "masike beshi rokto": "heavy menstrual flow", "shada srab": "vaginal discharge", "yoni chulkani": "vaginal itching", "komor betha": "pelvic pain","lower back pain":"pelvic pain","maja betha":"pelvic pain",
    "jondis": "jaundice", "chokh holud": "jaundice", "mukh gha": "mouth ulcer", "dat betha": "toothache",
    "period pain": "painful menstruation", "painful period": "painful menstruation", "painful periods": "painful menstruation",
    "period cramps": "painful menstruation", "menstrual cramps": "painful menstruation",
    "menstruation pain": "painful menstruation", "menstrual pain": "painful menstruation",
}

ADDITIONAL_ENGLISH_SYNONYMS = {
    "high fever": "fever", "low grade fever": "fever", "body temperature": "fever", "feeling feverish": "fever",
    "migraine": "headache", "head pressure": "headache", "severe headache": "headache", "lightheaded": "dizziness", "vertigo": "dizziness",
    "tiredness": "weakness", "fatigue": "weakness", "body weakness": "weakness", "loss of energy": "weakness",
    "productive cough": "coughing up sputum", "phlegm": "coughing up sputum", "sputum": "coughing up sputum", "dry cough": "cough",
    "cannot breathe": "difficulty breathing", "hard to breathe": "difficulty breathing", "air hunger": "shortness of breath", "wheeze": "wheezing",
    "chest pressure": "chest tightness", "tight chest": "chest tightness", "heart racing": "palpitations", "irregular pulse": "irregular heartbeat",
    "stomach ache": "sharp abdominal pain", "stomach cramps": "sharp abdominal pain", "lower belly pain": "lower abdominal pain", "pelvic ache": "pelvic pain",
    "watery stool": "diarrhea", "bloody stool": "blood in stool", "blood stool": "blood in stool", "constipated": "constipation",
    "burning urine": "painful urination", "urine pain": "painful urination", "pee burning": "painful urination", "pee often": "frequent urination",
    "ear ache": "ear pain", "reduced hearing": "diminished hearing", "blocked ear": "diminished hearing", "tinnitus": "ringing in ear",
    "throat ache": "sore throat", "lost voice": "hoarse voice", "voice hoarse": "hoarse voice", "trouble swallowing": "difficulty in swallowing",
    "nasal discharge": "nasal congestion", "nose running": "nasal congestion", "runny nostril": "nasal congestion", "snore": "snoring",
    "eye pain": "pain in eye", "red eye": "eye redness", "blurry vision": "diminished vision", "vision loss": "blindness",
    "fits": "seizures", "convulsions": "seizures", "passed out": "fainting", "blackout": "fainting",
    "arm ache": "arm pain", "arms ache": "arm pain", "aching arms": "arm pain", "leg ache": "leg pain", "legs ache": "leg pain", "aching legs": "leg pain", "joint ache": "knee pain", "spine pain": "back pain",
    "skin itch": "itching of skin", "itchy skin": "itching of skin", "swollen skin": "skin swelling", "hives": "skin rash",
    "heavy period": "heavy menstrual flow", "heavy bleeding period": "heavy menstrual flow", "vaginal fluid": "vaginal discharge",
    "period pain": "painful menstruation", "painful period": "painful menstruation", "painful periods": "painful menstruation",
    "period cramps": "painful menstruation", "menstrual cramps": "painful menstruation",
    "yellow eyes": "jaundice", "yellow skin": "jaundice", "mouth sore": "mouth ulcer", "tooth pain": "toothache",
    "loss of feeling": "loss of sensation", "numbness": "loss of sensation", "tingling": "weakness", "slurred speech": "slurring words",
    "swollen leg": "leg swelling", "feet swelling": "leg swelling", "ankle swelling": "leg swelling", "testicle pain": "pain in testicles",
}


def _candidate_phrases(text):
    lowered = text.lower()
    phrases = set()

    for clause in re.split(CLAUSE_SPLIT_PATTERN, lowered):
        phrases.update(re.findall(r"[a-z][a-z\s-]{2,}", clause))
        words = re.findall(r"[a-z]+", clause)

        for size in (2, 3, 4):
            for idx in range(0, max(len(words) - size + 1, 0)):
                phrases.add(" ".join(words[idx:idx + size]))

    return phrases


def _contains_phrase(text, phrase):
    phrase = str(phrase).lower().strip()
    if not phrase:
        return False

    escaped = re.escape(phrase).replace(r"\ ", r"\s+")
    pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None


def _is_negated(text, phrase):
    return is_symptom_negated(text, phrase)


EXACT_ONLY_FEATURES = {
    "sharp chest pain",
    "chest pain",
    "chest tightness",
    "shortness of breath",
    "difficulty breathing",
    "sharp abdominal pain",
    "lower abdominal pain",
    "burning abdominal pain",
    "blood in stool",
    "blood in urine",
    "vomiting blood",
    "hemoptysis",
    "rectal bleeding",
    "painful urination",
    "frequent urination",
    "retention of urine",
    "involuntary urination",
    "pain in eye",
    "diminished vision",
    "blindness",
    "seizures",
    "fainting",
    "slurring words",
    "loss of sensation",
    "irregular heartbeat",
    "palpitations",
    "painful menstruation",
    "heavy menstrual flow",
    "spotting or bleeding during pregnancy",
    "vaginal discharge",
    "vaginal pain",
}


def normalize_symptom_input(text, feature_cols, min_score=95):
    extracted = {}

    if not text:
        return extracted

    feature_set = set(feature_cols)
    normalized_text = text.lower()

    for phrase, feature_name in {**BANGLA_SYMPTOMS, **ENGLISH_SYNONYMS, **ROMANIZED_BANGLA_SYNONYMS, **ADDITIONAL_ENGLISH_SYNONYMS}.items():
        if (
            feature_name in feature_set
            and _contains_phrase(normalized_text, phrase)
            and not _is_negated(normalized_text, phrase)
        ):
            extracted[feature_name] = 1

    for feature in feature_cols:
        if feature in ["age", "sex-no", "ispregnant"]:
            continue
        if _contains_phrase(normalized_text, feature) and not _is_negated(normalized_text, feature):
            extracted[feature] = 1

    if process is None or fuzz is None:
        return extracted

    choices = {
        phrase: feature
        for phrase, feature in {**ENGLISH_SYNONYMS, **ROMANIZED_BANGLA_SYNONYMS, **ADDITIONAL_ENGLISH_SYNONYMS}.items()
        if feature in feature_set and feature not in EXACT_ONLY_FEATURES
    }

    for phrase in _candidate_phrases(text):
        match = process.extractOne(
            phrase,
            choices.keys(),
            scorer=fuzz.WRatio
        )
        if not match or match[1] < min_score:
            continue

        canonical_phrase = match[0]
        feature = choices[canonical_phrase]

        if _is_negated(normalized_text, canonical_phrase) or _is_negated(normalized_text, phrase):
            continue

        extracted[feature] = 1

    return extracted


def validate_canonical_self_match(feature_cols):
    checked = [
        feature
        for feature in feature_cols
        if feature not in ["age", "sex-no", "ispregnant"]
    ]
    missed = [
        feature
        for feature in checked
        if normalize_symptom_input(feature, feature_cols).get(feature) != 1
    ]
    return {
        "checked": len(checked),
        "matched": len(checked) - len(missed),
        "missed": missed,
    }
