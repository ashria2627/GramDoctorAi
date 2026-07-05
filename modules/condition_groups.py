CONDITION_GROUPS = [
    {
        "key": "diabetes_pattern",
        "color": "orange",
        "min_matches": 2,
        "symptoms": {"frequent urination", "excessive_thirst", "increased_appetite", "weight_loss", "weakness", "fatigue"},
        "source_en": "Grouped symptom pattern - Diabetes risk",
        "source_bn": "সমন্বিত লক্ষণ - ডায়াবেটিস ঝুঁকি",
        "message_en": "Frequent urination, thirst, appetite or weight change together may suggest diabetes risk. Please check blood sugar and see a doctor.",
        "message_bn": "বারবার প্রস্রাব, বেশি তৃষ্ণা, ক্ষুধা বা ওজন পরিবর্তন একসাথে থাকলে ডায়াবেটিসের ঝুঁকি থাকতে পারে। রক্তে সুগার পরীক্ষা করুন এবং ডাক্তার দেখান।",
    },
    {
        "key": "pcos_pattern",
        "color": "orange",
        "min_matches": 3,
        "sex": "female",
        "symptoms": {"irregular_periods", "missed_period", "hair_loss", "weight_gain", "heavy menstrual flow"},
        "source_en": "Grouped symptom pattern - PCOS or hormonal disorder risk",
        "source_bn": "সমন্বিত লক্ষণ - PCOS বা হরমোনজনিত সমস্যা ঝুঁকি",
        "message_en": "Irregular or missed periods with hair loss, weight gain, or heavy bleeding may suggest PCOS or a hormonal disorder. A gynecology review is recommended.",
        "message_bn": "অনিয়মিত/বন্ধ মাসিকের সাথে চুল পড়া, ওজন বাড়া বা অতিরিক্ত রক্তপাত থাকলে PCOS বা হরমোনজনিত সমস্যা হতে পারে। গাইনি ডাক্তারের পরামর্শ নিন।",
    },
    {
        "key": "tb_pattern",
        "color": "orange",
        "min_matches": 3,
        "symptoms": {"cough", "night_sweats", "weight_loss", "decreased appetite", "hemoptysis"},
        "source_en": "Grouped symptom pattern - TB or chronic infection risk",
        "source_bn": "সমন্বিত লক্ষণ - যক্ষা বা দীর্ঘস্থায়ী সংক্রমণ ঝুঁকি",
        "message_en": "Cough or fever with night sweats, weight loss, appetite loss, or blood in sputum may suggest TB or another chronic infection. Medical testing is recommended.",
        "message_bn": "কাশি বা জ্বরের সাথে রাতে ঘাম, ওজন কমা, ক্ষুধামন্দা বা কফে রক্ত থাকলে যক্ষা বা দীর্ঘস্থায়ী সংক্রমণ হতে পারে। পরীক্ষা দরকার।",
    },
    {
        "key": "anemia_pattern",
        "color": "orange",
        "min_matches": 3,
        "symptoms": {"weakness", "fatigue", "palpitations", "fainting", "heavy menstrual flow", "decreased appetite"},
        "source_en": "Grouped symptom pattern - Anemia risk",
        "source_bn": "সমন্বিত লক্ষণ - রক্তস্বল্পতার ঝুঁকি",
        "message_en": "Weakness or tiredness with palpitations, fainting, appetite loss, or heavy periods may suggest anemia. A blood test and doctor review are recommended.",
        "message_bn": "দুর্বলতা বা ক্লান্তির সাথে বুক ধড়ফড়, অজ্ঞান হওয়া, ক্ষুধামন্দা বা অতিরিক্ত মাসিক থাকলে রক্তস্বল্পতা হতে পারে। রক্ত পরীক্ষা ও ডাক্তার দেখানো দরকার।",
    },
    {
        "key": "kidney_urinary_pattern",
        "color": "orange",
        "min_matches": 3,
        "symptoms": {"leg swelling", "facial_swelling", "reduced_urine_output", "blood in urine", "painful urination", "frequent urination"},
        "source_en": "Grouped symptom pattern - Kidney or urinary problem risk",
        "source_bn": "সমন্বিত লক্ষণ - কিডনি বা প্রস্রাবের সমস্যা ঝুঁকি",
        "message_en": "Swelling, reduced urine, blood in urine, or urinary pain/frequency together may suggest kidney or urinary disease. Please see a doctor.",
        "message_bn": "ফোলা, প্রস্রাব কমে যাওয়া, প্রস্রাবে রক্ত, প্রস্রাবে জ্বালা বা বারবার প্রস্রাব একসাথে থাকলে কিডনি/প্রস্রাবের সমস্যা হতে পারে। ডাক্তার দেখান।",
    },
    {
        "key": "gi_bleeding_pattern",
        "color": "red",
        "min_matches": 3,
        "symptoms": {"black_stool", "vomiting blood", "dizziness", "fainting"},
        "source_en": "Grouped symptom pattern - Possible gastrointestinal bleeding",
        "source_bn": "সমন্বিত লক্ষণ - পেট/পরিপাকতন্ত্রে রক্তক্ষরণের সম্ভাবনা",
        "message_en": "Black stool or vomiting blood with weakness, dizziness, or fainting can indicate gastrointestinal bleeding. Go to hospital urgently.",
        "message_bn": "কালো পায়খানা বা রক্তবমির সাথে দুর্বলতা, মাথা ঘোরা বা অজ্ঞান হলে পরিপাকতন্ত্রে রক্তক্ষরণ হতে পারে। জরুরি ভিত্তিতে হাসপাতালে যান।",
    },
    {
        "key": "thyroid_pattern",
        "color": "orange",
        "min_matches": 3,
        "symptoms": {"weight_gain", "weight_loss", "hair_loss", "palpitations", "heat_intolerance", "cold_intolerance", "fatigue"},
        "source_en": "Grouped symptom pattern - Thyroid or hormonal disorder risk",
        "source_bn": "সমন্বিত লক্ষণ - থাইরয়েড বা হরমোনজনিত সমস্যা ঝুঁকি",
        "message_en": "Weight change, hair loss, palpitations, temperature intolerance, or fatigue together may suggest a thyroid or hormonal disorder. Doctor review is recommended.",
        "message_bn": "ওজন পরিবর্তন, চুল পড়া, বুক ধড়ফড়, ঠান্ডা/গরম সহ্য না হওয়া বা ক্লান্তি একসাথে থাকলে থাইরয়েড বা হরমোনজনিত সমস্যা হতে পারে। ডাক্তার দেখান।",
    },
]

