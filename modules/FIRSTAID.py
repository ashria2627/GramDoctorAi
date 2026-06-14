SYMPTOM_FIRST_AID = {
    frozenset(["sharp chest pain", "sweating", "shortness of breath",'palpitations']): {
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

    frozenset(["electrocution", "burn", "unconsciousness"]): {
    "condition": "Possible Electrocution",
    "steps_en": [
        "Turn off the power source before touching the person",
        "Call emergency services if available",
        "Check breathing and responsiveness",
        "Do not touch exposed wires",
        "Go to the nearest hospital immediately",
    ],
    "steps_bn": [
        "ব্যক্তিকে স্পর্শ করার আগে বিদ্যুতের সংযোগ বন্ধ করুন",
        "সম্ভব হলে জরুরি সাহায্যের জন্য কল করুন",
        "শ্বাস-প্রশ্বাস ও সাড়া দিচ্ছে কিনা দেখুন",
        "খোলা বৈদ্যুতিক তার স্পর্শ করবেন না",
        "অবিলম্বে নিকটস্থ হাসপাতালে যান",
    ]
},

    frozenset(["poison", "vomiting", "confusion",'rat']): {
    "condition": "Possible Rat Poisoning",
    "steps_en": [
        "Do not induce vomiting unless instructed by a doctor",
        "Keep the poison container if available",
        "Give nothing by mouth to an unconscious person",
        "Watch for bleeding or worsening symptoms",
        "Go to hospital immediately",
    ],
    "steps_bn": [
        "ডাক্তারের পরামর্শ ছাড়া বমি করানোর চেষ্টা করবেন না",
        "সম্ভব হলে বিষের পাত্রটি সঙ্গে রাখুন",
        "অচেতন ব্যক্তিকে মুখে কিছু দেবেন না",
        "রক্তপাত বা উপসর্গ খারাপ হচ্ছে কিনা লক্ষ্য করুন",
        "অবিলম্বে হাসপাতালে যান",
    ]
},

frozenset(["fracture", "pain", "swelling"]): {
    "condition": "Possible Fracture",
    "steps_en": [
        "Keep the injured part still",
        "Apply a cold pack wrapped in cloth",
        "Do not try to straighten the bone",
        "Avoid unnecessary movement",
        "Go to the nearest hospital",
    ],
    "steps_bn": [
        "আঘাতপ্রাপ্ত অংশ স্থির রাখুন",
        "কাপড়ে মোড়ানো ঠান্ডা সেঁক দিন",
        "হাড় সোজা করার চেষ্টা করবেন না",
        "অপ্রয়োজনীয় নড়াচড়া এড়িয়ে চলুন",
        "নিকটস্থ হাসপাতালে যান",
    ]
},

frozenset(["sprain", "pain", "swelling"]): {
    "condition": "Possible Sprain",
    "steps_en": [
        "Rest the affected area",
        "Apply ice wrapped in cloth for 15–20 minutes",
        "Elevate the injured limb if possible",
        "Avoid strenuous activity",
        "Seek medical care if severe pain or inability to walk",
    ],
    "steps_bn": [
        "আক্রান্ত অংশ বিশ্রামে রাখুন",
        "কাপড়ে মোড়ানো বরফ ১৫–২০ মিনিট ধরে দিন",
        "সম্ভব হলে আক্রান্ত অঙ্গ উঁচু করে রাখুন",
        "ভারী কাজ এড়িয়ে চলুন",
        "তীব্র ব্যথা বা হাঁটতে না পারলে চিকিৎসা নিন",
    ]
},

frozenset(["high fever", "confusion", "heat exposure"]): {
    "condition": "Possible Heat Stroke",
    "steps_en": [
        "Move the person to a cool place",
        "Remove excess clothing",
        "Cool the body with wet cloths or fans",
        "Give water only if fully awake",
        "Go to hospital immediately",
    ],
    "steps_bn": [
        "ব্যক্তিকে ঠান্ডা স্থানে নিয়ে যান",
        "অতিরিক্ত কাপড় খুলে দিন",
        "ভেজা কাপড় বা পাখা দিয়ে শরীর ঠান্ডা করুন",
        "পুরোপুরি সচেতন থাকলে পানি দিন",
        "অবিলম্বে হাসপাতালে যান",
    ]
},

frozenset(["scorpion sting", "pain", "swelling"]): {
    "condition": "Possible Scorpion Sting",
    "steps_en": [
        "Wash the area with soap and water",
        "Apply a cold pack wrapped in cloth",
        "Keep the affected limb still",
        "Watch for breathing difficulty",
        "Go to hospital if symptoms worsen",
    ],
    "steps_bn": [
        "সাবান ও পানি দিয়ে স্থানটি ধুয়ে নিন",
        "কাপড়ে মোড়ানো ঠান্ডা সেঁক দিন",
        "আক্রান্ত অঙ্গ স্থির রাখুন",
        "শ্বাসকষ্ট হচ্ছে কিনা লক্ষ্য করুন",
        "উপসর্গ বাড়লে হাসপাতালে যান",
    ]
},

frozenset(["insect sting", "swelling", "shortness of breath"]): {
    "condition": "Possible Insect Sting Reaction",
    "steps_en": [
        "Move away from the insects",
        "Remove the stinger if visible",
        "Apply a cold pack",
        "Watch for swelling of face or difficulty breathing",
        "Go to hospital immediately if severe symptoms develop",
    ],
    "steps_bn": [
        "পোকামাকড় থেকে দূরে যান",
        "হুল দেখা গেলে সাবধানে সরিয়ে ফেলুন",
        "ঠান্ডা সেঁক দিন",
        "মুখ ফুলে যাওয়া বা শ্বাসকষ্ট হচ্ছে কিনা লক্ষ্য করুন",
        "তীব্র উপসর্গ হলে দ্রুত হাসপাতালে যান",
    ]
},

frozenset(["hook injury", "bleeding", "pain"]): {
    "condition": "Possible Fish Hook Injury",
    "steps_en": [
        "Wash the wound with clean water",
        "Control bleeding with gentle pressure",
        "Do not forcefully remove deeply embedded hooks",
        "Cover with a clean cloth",
        "Go to a healthcare facility for removal and tetanus protection",
    ],
    "steps_bn": [
        "পরিষ্কার পানি দিয়ে ক্ষত ধুয়ে নিন",
        "হালকা চাপ দিয়ে রক্তপাত বন্ধ করার চেষ্টা করুন",
        "গভীরভাবে ঢুকে থাকা বড়শি জোর করে টানবেন না",
        "পরিষ্কার কাপড় দিয়ে ঢেকে রাখুন",
        "বড়শি অপসারণ ও টিটেনাস প্রতিরোধের জন্য চিকিৎসাকেন্দ্রে যান",
    ]
},


frozenset(["fall injury", "pain", "swelling"]): {
    "condition": "Possible Fall Injury",
    "steps_en": [
        "Help the person rest and avoid unnecessary movement",
        "Apply a cold pack wrapped in cloth to painful areas",
        "Do not move the person if neck, back, or hip injury is suspected",
        "Watch for severe pain, vomiting, or loss of consciousness",
        "Go to the nearest hospital if symptoms are severe",
    ],
    "steps_bn": [
        "ব্যক্তিকে বিশ্রাম নিতে সাহায্য করুন এবং অপ্রয়োজনীয় নড়াচড়া এড়িয়ে চলুন",
        "ব্যথার স্থানে কাপড়ে মোড়ানো ঠান্ডা সেঁক দিন",
        "ঘাড়, পিঠ বা কোমরে আঘাতের সন্দেহ হলে নাড়াচাড়া করবেন না",
        "তীব্র ব্যথা, বমি বা অজ্ঞান হওয়ার লক্ষণ আছে কিনা লক্ষ্য করুন",
        "উপসর্গ গুরুতর হলে নিকটস্থ হাসপাতালে যান",
    ]
},

frozenset(["drug exposure", "pain", "swelling"]): {
    "condition": "Possible Drug Injection Exposure",
    "steps_en": [
        "Wash the area with soap and clean water",
        "Do not squeeze the wound or suck the blood",
        "Cover the area with a clean dressing",
        "Keep any medication or syringe information if available",
        "Go to a healthcare facility promptly for evaluation",
    ],
    "steps_bn": [
        "সাবান ও পরিষ্কার পানি দিয়ে স্থানটি ধুয়ে নিন",
        "ক্ষতস্থান চেপে ধরবেন না বা রক্ত চুষে বের করার চেষ্টা করবেন না",
        "পরিষ্কার ব্যান্ডেজ বা কাপড় দিয়ে ঢেকে রাখুন",
        "সম্ভব হলে ব্যবহৃত ওষুধ বা সিরিঞ্জের তথ্য সংরক্ষণ করুন",
        "দ্রুত চিকিৎসাকেন্দ্রে গিয়ে পরীক্ষা করান",
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
    "snake_bite": SYMPTOM_FIRST_AID[
        frozenset(["snake bite", "weakness", "difficulty in swallowing"])
    ],

    "animal_bite": SYMPTOM_FIRST_AID[
        frozenset(["animal bite", "bleeding", "pain"])
    ],

    "burn": SYMPTOM_FIRST_AID[
        frozenset(["burn", "blisters", "pain"])
    ],

    "poison": SYMPTOM_FIRST_AID[
        frozenset(["poison", "vomiting", "confusion"])
    ],

    "drowning": SYMPTOM_FIRST_AID[
        frozenset(["drowning", "shortness of breath", "unconsciousness"])
    ],

    "electrocution": SYMPTOM_FIRST_AID[
        frozenset(["electrocution", "burn", "unconsciousness"])
    ],

    "rat_poison": SYMPTOM_FIRST_AID[
        frozenset(["poison", "vomiting", "confusion","rat"])
    ],

    "fracture": SYMPTOM_FIRST_AID[
        frozenset(["fracture", "pain", "swelling"])
    ],

    "sprain": SYMPTOM_FIRST_AID[
        frozenset(["sprain", "pain", "swelling"])
    ],

    "heat_stroke": SYMPTOM_FIRST_AID[
        frozenset(["high fever", "confusion", "heat exposure"])
    ],

    "scorpion_sting": SYMPTOM_FIRST_AID[
        frozenset(["scorpion sting", "pain", "swelling"])
    ],

    "insect_sting": SYMPTOM_FIRST_AID[
        frozenset(["insect sting", "swelling", "shortness of breath"])
    ],

    "hook_injury": SYMPTOM_FIRST_AID[
        frozenset(["hook injury", "bleeding", "pain"])
    ],

    "fall_injury": SYMPTOM_FIRST_AID[
        frozenset(["fall injury", "pain", "swelling"])
    ],

    "drug_injection_exposure": SYMPTOM_FIRST_AID[
        frozenset(["drug exposure", "pain", "swelling"])
    ],
}

def get_first_aid_from_followup(followup_answers: dict, language: str, symptoms: dict = None, triage_color: str = None) -> dict:
    lang_key = "bn" if language == "বাংলা" else "en"

    # If triage is red and we have symptoms — use symptom-based first aid (handles palpitations → cardiac etc.)
    if triage_color == "red" and symptoms:
        result = get_first_aid(symptoms, language)
        if result["condition"] != ("General Care" if language == "English" else "সাধারণ পরামর্শ"):
            return result

    # Otherwise use followup category map
    detected = set()
    for k in followup_answers.keys():
        cat = "_".join(k.split("_")[1:-1])
        detected.add(cat.replace(" ", "_"))

    category_map = {
        "snake_bite": "snake_bite",
        "animal_bite": "animal_bite",
        "burn": "burn",
        "pesticide_poisoning": "poison",
        "drug_exposure": "drug_injection_exposure",
        "wound": "fall_injury",
        "drowning": "drowning",
        "seizure": "electrocution",
        "heat_stroke": "heat_stroke",
    }

    for cat, key in category_map.items():
        if cat in detected and key in SPECIAL_FIRST_AID:
            advice = SPECIAL_FIRST_AID[key]
            return {
                "condition": advice["condition"],
                "steps": advice[f"steps_{lang_key}"]
            }

    return {
        "condition": "General Care" if language == "English" else "সাধারণ পরামর্শ",
        "steps": DEFAULT_FIRST_AID[lang_key]
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