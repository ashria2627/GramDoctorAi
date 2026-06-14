LOCAL_EMERGENCY_KEYWORDS = {
    "snake bite": {
        "keywords": ["সাপ", "snake bite", "সাপে কামড়", "সাপের কামড়"],
        "special_key": "snake_bite",
        "condition": "Snake Bite",
        "color": "red",
    },
    "animal bite": {
        "keywords": ["কুকুর", "বিড়াল", "dog bite", "cat scratch", "animal bite", "কামড়", "আঁচড়"],
        "special_key": "animal_bite",
        "condition": "Animal Bite",
        "color": "red",
    },
    "burn": {
        "keywords": ["পোড়া", "পুড়ে", "burn", "scald", "দগ্ধ"],
        "special_key": "burn",
        "condition": "Burn Injury",
        "color": "orange",
    },
    "poison": {
        "keywords": ["বিষ", "poison", "পেস্টিসাইড", "pesticide", "কীটনাশক"],
        "special_key": "poison",
        "condition": "Poisoning",
        "color": "red",
    },
    "drowning": {
        "keywords": ["ডুবে", "drowning", "পানিতে ডুবে"],
        "special_key": "drowning",
        "condition": "Drowning",
        "color": "red",
    },
    "fracture": {
        "keywords": ["হাড় ভাঙা", "fracture", "ভেঙে গেছে", "broken bone"],
        "special_key": "fracture",
        "condition": "Possible Fracture",
        "color": "orange",
    },
    "sprain": {
        "keywords": ["মচকানো", "sprain", "twisted", "মচকে গেছে"],
        "special_key": "sprain",
        "condition": "Possible Sprain",
        "color": "green",
    },
    "heat stroke": {
        "keywords": ["হিট স্ট্রোক", "heat stroke", "রোদে পড়া", "sunstroke"],
        "special_key": "heat_stroke",
        "condition": "Possible Heat Stroke",
        "color": "red",
    },
    "scorpion sting": {
        "keywords": ["বিচ্ছু", "scorpion", "কাঁকড়াবিছা"],
        "special_key": "scorpion_sting",
        "condition": "Possible Scorpion Sting",
        "color": "orange",
    },
    "insect sting": {
        "keywords": ["মৌমাছি", "wasp", "bee sting", "insect bite", "পোকার কামড়"],
        "special_key": "insect_sting",
        "condition": "Insect Sting",
        "color": "orange",
    },
    "fall injury": {
        "keywords": ["পড়ে গেছি", "fell down", "fall", "পিছলে পড়া", "slipped"],
        "special_key": "fall_injury",
        "condition": "Fall Injury",
        "color": "orange",
    },
    "drug exposure": {
        "keywords": ["ইনজেকশন", "needle", "drug inject", "নেশার সুঁই", "সিরিঞ্জ"],
        "special_key": "drug_injection_exposure",
        "condition": "Drug Injection Exposure",
        "color": "orange",
    },
    "electrocution": {
        "keywords": ["বিদ্যুৎ", "electric shock", "electrocution", "বৈদ্যুতিক"],
        "special_key": "electrocution",
        "condition": "Possible Electrocution",
        "color": "red",
    },
}


def detect_local_emergency(text, SPECIAL_FIRST_AID):
    if not text:
        return None

    lowered = text.lower()

    for category, data in LOCAL_EMERGENCY_KEYWORDS.items():
        for kw in data["keywords"]:
            if kw.lower() in lowered:
                key = data["special_key"]
                advice = SPECIAL_FIRST_AID.get(key)
                if not advice:
                    continue
                return {
                    "found": True,
                    "condition": data["condition"],
                    "color": data["color"],
                    "advice_en": advice.get("steps_en", []),
                    "advice_bn": advice.get("steps_bn", []),
                }

    return None