COLOR_ORDER = {"gray": 0, "green": 1, "orange": 3, "red": 4}


def _active_set(symptoms, extra_symptoms):
    active = {
        key
        for key, value in (symptoms or {}).items()
        if value == 1 and key not in {"age", "sex-no", "ispregnant"}
    }
    active.update(extra_symptoms or [])
    return active


def detect_condition_groups(symptoms, extra_symptoms=None, lang="English"):
    active = _active_set(symptoms, extra_symptoms)
    sex_is_female = (symptoms or {}).get("sex-no") == 1
    matches = []

    for group in CONDITION_GROUPS:
        if group.get("sex") == "female" and not sex_is_female:
            continue

        matched = sorted(active.intersection(group["symptoms"]))
        if len(matched) >= group["min_matches"]:
            matches.append({
                "key": group["key"],
                "color": group["color"],
                "source": group["source_en"] if lang == "English" else group["source_bn"],
                "message": group["message_en"] if lang == "English" else group["message_bn"],
                "matched": matched,
            })

    return sorted(
        matches,
        key=lambda item: (COLOR_ORDER.get(item["color"], 0), len(item["matched"])),
        reverse=True,
    )


def apply_condition_group_rules(symptoms, result, extra_symptoms=None, lang="English"):
    matches = detect_condition_groups(symptoms, extra_symptoms, lang)
    if not matches:
        return result, []

    top_match = matches[0]
    current_color = str((result or {}).get("color", "gray")).lower()
    if COLOR_ORDER.get(top_match["color"], 0) > COLOR_ORDER.get(current_color, 0):
        updated = dict(result or {})
        updated.update({
            "color": top_match["color"],
            "source": top_match["source"],
            "message": top_match["message"],
            "confidence": None,
        })
        return updated, matches

    return result, matches
