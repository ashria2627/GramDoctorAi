import os
import unicodedata
import pandas as pd
from urllib.parse import quote

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "recommended_doctors.csv")


def _is_bangla_mode(language):
    normalized = unicodedata.normalize("NFC", str(language or "")).strip()
    return normalized == "বাংলা" or normalized.lower() in ("bangla", "bn", "bn-bd")


def _is_usable_bangla(text):
    if pd.isna(text):
        return False
    text = str(text).strip()
    if not text:
        return False
    stripped = text.replace(" ", "")
    if not stripped:
        return False
    return stripped.count("?") / len(stripped) < 0.3


def find_doctors(specialist_name, language="English", limit=5):
    df = pd.read_csv(CSV_PATH)
    matched = df[df["specialist_en"] == specialist_name].sort_values("rating", ascending=False)

    bangla_mode = _is_bangla_mode(language)

    results = []
    for _, row in matched.head(limit).iterrows():
        name = row["Name_bn"] if bangla_mode and _is_usable_bangla(row["Name_bn"]) else row["Name_en"]
        hospital = row["hospital_bn"] if bangla_mode and _is_usable_bangla(row["hospital_bn"]) else row["hospital_en"]
        results.append({
            "name": name,
            "hospital": hospital,
            "speciality": row["Speciality"],
            "profile_url": row["profile_url"],
        })
    return results


def google_search_url(specialist_name):
    return f"https://www.google.com/search?q=best+{quote(specialist_name)}+near+me"