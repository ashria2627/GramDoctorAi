
LOCAL_EMERGENCY_KEYWORDS = {
    "snake bite": {
        "keywords": [
            "সাপ",
            "সাপে কামড়",
            "সাপের কামড়",
            "সাপ কামড়াইছে",
            "সাপ কামড় দিছে",
            "সাপে কাটছে",
            "সাপে কেটেছে",
            "সাপে দংশন",
            "সাপে দংশন",
            "সাপে ছোবল",
            "সাপের ছোবল",
            "সাপে ছোবল দিছে",
            "সাপে ছোবল মারছে",
            "সাপে ধরছে",
            "সাপে লাগছে",
            "সাপে খাইছে",
            "সাপে দেইছে",
            "সাপে কামড়াইছে হাতে",
            "সাপে কামড়াইছে পায়ে",
            "snake",
            "snake bite",
            "snakebite",
            "bitten by snake",
            "snake bit me",
            "snake has bitten me",
            "venomous snake bite"
        ],
        "first_aid_key": frozenset(
            ["snake bite", "weakness", "difficulty in swallowing"]
        ),
        "condition": "Snake Bite",
    },

    "animal bite": {
        "keywords": [
            "কুকুর কামড়",
            "কুকুরে কামড়াইছে",
            "কুত্তায় কামড়াইছে",
            "কুকুরে ধরছে",
            "বিড়ালের আঁচড়",
            "বিড়াল আঁচড়াইছে",
            "বিড়ালে কামড়াইছে",
            "শিয়ালে কামড়াইছে",
            "বানরে কামড়াইছে",
            "পশুর কামড়",
            "আঁচড়",
            "কামড়",
            "dog bite",
            "dog bit me",
            "cat scratch",
            "cat bite",
            "animal bite",
            'bitten by a dog',
            'bitten by a cat',
            'bit by a monkey',
            'bit by a fox',
        ],
        "first_aid_key": frozenset(
            ["animal bite", "bleeding", "pain"]
        ),
        "condition": "Animal Bite",
    },

    "burn": {
        "keywords": [
            "পোড়া",
            "পুড়ে গেছে",
            "আগুনে পুড়েছে",
            "গরম পানিতে পুড়েছে",
            "চুলায় পুড়েছে",
            "দগ্ধ",
            "গরম তেলে পুড়েছে",
            "হাত পুড়েছে",
            "শরীর পুড়েছে",
            "burn",
            "burned",
            "burnt",
            "scald"
        ],
        "first_aid_key": frozenset(
            ["burn", "blisters", "pain"]
        ),
        "condition": "Burn Injury",
    },

    "poisoning": {
        "keywords": [
            "বিষ",
            "বিষ খেয়েছে",
            "বিষ খাইছে",
            "বিষক্রিয়া",
            "কীটনাশক",
            "পেস্টিসাইড",
            "ধানের ওষুধ",
            "ধানের বিষ",
            "ইঁদুর মারার ওষুধ",
            "ইঁদুরের বিষ",
            "টয়লেট ক্লিনার খেয়েছে",
            "এসিড খেয়েছে",
            "বিষ পান করেছে",
            "poison",
            "poisoning",
            "pesticide",
            "pesticide poisoning",
            "rat poison",
            "chemical poisoning"
        ],
        "first_aid_key": frozenset(
            ["poison", "vomiting", "confusion"]
        ),
        "condition": "Poisoning",
    },

    "drowning": {
        "keywords": [
            "ডুবে গেছে",
            "পানিতে ডুবে গেছে",
            "পুকুরে ডুবে গেছে",
            "নদীতে ডুবে গেছে",
            "ডুবেছে",
            "পানিতে তলিয়ে গেছে",
            "ডুবে ছিল",
            "প্রায় ডুবে গিয়েছিল",
            "near drowning",
            "drowning",
            "almost drowned"
        ],
        "first_aid_key": frozenset(
            ["drowning", "shortness of breath", "unconsciousness"]
        ),
        "condition": "Drowning",
    },

    "fall injury": {
        "keywords": [
            "পড়ে গেছে",
            "পড়ে গিয়ে",
            "উঁচু থেকে পড়েছে",
            "সিঁড়ি থেকে পড়েছে",
            "গাছ থেকে পড়েছে",
            "বাথরুমে পড়ে গেছে",
            "পা পিছলে পড়েছে",
            "রিকশা থেকে পড়েছে",
            "মোটরসাইকেল থেকে পড়েছে",
            "fall",
            "fell down",
            "slipped",
            "slipped and fell"
        ],
        "first_aid_key": frozenset(
            ["fall injury", "pain", "swelling"]
        ),
        "condition": "Fall Injury",
    },

    "drug injection exposure": {
        "keywords": [
            "ইনজেকশন দিয়েছে",
            "ভুল ইনজেকশন",
            "সুঁই ফুটেছে",
            "সুঁই লেগেছে",
            "ব্যবহৃত সুঁই",
            "মাদক ইনজেকশন",
            "সিরিঞ্জ",
            "ইনজেকশনের পর সমস্যা",
            "needle stick",
            "needle injury",
            "used needle",
            "syringe injury",
            "drug injection",
            "injection reaction"
        ],
        "first_aid_key": frozenset(
            ["drug exposure", "pain", "swelling"]
        ),
        "condition": "Drug Injection Exposure",
    },

"electrocution": {
    "keywords": [
        "বিদ্যুৎস্পৃষ্ট",
        "কারেন্ট লেগেছে",
        "বিদ্যুৎ লেগেছে",
        "শক খেয়েছে",
        "ইলেকট্রিক শক",
        "electric shock",
        "electrocution",
        "current shock"
    ],
    "first_aid_key": frozenset(
        ["electrocution", "burn", "unconsciousness"]
    ),
    "condition": "Electrocution",
},

"rat poison": {
    "keywords": [
        "ইঁদুরের বিষ",
        "ইঁদুর মারার ওষুধ",
        "ইঁদুরের বিষ খেয়েছে",
        "ইঁদুর মারার বিষ",
        "rat poison",
        "rat poison ingestion"
    ],
    "first_aid_key": frozenset(
        ["poison", "vomiting", "confusion",'rat']
    ),
    "condition": "Rat Poisoning",
},

"fracture": {
    "keywords": [
        "হাড় ভেঙেছে",
        "হাত ভেঙেছে",
        "পা ভেঙেছে",
        "হাড় ভাঙ্গা",
        "হাড়ে ফাটল",
        "fracture",
        "broken bone",
        "bone fracture"
    ],
    "first_aid_key": frozenset(
        ["fracture", "pain", "swelling"]
    ),
    "condition": "Fracture",
},

"sprain": {
    "keywords": [
        "মচকেছে",
        "গোড়ালি মচকেছে",
        "হাত মচকেছে",
        "পা মচকেছে",
        "sprain",
        "twisted ankle",
        "twisted wrist"
    ],
    "first_aid_key": frozenset(
        ["sprain", "pain", "swelling"]
    ),
    "condition": "Sprain",
},

"heat stroke": {
    "keywords": [
        "হিট স্ট্রোক",
        "গরমে অজ্ঞান",
        "রোদে অজ্ঞান",
        "অতিরিক্ত গরমে অসুস্থ",
        "heat stroke",
        "heat exhaustion"
    ],
    "first_aid_key": frozenset(
        ["high fever", "confusion", "heat exposure"]
    ),
    "condition": "Heat Stroke",
},

"scorpion sting": {
    "keywords": [
        "বিছার কামড়",
        "বিছা কামড়েছে",
        "বিছার হুল",
        "scorpion sting",
        "scorpion bite"
    ],
    "first_aid_key": frozenset(
        ["scorpion sting", "pain", "swelling"]
    ),
    "condition": "Scorpion Sting",
},

"insect sting": {
    "keywords": [
        "মৌমাছির হুল",
        "বোলতার কামড়",
        "পোকা কামড়েছে",
        "মৌমাছি কামড়েছে",
        "বোলতা কামড়েছে",
        "bee sting",
        "wasp sting",
        "insect bite",
        "insect sting"
    ],
    "first_aid_key": frozenset(
        ["insect sting", "swelling", "shortness of breath"]
    ),
    "condition": "Insect Sting",
},

"hook injury": {
    "keywords": [
        "বড়শি ফুটেছে",
        "বড়শি লেগেছে",
        "মাছ ধরার বড়শি",
        "বড়শিতে হাত ফুটেছে",
        "fish hook injury",
        "fishhook injury",
        "hook injury"
    ],
    "first_aid_key": frozenset(
        ["hook injury", "bleeding", "pain"]
    ),
    "condition": "Fish Hook Injury",
},

}


def detect_local_emergency(text, SYMPTOM_FIRST_AID):
    if not text:
        return None

    lowered = text.lower()

    for category, data in LOCAL_EMERGENCY_KEYWORDS.items():
        for kw in data["keywords"]:
            if kw.lower() in lowered:
                advice = SYMPTOM_FIRST_AID.get(data["first_aid_key"])
                if not advice:
                    continue
                return {
                    "found": True,
                    "condition": data["condition"],
                    "color": "red",
                    "advice_en": advice.get("steps_en", []),
                    "advice_bn": advice.get("steps_bn", []),
                }

    return None