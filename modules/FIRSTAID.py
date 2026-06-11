SYMPTOM_FIRST_AID = {
    frozenset(["sharp chest pain", "sweating", "shortness of breath"]): {
        "condition": "Possible Cardiac Emergency",
        "steps_en": [
            "Call 999 immediately",
            "Have patient sit or lie down — do not let them walk",
            "Loosen tight clothing around chest and neck",
            "If patient is conscious, give aspirin 300mg if available and not allergic",
            "Do not leave patient alone",
        ],
        "steps_bn": [
            "এখনই ৯৯৯ নম্বরে ফোন করুন",
            "রোগীকে বসান বা শুইয়ে দিন — হাঁটাবেন না",
            "বুক ও গলার চারপাশের পোশাক আলগা করুন",
            "সচেতন থাকলে অ্যাসপিরিন ৩০০মিগ্রা দিন (অ্যালার্জি না থাকলে)",
            "রোগীকে একা রাখবেন না",
        ]
    },
    frozenset(["fever", "vomiting", "sharp abdominal pain"]): {
        "condition": "Possible Dengue Warning",
        "steps_en": [
            "Give oral saline (ORS) every 30 minutes",
            "Do NOT give ibuprofen or aspirin — worsens dengue bleeding",
            "Paracetamol only for fever control",
            "Record urine output — reduced urination is a danger sign",
            "Go to hospital today",
        ],
        "steps_bn": [
            "প্রতি ৩০ মিনিটে খাবার স্যালাইন দিন",
            "আইবুপ্রোফেন বা অ্যাসপিরিন দেবেন না",
            "জ্বরের জন্য শুধু প্যারাসিটামল দিন",
            "প্রস্রাব কমে গেলে বিপদ সংকেত",
            "আজই হাসপাতালে যান",
        ]
    },
    frozenset(["slurring words"]): {
        "condition": "Possible Stroke",
        "steps_en": [
            "Call 999 immediately — every minute matters",
            "Note the exact time symptoms started",
            "Do not give food or water",
            "Lay patient on their side if vomiting",
            "Do not give aspirin for stroke",
        ],
        "steps_bn": [
            "এখনই ৯৯৯ নম্বরে ফোন করুন",
            "লক্ষণ শুরুর সময় নোট করুন",
            "কিছু খাওয়াবেন না",
            "বমি হলে পাশে শুইয়ে দিন",
            "স্ট্রোকে অ্যাসপিরিন দেবেন না",
        ]
    },
    frozenset(["seizures"]): {
        "condition": "Seizure",
        "steps_en": [
            "Clear area of hard objects — protect from injury",
            "Do NOT hold the person down or put anything in mouth",
            "Turn patient on their side after seizure stops",
            "Time the seizure — if over 5 minutes call 999",
            "Stay until fully conscious",
        ],
        "steps_bn": [
            "আশেপাশের শক্ত জিনিস সরিয়ে দিন",
            "রোগীকে চেপে ধরবেন না, মুখে কিছু দেবেন না",
            "খিঁচুনি থামলে পাশে শুইয়ে দিন",
            "৫ মিনিটের বেশি হলে ৯৯৯ ডাকুন",
            "পুরোপুরি সচেতন না হওয়া পর্যন্ত পাশে থাকুন",
        ]
    },
    frozenset(["diarrhea", "vomiting"]): {
        "condition": "Dehydration Risk",
        "steps_en": [
            "Give ORS (oral saline) after every loose stool",
            "Small frequent sips of clean water",
            "Avoid solid food until vomiting stops",
            "Watch for sunken eyes, no tears, dry mouth — go to hospital",
            "No antibiotics without prescription",
        ],
        "steps_bn": [
            "প্রতিটি পাতলা পায়খানার পর খাবার স্যালাইন দিন",
            "অল্প অল্প করে বিশুদ্ধ পানি দিন",
            "বমি না থামা পর্যন্ত শক্ত খাবার দেবেন না",
            "চোখ বসে যাওয়া, মুখ শুকানো — হাসপাতালে যান",
            "ডাক্তার ছাড়া অ্যান্টিবায়োটিক নয়",
        ]
    },
    frozenset(["pain in eye", "diminished vision"]): {
        "condition": "Possible Eye Injury / Sudden Vision Loss",
        "steps_en": [
            "Do not rub or press the eye",
            "Cover the eye loosely with a clean cloth",
            "Do not try to remove any object stuck in the eye",
            "Avoid bright light exposure",
            "Go to hospital today — sudden vision loss is urgent",
        ],
        "steps_bn": [
            "চোখ ঘষবেন না বা চাপ দেবেন না",
            "পরিষ্কার কাপড় দিয়ে হালকাভাবে চোখ ঢেকে দিন",
            "চোখে আটকে থাকা কোনো কিছু বের করার চেষ্টা করবেন না",
            "তীব্র আলো এড়িয়ে চলুন",
            "আজই হাসপাতালে যান — হঠাৎ দৃষ্টিশক্তি কমে যাওয়া জরুরি",
        ]
    },
    frozenset(["snake bite", "weakness", "difficulty in swallowing"]): {
        "condition": "Possible Snake Bite",
        "steps_en": [
            "Keep patient still — movement spreads venom faster",
            "Remove tight clothing/jewelry near the bite",
            "Keep bitten limb at or below heart level",
            "Do NOT cut, suck, or apply ice/tourniquet",
            "Go to hospital immediately — note time of bite",
        ],
        "steps_bn": [
            "রোগীকে নড়াচড়া করতে দেবেন না — বিষ দ্রুত ছড়াবে",
            "কামড়ের কাছে আংটি বা টাইট পোশাক খুলে ফেলুন",
            "কামড়ের অঙ্গ হৃদপিণ্ডের সমান বা নিচে রাখুন",
            "কাটবেন না, চুষবেন না, বরফ বা বাঁধন দেবেন না",
            "এখনই হাসপাতালে যান — কামড়ের সময় নোট করুন",
        ]
    },
    
frozenset(["burn", "blisters", "pain"]): {
    "condition": "Burn Injury",
    "steps_en": [
        "Cool the burn under running water for 20 minutes",
        "Remove rings or tight clothing before swelling starts",
        "Cover with a clean cloth or sterile dressing",
        "Do NOT apply toothpaste, oil, or ice",
        "Seek medical care for large or severe burns",
    ],
    "steps_bn": [
        "২০ মিনিট ধরে ঠান্ডা প্রবাহমান পানিতে পোড়া স্থান ধুয়ে নিন",
        "ফোলা শুরু হওয়ার আগে আংটি বা টাইট পোশাক খুলুন",
        "পরিষ্কার কাপড় বা জীবাণুমুক্ত ড্রেসিং দিয়ে ঢেকে রাখুন",
        "টুথপেস্ট, তেল বা বরফ ব্যবহার করবেন না",
        "গুরুতর বা বড় পোড়ায় দ্রুত চিকিৎসা নিন",
    ]
},

frozenset(["poison", "vomiting", "confusion"]): {
    "condition": "Possible Poisoning",
    "steps_en": [
        "Move the person away from the poison source",
        "If conscious, rinse the mouth with water",
        "Do NOT induce vomiting unless instructed by a doctor",
        "Keep any medicine bottle or poison container for identification",
        "Go to the nearest hospital immediately",
    ],
    "steps_bn": [
        "রোগীকে বিষের উৎস থেকে দূরে সরিয়ে নিন",
        "সচেতন থাকলে মুখ পানি দিয়ে ধুয়ে দিন",
        "ডাক্তারের নির্দেশ ছাড়া বমি করানোর চেষ্টা করবেন না",
        "ওষুধ বা বিষের পাত্র সংরক্ষণ করুন যাতে শনাক্ত করা যায়",
        "দ্রুত নিকটস্থ হাসপাতালে নিয়ে যান",
    ]
},

frozenset(["drowning", "shortness of breath", "unconsciousness"]): {
    "condition": "Near Drowning",
    "steps_en": [
        "Remove the person from the water safely",
        "Call emergency services immediately",
        "Check breathing and begin CPR if not breathing",
        "Keep the person warm and lying flat",
        "Even if recovered, seek urgent medical attention",
    ],
    "steps_bn": [
        "নিরাপদভাবে রোগীকে পানি থেকে তুলে আনুন",
        "অবিলম্বে জরুরি সহায়তা ডাকুন",
        "শ্বাস পরীক্ষা করুন এবং শ্বাস না থাকলে CPR শুরু করুন",
        "রোগীকে গরম রাখুন এবং শুইয়ে রাখুন",
        "সুস্থ মনে হলেও দ্রুত হাসপাতালে নিয়ে যান",
    ]
},

frozenset(["animal bite", "bleeding", "pain"]): {
    "condition": "Animal Bite",
    "steps_en": [
        "Wash the wound thoroughly with soap and running water for 15 minutes",
        "Apply pressure to stop bleeding",
        "Cover with a clean dressing",
        "Do NOT ignore even small bites due to rabies risk",
        "Go to hospital for rabies vaccine and tetanus protection",
    ],
    "steps_bn": [
        "১৫ মিনিট ধরে সাবান ও প্রবাহমান পানি দিয়ে ক্ষত ভালোভাবে ধুয়ে নিন",
        "রক্তপাত বন্ধ করতে চাপ দিন",
        "পরিষ্কার ব্যান্ডেজ দিয়ে ঢেকে রাখুন",
        "রেবিসের ঝুঁকির কারণে ছোট কামড়ও অবহেলা করবেন না",
        "রেবিস টিকা ও টিটেনাসের জন্য হাসপাতালে যান",
    ]
},
    frozenset(["sharp abdominal pain", "vomiting", "constipation"]): {
        "condition": "Possible Bowel Obstruction / Hernia Emergency",
        "steps_en": [
            "Do not give food or water by mouth",
            "Do not give laxatives or pain medicine",
            "Have patient lie down in a comfortable position",
            "Watch for fever or worsening pain",
            "Go to hospital today — do not delay",
        ],
        "steps_bn": [
            "মুখে কোনো খাবার বা পানি দেবেন না",
            "জোলাপ বা ব্যথার ওষুধ দেবেন না",
            "রোগীকে আরামদায়ক ভঙ্গিতে শুইয়ে দিন",
            "জ্বর বা ব্যথা বাড়ছে কিনা লক্ষ্য করুন",
            "আজই হাসপাতালে যান — দেরি করবেন না",
        ]
    },
    frozenset(["leg swelling", "shortness of breath", "sharp chest pain"]): {
        "condition": "Possible Blood Clot in Lung",
        "steps_en": [
            "Call 999 immediately",
            "Keep patient resting — do not let them walk or exert",
            "Do not massage the swollen leg",
            "Loosen tight clothing",
            "Go to hospital immediately",
        ],
        "steps_bn": [
            "এখনই ৯৯৯ নম্বরে ফোন করুন",
            "রোগীকে বিশ্রামে রাখুন — হাঁটতে দেবেন না",
            "ফোলা পা ম্যাসাজ করবেন না",
            "টাইট পোশাক আলগা করুন",
            "এখনই হাসপাতালে যান",
        ]
    },
    frozenset(["delusions or hallucinations", "fever", "headache"]): {
        "condition": "Possible Meningitis / Severe Infection",
        "steps_en": [
            "Keep patient in a quiet, dim room — bright light worsens headache",
            "Give paracetamol for fever, avoid aspirin",
            "Keep patient hydrated with small sips of water",
            "Watch for stiff neck or rash — call 999 if present",
            "Go to hospital today — do not wait",
        ],
        "steps_bn": [
            "শান্ত, কম আলোর ঘরে রাখুন — তীব্র আলো মাথাব্যথা বাড়ায়",
            "জ্বরের জন্য প্যারাসিটামল দিন, অ্যাসপিরিন নয়",
            "অল্প অল্প পানি দিয়ে হাইড্রেট রাখুন",
            "ঘাড় শক্ত হওয়া বা র‍্যাশ দেখলে ৯৯৯ ডাকুন",
            "আজই হাসপাতালে যান — দেরি করবেন না",
        ]
    },
    frozenset(["spotting or bleeding during pregnancy"]): {
        "condition": "Possible Pregnancy Emergency",
        "steps_en": [
            "Have patient lie down on her left side",
            "Do not insert anything into the vagina",
            "Count and note number of pads used",
            "Keep her warm and calm",
            "Go to hospital immediately — call 999 if heavy bleeding",
        ],
        "steps_bn": [
            "রোগীকে বাম পাশ হয়ে শুইয়ে দিন",
            "যোনিপথে কিছু প্রবেশ করাবেন না",
            "কতটা প্যাড ব্যবহার হচ্ছে তা গুনুন",
            "তাকে গরম ও শান্ত রাখুন",
            "এখনই হাসপাতালে যান — বেশি রক্তক্ষরণ হলে ৯৯৯ ডাকুন",
        ]
    },
    frozenset(["retention of urine", "lower abdominal pain"]): {
        "condition": "Possible Urinary Retention",
        "steps_en": [
            "Do not press hard on the lower abdomen",
            "Encourage patient to try sitting upright to urinate",
            "Apply a warm cloth to lower abdomen if comfortable",
            "Do not give excessive fluids",
            "Go to hospital today if no urination for several hours",
        ],
        "steps_bn": [
            "তলপেটে জোরে চাপ দেবেন না",
            "সোজা হয়ে বসে প্রস্রাবের চেষ্টা করতে বলুন",
            "আরাম লাগলে তলপেটে গরম কাপড় দিন",
            "অতিরিক্ত পানি দেবেন না",
            "কয়েক ঘণ্টা প্রস্রাব না হলে আজই হাসপাতালে যান",
        ]
    },
}

