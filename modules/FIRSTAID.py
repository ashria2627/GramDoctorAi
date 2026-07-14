SYMPTOM_ALIASES = {
    "painful periods": "painful menstruation",
    "heavy menstrual bleeding": "heavy menstrual flow",
    "slurring words": "difficulty speaking",
}




SYMPTOM_FIRST_AID = {
    frozenset(["sharp chest pain", "shortness of breath",'palpitations']): {
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
    frozenset(["fever", "vomiting", "sharp abdominal pain","skin rash","weakness","decreased appetite"]): {
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
    frozenset(["difficulty speaking"]): {
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

frozenset(["irregular periods"]): {
    "condition": "Possible Irregular Menstrual Cycle",
    "steps_en": [
        "Keep a record of your menstrual dates and symptoms",
        "Eat a balanced diet and stay hydrated",
        "Manage stress and get adequate sleep",
        "Avoid taking hormonal medicines without medical advice",
        "See a healthcare provider if periods are very infrequent, absent, or accompanied by severe symptoms",
    ],
    "steps_bn": [
        "মাসিকের তারিখ ও উপসর্গের রেকর্ড রাখুন",
        "সুষম খাবার খান এবং পর্যাপ্ত পানি পান করুন",
        "মানসিক চাপ কমানোর চেষ্টা করুন এবং পর্যাপ্ত ঘুমান",
        "চিকিৎসকের পরামর্শ ছাড়া হরমোনজাতীয় ওষুধ গ্রহণ করবেন না",
        "মাসিক খুব অনিয়মিত, বন্ধ হয়ে গেলে বা অন্য গুরুতর উপসর্গ থাকলে চিকিৎসকের পরামর্শ নিন",
    ]
},

frozenset(["painful menstruation"]): {
    "condition": "Possible Painful Menstruation",
    "steps_en": [
        "Rest and apply a warm compress to the lower abdomen",
        "Drink plenty of fluids",
        "Light exercise or walking may help relieve discomfort",
        "Take pain medicine only as directed",
        "Seek medical care if pain is severe or worsening",
    ],
    "steps_bn": [
        "বিশ্রাম নিন এবং তলপেটে হালকা গরম সেঁক দিন",
        "পর্যাপ্ত পানি ও তরল পান করুন",
        "হালকা ব্যায়াম বা হাঁটাচলা ব্যথা কমাতে সাহায্য করতে পারে",
        "প্রয়োজন হলে নির্দেশনা অনুযায়ী ব্যথার ওষুধ গ্রহণ করুন",
        "ব্যথা খুব বেশি হলে বা বাড়তে থাকলে চিকিৎসকের পরামর্শ নিন",
    ]
},

frozenset(["heavy menstrual flow"]):  {
    "condition": "Possible Heavy Menstrual Bleeding",
    "steps_en": [
        "Use clean sanitary pads and monitor the amount of bleeding",
        "Drink plenty of fluids and eat iron-rich foods",
        "Avoid strenuous activities if feeling weak or dizzy",
        "Do not take medicines to stop bleeding without medical advice",
        "Go to a healthcare facility promptly if bleeding is very heavy, prolonged, or causing dizziness",
    ],
    "steps_bn": [
        "পরিষ্কার স্যানিটারি প্যাড ব্যবহার করুন এবং রক্তপাতের পরিমাণ লক্ষ্য করুন",
        "পর্যাপ্ত পানি পান করুন এবং আয়রনসমৃদ্ধ খাবার খান",
        "দুর্বলতা বা মাথা ঘোরা থাকলে অতিরিক্ত পরিশ্রম এড়িয়ে চলুন",
        "চিকিৎসকের পরামর্শ ছাড়া রক্তপাত বন্ধের ওষুধ গ্রহণ করবেন না",
        "রক্তপাত খুব বেশি হলে, দীর্ঘস্থায়ী হলে বা মাথা ঘোরা দেখা দিলে দ্রুত চিকিৎসাকেন্দ্রে যান",
    ]
},
# 1. Viral Upper Respiratory Infection
frozenset(["cough", "sore throat", "fever"]): {
    "condition": "Possible Viral Respiratory Infection",
    "steps_en": [
        "Drink plenty of warm fluids",
        "Gargle with warm salt water",
        "Rest well",
        "Wear a mask to avoid spreading infection",
        "See a doctor if fever lasts more than 3 days or breathing becomes difficult",
    ],
    "steps_bn": [
        "গরম তরল পান করুন",
        "গরম লবণ পানি দিয়ে গার্গল করুন",
        "পর্যাপ্ত বিশ্রাম নিন",
        "অন্যদের সংক্রমণ এড়াতে মাস্ক ব্যবহার করুন",
        "৩ দিনের বেশি জ্বর থাকলে বা শ্বাসকষ্ট হলে চিকিৎসকের কাছে যান",
    ]
},

# 2. Influenza
frozenset(["fever", "cough", "body pain", "chills","difficulty breathing"]): {
    "condition": "Possible Influenza",
    "steps_en": [
        "Rest at home",
        "Drink plenty of fluids",
        "Take paracetamol for fever",
        "Avoid close contact with others",
        "Seek medical care if breathing becomes difficult",
    ],
    "steps_bn": [
        "বাড়িতে বিশ্রাম নিন",
        "পর্যাপ্ত তরল পান করুন",
        "জ্বরের জন্য প্যারাসিটামল গ্রহণ করুন",
        "অন্যদের থেকে দূরে থাকুন",
        "শ্বাসকষ্ট হলে চিকিৎসকের কাছে যান",
    ]
},

# 3. Asthma
frozenset(["wheezing", "chest tightness", "cough"]): {
    "condition": "Possible Asthma Attack",
    "steps_en": [
        "Sit upright",
        "Use prescribed inhaler if available",
        "Stay calm",
        "Avoid smoke and dust",
        "Go to hospital if symptoms worsen",
    ],
    "steps_bn": [
        "সোজা হয়ে বসুন",
        "ইনহেলার থাকলে ব্যবহার করুন",
        "শান্ত থাকুন",
        "ধোঁয়া ও ধুলাবালি এড়িয়ে চলুন",
        "উপসর্গ বাড়লে হাসপাতালে যান",
    ]
},

# 4. Severe Allergy
frozenset(["allergic reaction", "lip swelling", "throat swelling"]): {
    "condition": "Possible Severe Allergic Reaction",
    "steps_en": [
        "Call 999 immediately",
        "Avoid the suspected allergen",
        "Use an adrenaline auto-injector if prescribed",
        "Keep the person sitting upright",
        "Go to hospital immediately",
    ],
    "steps_bn": [
        "এখনই ৯৯৯ নম্বরে ফোন করুন",
        "যে কারণে অ্যালার্জি হয়েছে তা এড়িয়ে চলুন",
        "প্রেসক্রাইব করা এপিনেফ্রিন থাকলে ব্যবহার করুন",
        "রোগীকে সোজা বসিয়ে রাখুন",
        "অবিলম্বে হাসপাতালে যান",
    ]
},

# 5. Mild Allergy
frozenset(["skin rash", "itching of skin"]): {
    "condition": "Possible Mild Allergy",
    "steps_en": [
        "Wash the affected area",
        "Apply a cool compress",
        "Avoid scratching",
        "Avoid known allergens",
        "See a doctor if swelling develops",
    ],
    "steps_bn": [
        "স্থানটি পরিষ্কার পানি দিয়ে ধুয়ে নিন",
        "ঠান্ডা সেঁক দিন",
        "চুলকাবেন না",
        "অ্যালার্জির কারণ এড়িয়ে চলুন",
        "ফুলে গেলে চিকিৎসকের কাছে যান",
    ]
},

# 6. UTI
frozenset(["painful urination", "frequent urination", "blood in urine"]): {
    "condition": "Possible Urinary Tract Infection",
    "steps_en": [
        "Drink plenty of water",
        "Do not hold urine",
        "Maintain genital hygiene",
        "Avoid self-medicating with antibiotics",
        "Visit a doctor today",
    ],
    "steps_bn": [
        "পর্যাপ্ত পানি পান করুন",
        "প্রস্রাব আটকে রাখবেন না",
        "যৌনাঙ্গ পরিষ্কার রাখুন",
        "নিজে থেকে অ্যান্টিবায়োটিক খাবেন না",
        "আজই চিকিৎসকের কাছে যান",
    ]
},

# 7. Kidney Stone
frozenset(["back pain", "blood in urine", "painful urination"]): {
    "condition": "Possible Kidney Stone",
    "steps_en": [
        "Drink water unless vomiting",
        "Rest",
        "Do not ignore severe pain",
        "Avoid heavy activity",
        "Go to hospital today",
    ],
    "steps_bn": [
        "বমি না হলে পর্যাপ্ত পানি পান করুন",
        "বিশ্রাম নিন",
        "তীব্র ব্যথা অবহেলা করবেন না",
        "ভারী কাজ করবেন না",
        "আজই হাসপাতালে যান",
    ]
},

# 8. Gastritis
frozenset(["burning abdominal pain", "heartburn", "nausea"]): {
    "condition": "Possible Gastritis",
    "steps_en": [
        "Eat small meals",
        "Avoid spicy food",
        "Drink water",
        "Avoid alcohol and smoking",
        "See a doctor if vomiting blood develops",
    ],
    "steps_bn": [
        "অল্প অল্প করে খাবার খান",
        "ঝাল খাবার এড়িয়ে চলুন",
        "পানি পান করুন",
        "ধূমপান ও অ্যালকোহল এড়িয়ে চলুন",
        "রক্তবমি হলে হাসপাতালে যান",
    ]
},

# 9. Food Poisoning
frozenset(["vomiting", "diarrhea", "nausea"]): {
    "condition": "Possible Food Poisoning",
    "steps_en": [
        "Drink ORS frequently",
        "Take small sips of water",
        "Avoid oily food",
        "Rest",
        "Go to hospital if unable to keep fluids down",
    ],
    "steps_bn": [
        "বারবার ওআরএস পান করুন",
        "অল্প অল্প করে পানি পান করুন",
        "তেলযুক্ত খাবার এড়িয়ে চলুন",
        "বিশ্রাম নিন",
        "পানি ধরে রাখতে না পারলে হাসপাতালে যান",
    ]
},

# 10. Eye Infection
frozenset(["eye redness", "white discharge from eye", "itchiness of eye"]): {
    "condition": "Possible Eye Infection",
    "steps_en": [
        "Wash hands frequently",
        "Avoid touching the eye",
        "Use a clean cloth to wipe discharge",
        "Do not share towels",
        "Visit an eye doctor",
    ],
    "steps_bn": [
        "ঘন ঘন হাত ধুয়ে নিন",
        "চোখে হাত দেবেন না",
        "পরিষ্কার কাপড় দিয়ে ময়লা পরিষ্কার করুন",
        "তোয়ালে ভাগাভাগি করবেন না",
        "চোখের ডাক্তার দেখান",
    ]
},

# 11. Sinusitis
frozenset(["nasal congestion", "painful sinuses", "headache"]): {
    "condition": "Possible Sinusitis",
    "steps_en": [
        "Drink plenty of fluids",
        "Use steam inhalation or saline nasal spray",
        "Take paracetamol for pain or fever if needed",
        "Rest and avoid smoke or dust",
        "See a doctor if symptoms last more than 10 days or worsen",
    ],
    "steps_bn": [
        "পর্যাপ্ত পানি পান করুন",
        "ভাপ নিন বা স্যালাইন নাকের স্প্রে ব্যবহার করুন",
        "প্রয়োজনে ব্যথা বা জ্বরের জন্য প্যারাসিটামল খান",
        "বিশ্রাম নিন এবং ধোঁয়া বা ধুলাবালি এড়িয়ে চলুন",
        "১০ দিনের বেশি থাকলে বা অবস্থা খারাপ হলে চিকিৎসকের কাছে যান",
    ]
},
frozenset(["vomiting"]): {
    "condition": "Vomiting",
    "steps_en": [
        "Take small sips of clean water or ORS frequently to prevent dehydration",
        "Avoid solid food until vomiting settles",
        "Once vomiting improves, start with bland foods such as rice, toast, or bananas",
        "Rest and avoid strenuous activity",
        "Seek medical care if vomiting continues for more than 24 hours, you cannot keep fluids down, or blood appears in the vomit"
    ],
    "steps_bn": [
        "পানিশূন্যতা রোধে অল্প অল্প করে বারবার পানি বা ওআরএস পান করুন",
        "বমি কমা পর্যন্ত শক্ত খাবার এড়িয়ে চলুন",
        "বমি কমে গেলে ভাত, টোস্ট বা কলার মতো হালকা খাবার দিয়ে শুরু করুন",
        "বিশ্রাম নিন এবং ভারী কাজ এড়িয়ে চলুন",
        "২৪ ঘণ্টার বেশি বমি চললে, পানি ধরে রাখতে না পারলে বা বমিতে রক্ত দেখা গেলে দ্রুত চিকিৎসকের কাছে যান"
    ]
},
# 12. Ear Infection
frozenset(["ear pain", "diminished hearing", "fever"]): {
    "condition": "Possible Ear Infection",
    "steps_en": [
        "Keep the ear dry",
        "Do not insert anything into the ear",
        "Take paracetamol for pain or fever if needed",
        "See a doctor within 24 hours",
        "Seek urgent care if swelling behind the ear or severe pain develops",
    ],
    "steps_bn": [
        "কান শুকনো রাখুন",
        "কানের ভেতরে কিছু প্রবেশ করাবেন না",
        "প্রয়োজনে ব্যথা বা জ্বরের জন্য প্যারাসিটামল খান",
        "২৪ ঘণ্টার মধ্যে চিকিৎসকের কাছে যান",
        "কানের পেছনে ফোলা বা তীব্র ব্যথা হলে জরুরি চিকিৎসা নিন",
    ]
},

# 13. Migraine
frozenset(["headache", "nausea", "dizziness"]): {
    "condition": "Possible Migraine",
    "steps_en": [
        "Rest in a quiet, dark room",
        "Drink plenty of water",
        "Take prescribed migraine medicine or paracetamol if appropriate",
        "Avoid bright lights and loud sounds",
        "Go to hospital immediately if this is the worst headache ever or with weakness",
    ],
    "steps_bn": [
        "শান্ত ও অন্ধকার ঘরে বিশ্রাম নিন",
        "পর্যাপ্ত পানি পান করুন",
        "প্রয়োজনে চিকিৎসকের পরামর্শ অনুযায়ী ওষুধ বা প্যারাসিটামল খান",
        "উজ্জ্বল আলো ও উচ্চ শব্দ এড়িয়ে চলুন",
        "জীবনের সবচেয়ে তীব্র মাথাব্যথা বা দুর্বলতা থাকলে দ্রুত হাসপাতালে যান",
    ]
},

# 14. Heat Exhaustion
frozenset(["dizziness", "weakness", "sweating"]): {
    "condition": "Possible Heat Exhaustion",
    "steps_en": [
        "Move to a cool shaded place",
        "Drink cool water or oral rehydration solution",
        "Loosen or remove excess clothing",
        "Cool the body with wet cloths or a fan",
        "Seek medical care if symptoms do not improve within 30 minutes",
    ],
    "steps_bn": [
        "ঠান্ডা বা ছায়াযুক্ত স্থানে যান",
        "ঠান্ডা পানি বা ওআরএস পান করুন",
        "আঁটসাঁট বা অতিরিক্ত কাপড় খুলে ফেলুন",
        "ভেজা কাপড় বা পাখা দিয়ে শরীর ঠান্ডা করুন",
        "৩০ মিনিটেও উন্নতি না হলে চিকিৎসা নিন",
    ]
},

# 15. Dehydration
frozenset(["decreased appetite", "dizziness", "weakness"]): {
    "condition": "Possible Dehydration",
    "steps_en": [
        "Drink oral rehydration solution frequently",
        "Take small sips of water often",
        "Rest in a cool place",
        "Avoid alcohol and excessive heat",
        "Go to hospital if unable to drink or symptoms become severe",
    ],
    "steps_bn": [
        "বারবার ওআরএস পান করুন",
        "অল্প অল্প করে বারবার পানি পান করুন",
        "ঠান্ডা স্থানে বিশ্রাম নিন",
        "অ্যালকোহল ও অতিরিক্ত গরম এড়িয়ে চলুন",
        "পানি পান করতে না পারলে বা অবস্থা খারাপ হলে হাসপাতালে যান",
    ]
},

# 16. Pregnancy Warning
frozenset(["problems during pregnancy", "vaginal discharge", "lower abdominal pain"]): {
    "condition": "Pregnancy Warning Signs",
    "steps_en": [
        "Rest and avoid strenuous activity",
        "Do not self-medicate",
        "Monitor bleeding, discharge, or pain",
        "Contact your obstetrician immediately",
        "Go to the nearest hospital if severe pain, bleeding, or reduced fetal movement occurs",
    ],
    "steps_bn": [
        "বিশ্রাম নিন এবং ভারী কাজ এড়িয়ে চলুন",
        "নিজে থেকে ওষুধ খাবেন না",
        "রক্তপাত, স্রাব বা ব্যথার দিকে নজর রাখুন",
        "অবিলম্বে স্ত্রীরোগ বিশেষজ্ঞের সাথে যোগাযোগ করুন",
        "তীব্র ব্যথা, রক্তপাত বা শিশুর নড়াচড়া কমে গেলে দ্রুত হাসপাতালে যান",
    ]
},

# 17. Pelvic Infection
frozenset(["pelvic pain", "vaginal discharge", "fever"]): {
    "condition": "Possible Pelvic Infection",
    "steps_en": [
        "Rest and drink plenty of fluids",
        "Avoid sexual activity until evaluated",
        "Do not self-medicate with antibiotics",
        "See a doctor as soon as possible",
        "Go to hospital immediately if severe abdominal pain or fainting occurs",
    ],
    "steps_bn": [
        "বিশ্রাম নিন এবং পর্যাপ্ত পানি পান করুন",
        "চিকিৎসা না হওয়া পর্যন্ত যৌন সম্পর্ক এড়িয়ে চলুন",
        "নিজে থেকে অ্যান্টিবায়োটিক খাবেন না",
        "যত দ্রুত সম্ভব চিকিৎসকের কাছে যান",
        "তীব্র পেটব্যথা বা অজ্ঞান হলে দ্রুত হাসপাতালে যান",
    ]
},

# 18. Hemorrhoids / Anal Disease
frozenset(["rectal bleeding", "pain of the anus", "constipation"]): {
    "condition": "Possible Hemorrhoids or Anal Disease",
    "steps_en": [
        "Drink plenty of water",
        "Eat high-fiber foods",
        "Avoid straining during bowel movements",
        "Take warm sitz baths",
        "See a doctor if bleeding continues or is heavy",
    ],
    "steps_bn": [
        "পর্যাপ্ত পানি পান করুন",
        "আঁশযুক্ত খাবার বেশি খান",
        "পায়খানার সময় অতিরিক্ত চাপ দেবেন না",
        "কুসুম গরম পানিতে সিটজ বাথ নিন",
        "রক্তপাত চলতে থাকলে বা বেশি হলে চিকিৎসকের কাছে যান",
    ]
},

# 19. Dental Infection
frozenset(["toothache", "mouth pain", "mouth ulcer"]): {
    "condition": "Possible Dental Infection",
    "steps_en": [
        "Rinse your mouth with warm salt water",
        "Maintain good oral hygiene",
        "Avoid very hot or cold foods",
        "Take paracetamol if needed for pain",
        "Visit a dentist as soon as possible",
    ],
    "steps_bn": [
        "হালকা গরম লবণ পানিতে কুলি করুন",
        "মুখের পরিচ্ছন্নতা বজায় রাখুন",
        "খুব গরম বা ঠান্ডা খাবার এড়িয়ে চলুন",
        "প্রয়োজনে ব্যথার জন্য প্যারাসিটামল খান",
        "যত দ্রুত সম্ভব দন্ত চিকিৎসকের কাছে যান",
    ]
},

# 20. Neck Infection
frozenset(["neck swelling", "sore throat", "fever","difficulty breathing"]): {
    "condition": "Possible Neck Infection",
    "steps_en": [
        "Rest and drink plenty of fluids",
        "Gargle with warm salt water",
        "Take paracetamol for fever if needed",
        "See a doctor the same day",
        "Go to hospital immediately if breathing or swallowing becomes difficult",
    ],
    "steps_bn": [
        "বিশ্রাম নিন এবং পর্যাপ্ত পানি পান করুন",
        "হালকা গরম লবণ পানিতে গার্গল করুন",
        "প্রয়োজনে জ্বরের জন্য প্যারাসিটামল খান",
        "আজই চিকিৎসকের কাছে যান",
        "শ্বাস নিতে বা গিলতে কষ্ট হলে দ্রুত হাসপাতালে যান",
    ]
},

# 21. Severe Lung Disease
frozenset(["hemoptysis", "cough", "difficulty breathing"]): {
    "condition": "Possible Severe Lung Disease",
    "steps_en": [
        "Go to the nearest hospital immediately",
        "Keep the patient sitting upright",
        "Avoid strenuous activity",
        "Do not smoke",
        "Call emergency services if breathing worsens",
    ],
    "steps_bn": [
        "অবিলম্বে নিকটস্থ হাসপাতালে যান",
        "রোগীকে সোজা বসিয়ে রাখুন",
        "ভারী কাজ করবেন না",
        "ধূমপান করবেন না",
        "শ্বাসকষ্ট বাড়লে জরুরি সেবায় ফোন করুন",
    ]
},

# 22. Liver Disease
frozenset(["jaundice", "decreased appetite", "nausea"]): {
    "condition": "Possible Liver Disease",
    "steps_en": [
        "Avoid alcohol completely",
        "Drink adequate fluids",
        "Eat light, nutritious meals",
        "See a doctor as soon as possible",
        "Go to hospital immediately if confusion, severe abdominal pain, or persistent vomiting develops",
    ],
    "steps_bn": [
        "সম্পূর্ণভাবে অ্যালকোহল এড়িয়ে চলুন",
        "পর্যাপ্ত তরল পান করুন",
        "হালকা ও পুষ্টিকর খাবার খান",
        "যত দ্রুত সম্ভব চিকিৎসকের কাছে যান",
        "অচেতনভাব, তীব্র পেটব্যথা বা বারবার বমি হলে দ্রুত হাসপাতালে যান",
    ]
},
# 23. Neurological Emergency
frozenset(["difficulty speaking", "loss of sensation", "problems with movement"]): {
    "condition": "Possible Stroke",
    "steps_en": [
        "Call 999 immediately",
        "Note the time symptoms started",
        "Do not give food or water",
        "Keep the patient lying on one side if vomiting",
        "Go to the nearest hospital immediately",
    ],
    "steps_bn": [
        "এখনই ৯৯৯ নম্বরে ফোন করুন",
        "লক্ষণ শুরুর সময় লিখে রাখুন",
        "মুখে কিছু খেতে দেবেন না",
        "বমি হলে পাশ ফিরিয়ে শুইয়ে দিন",
        "অবিলম্বে হাসপাতালে যান",
    ]
},

# 24. Musculoskeletal Pain
frozenset(["back pain", "arm pain", "leg pain"]): {
    "condition": "Possible Muscle Strain",
    "steps_en": [
        "Rest the painful areas",
        "Apply a warm compress or hot water bag for 15–20 minutes",
        "Avoid heavy lifting",
        "Drink water",
        "See a doctor if pain persists or follows an injury",
    ],
    "steps_bn": [
        "ব্যথার অংশ বিশ্রামে রাখুন",
        "১৫–২০ মিনিট গরম পানির ব্যাগ বা গরম সেঁক দিন",
        "ভারী কাজ এড়িয়ে চলুন",
        "পর্যাপ্ত পানি পান করুন",
        "ব্যথা না কমলে চিকিৎসকের কাছে যান",
    ]
},

# 25. Allergy + Pain
frozenset(["allergic reaction", "back pain", "arm pain","difficulty breathing"]): {
    "condition": "Allergic Reaction with Muscle Pain",
    "steps_en": [
        "Avoid the suspected allergen",
        "Apply a warm compress to painful muscles",
        "Drink plenty of water",
        "Take an antihistamine if previously prescribed",
        "Go to hospital immediately if swelling of lips or breathing difficulty develops",
    ],
    "steps_bn": [
        "যে কারণে অ্যালার্জি হয়েছে তা এড়িয়ে চলুন",
        "ব্যথার স্থানে গরম পানির ব্যাগ দিয়ে সেঁক দিন",
        "পর্যাপ্ত পানি পান করুন",
        "আগে থেকে পরামর্শ থাকলে অ্যান্টিহিস্টামিন গ্রহণ করুন",
        "ঠোঁট ফুলে গেলে বা শ্বাসকষ্ট হলে দ্রুত হাসপাতালে যান",
    ]
},
frozenset(["lower abdominal pain"]): {
    "condition": "Lower Abdominal Pain",
    "steps_en": [
        "Rest and avoid strenuous activity",
        "Drink plenty of water unless your doctor has advised otherwise",
        "Eat light, easily digestible foods if you feel able to eat",
        "Avoid taking painkillers such as ibuprofen or aspirin until the cause is known",
        "Seek medical care promptly if the pain becomes severe, is persistent, or is accompanied by fever, vomiting, blood in stool or urine, dizziness, or pregnancy-related symptoms"
    ],
    "steps_bn": [
        "বিশ্রাম নিন এবং ভারী কাজ এড়িয়ে চলুন",
        "চিকিৎসক নিষেধ না করলে পর্যাপ্ত পানি পান করুন",
        "খেতে পারলে হালকা ও সহজপাচ্য খাবার খান",
        "কারণ নিশ্চিত না হওয়া পর্যন্ত আইবুপ্রোফেন বা অ্যাসপিরিনের মতো ব্যথানাশক ওষুধ নিজে থেকে খাবেন না",
        "ব্যথা তীব্র হলে, দীর্ঘস্থায়ী হলে, অথবা জ্বর, বমি, মল বা প্রস্রাবে রক্ত, মাথা ঘোরা বা গর্ভাবস্থার উপসর্গ থাকলে দ্রুত চিকিৎসকের কাছে যান"
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
    "heavy_menstrual_flow": SYMPTOM_FIRST_AID[
    frozenset(["heavy menstrual flow"])
    ],
    "painful_menstruation": SYMPTOM_FIRST_AID[
    frozenset(["painful menstruation"])
    ],
    "irregular_periods": SYMPTOM_FIRST_AID[
        frozenset(["irregular periods"])
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
        "heavy_menstrual_flow": "heavy_menstrual_flow",
        "painful_menstruation": "painful_menstruation",
        "irregular_periods": "irregular_periods",
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
    active = set()

    for k, v in symptoms.items():
        if v == 1 and k not in ["age", "sex-no", "ispregnant"]:
            active.add(SYMPTOM_ALIASES.get(k, k))

    lang_key = "bn" if language == "বাংলা" else "en"

    menstrual_symptoms = {
        "painful menstruation",
        "heavy menstrual flow",
        "irregular periods",
        "pelvic pain",
        "lower abdominal pain",
        "vaginal discharge",
        "vaginal pain",
    }
    abdominal_symptoms = {"sharp abdominal pain", "lower abdominal pain", "pelvic pain"}
    limb_pain_symptoms = {"arm pain", "leg pain", "back pain", "knee pain", "joint pain", "neck pain", "hip pain"}

    if active.intersection(abdominal_symptoms) and active.intersection({"vomiting", "nausea", "diarrhea"}):
        return {
            "condition": "Possible Abdominal/Gastrointestinal Illness" if language == "English" else "সম্ভাব্য পেটের/পাকস্থলীর অসুস্থতা",
            "steps": [
                "Take small sips of clean water or ORS",
                "Eat light food and avoid oily or spicy food",
                "Rest and monitor pain, vomiting, stool, and fever",
                "Do not take painkillers or antibiotics without medical advice",
                "Go to hospital urgently if pain is severe, persistent, right-sided, with blood, fainting, or repeated vomiting",
            ] if language == "English" else [
                "পরিষ্কার জল বা ওআরএস অল্প অল্প করে পান করুন",

"হালকা খাবার খান এবং তৈলাক্ত বা মশলাদার খাবার এড়িয়ে চলুন",

"বিশ্রাম নিন এবং ব্যথা, বমি, মল ও জ্বরের দিকে নজর রাখুন",

"ডাক্তারের পরামর্শ ছাড়া ব্যথানাশক বা অ্যান্টিবায়োটিক খাবেন না",
"ব্যথা তীব্র, দীর্ঘস্থায়ী, ডান দিকে হলে, ব্যথার সাথে রক্ত ​​গেলে, জ্ঞান হারালে বা বারবার বমি হলে অবিলম্বে হাসপাতালে যান",
            ],
        }

    if len(active) >= 3 and active.intersection(menstrual_symptoms):
        return {
            "condition": (
                "Multiple Symptoms With Menstrual/Gynecological Pain"
                if language == "English"
                else "মাসিক/স্ত্রীরোগ সংক্রান্ত ব্যথার সাথে একাধিক উপসর্গ"
            ),
            "steps": [
                "Rest and avoid heavy activity",
                "Use a warm compress on the lower abdomen if comfortable",
                "Drink clean water and eat light food",
                "Do not take multiple medicines without medical advice",
                "See a gynecologist or clinic if pain is severe, recurrent, with heavy bleeding, fever, fainting, or unusual dischargeRest and avoid heavy activity",
                "Use a warm compress on the lower abdomen if comfortable",
                "Drink clean water and eat light food",
                "Do not take multiple medicines without medical advice",
                "See a gynecologist or clinic if pain is severe, recurrent, with heavy bleeding, fever, fainting, or unusual discharge",
            ] if language == "English" else [
                "বিশ্রাম নিন এবং ভারী কাজ থেকে বিরত থাকুন",

"আরামদায়ক হলে তলপেটে গরম সেঁক দিন",

"পরিষ্কার জল পান করুন এবং হালকা খাবার খান",

"ডাক্তারের পরামর্শ ছাড়া একাধিক ওষুধ খাবেন না",

"ব্যথা তীব্র হলে, বারবার হলে, অতিরিক্ত রক্তপাত, জ্বর, জ্ঞান হারানো বা অস্বাভাবিক স্রাব হলে স্ত্রীরোগ বিশেষজ্ঞ বা ক্লিনিকে যান।",
            ]
        }

    if len(active.intersection(limb_pain_symptoms)) >= 2:
        return {
            "condition": "Possible Muscle or Joint Pain" if language == "English" else "সম্ভাব্য পেশী বা জয়েন্টের ব্যথা",
            "steps": [
                "Rest the painful areas",
                "Use warm compresses for muscle aches, or cold compresses if pain followed an injury",
                "Avoid heavy lifting and strenuous activity",
                "Drink water and monitor swelling, redness, numbness, or weakness",
                "See a doctor if pain is severe, follows injury, or does not improve",
            ] if language == "English" else [
                "ব্যথাযুক্ত স্থানগুলিতে বিশ্রাম দিন",

"পেশীর ব্যথার জন্য গরম সেঁক দিন, অথবা আঘাতের পর ব্যথা হলে ঠান্ডা সেঁক দিন",

"ভারী জিনিস তোলা এবং কঠোর পরিশ্রমের কাজ এড়িয়ে চলুন",

"জল পান করুন এবং ফোলা, লালচে ভাব, অসাড়তা বা দুর্বলতার দিকে নজর রাখুন",

"ব্যথা তীব্র হলে, আঘাতের পর হলে, বা অবস্থার উন্নতি না হলে ডাক্তারের পরামর্শ নিন।",
            ],
        }

    # Check largest combinations first
    rules = sorted(
        SYMPTOM_FIRST_AID.items(),
        key=lambda x: len(x[0]),
        reverse=True
    )

    for symptom_set, advice in rules:
        if len(symptom_set) <= 2:
            continue

        matched = len(symptom_set & active)

        # Larger rules need at least three actual matches; two vague overlaps are too noisy.
        if matched >= max(3, len(symptom_set) - 1):
            return {
                "condition": advice["condition"],
                "steps": advice[f"steps_{lang_key}"]
            }

    # Multiple unrelated symptoms
    if len(active) >= 4 or (len(active) >= 3 and active.intersection(abdominal_symptoms)):
        return {
            "condition": (
                "Multiple Symptoms Requiring Medical Evaluation"
                if language == "English"
                else "একাধিক উপসর্গের জন্য চিকিৎসা মূল্যায়ন প্রয়োজন"
            ),
            "steps": [
                "Rest and avoid strenuous activity",
                "Drink plenty of clean water",
                "Treat each symptom safely (warm compress for muscle pain, cool compress for rash/itching)",
                "Avoid taking multiple medicines without medical advice",
                "Visit a healthcare facility today"
            ] if language == "English" else [
                "বিশ্রাম নিন",
                "পর্যাপ্ত বিশুদ্ধ পানি পান করুন",
                "উপসর্গ অনুযায়ী নিরাপদ প্রাথমিক পরিচর্যা করুন (ব্যথায় গরম সেঁক, র‍্যাশে ঠান্ডা সেঁক)",
                "চিকিৎসকের পরামর্শ ছাড়া একাধিক ওষুধ একসাথে খাবেন না",
                "আজই নিকটস্থ চিকিৎসাকেন্দ্রে যান"
            ]
        }

    for symptom_set, advice in rules:
      if len(symptom_set) <= 2 and symptom_set.issubset(active):
        return {
            "condition": advice["condition"],
            "steps": advice[f"steps_{lang_key}"]
        }
    EMERGENCY_SYMPTOMS = {
    "sharp chest pain",
    "shortness of breath",
    "palpitations",
    "loss of consciousness",
    "difficulty breathing",
    "snake bite",
    "seizure",
    "heavy bleeding",
    "severe burn",
    "drowning",
    "pesticide poisoning",
}    
    for symptom_set, advice in rules:
      if len(symptom_set) >= 3:
        matched = symptom_set & active
        if matched and any(sym in EMERGENCY_SYMPTOMS for sym in matched):
            return {
                "condition": advice["condition"],
                "steps": advice[f"steps_{lang_key}"]
            }

    return {
        "condition": "General Care" if language == "English" else "সাধারণ পরামর্শ",
        "steps": DEFAULT_FIRST_AID[lang_key]
    }