DEFAULT_FIRST_AID = {
    "en": [
        "Rest and avoid physical exertion",
        "Stay hydrated with clean water",
        "Monitor symptoms and note any changes",
        "Seek medical care if condition worsens",
    ],
    "bn": [
        "বিশ্রাম নিন",
        "বিশুদ্ধ পানি পান করুন",
        "লক্ষণ পর্যবেক্ষণ করুন",
        "অবস্থা খারাপ হলে চিকিৎসক দেখান",
    ]
}

SPECIAL_FIRST_AID = {
    "snake_bite": SYMPTOM_FIRST_AID[frozenset(["snake bite", "weakness", "difficulty in swallowing"])],
    "burn": SYMPTOM_FIRST_AID[frozenset(["burn", "blisters", "pain"])],
    "poison": SYMPTOM_FIRST_AID[frozenset(["poison", "vomiting", "confusion"])],
    "drowning": SYMPTOM_FIRST_AID[frozenset(["drowning", "shortness of breath", "unconsciousness"])],
    "animal_bite": SYMPTOM_FIRST_AID[frozenset(["animal bite", "bleeding", "pain"])],
}

def get_first_aid(symptoms: dict, language: str) -> dict:
    active = set(k for k, v in symptoms.items() if v == 1 and k not in ['age', 'sex-no', 'ispregnant'])
    lang_key = "bn" if language == "বাংলা" else "en"

    for symptom_set, advice in SYMPTOM_FIRST_AID.items():
        if len(symptom_set & active) >= len(symptom_set) * 0.5:
            return {
                "condition": advice["condition"],
                "steps": advice[f"steps_{lang_key}"]
            }

    return {
        "condition": "General Care" if language == "English" else "সাধারণ পরামর্শ",
        "steps": DEFAULT_FIRST_AID[lang_key]
    }