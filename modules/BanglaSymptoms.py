import re

from modules.text_negation import is_symptom_negated


SYMPTOMS = {
 # Nasal congestion
    "নাক বন্ধ": "nasal congestion",
    "নাক বন্ধ হয়ে গেছে": "nasal congestion",
    "নাক দিয়ে শ্বাস নিতে কষ্ট": "nasal congestion",
    "নাক আটকে গেছে": "nasal congestion",

    # Mental confusion / psychosis
    "মানসিক বিভ্রান্তি": "depressive or psychotic symptoms",
    "মাথা ঠিকমতো কাজ করছে না": "depressive or psychotic symptoms",
    "বাস্তবতা বুঝতে পারছি না": "depressive or psychotic symptoms",
    "অস্বাভাবিক আচরণ": "depressive or psychotic symptoms",

    # Lower abdominal pain
    "তলপেট ব্যথা": "lower abdominal pain",
    "তলপেটে ব্যথা": "lower abdominal pain",
    "নিচের পেটে ব্যথা": "lower abdominal pain",
    "তলপেটে প্রচণ্ড ব্যথা": "lower abdominal pain",

    # Arm pain
    "হাতে ব্যথা": "arm pain",
    "হাত ব্যথা": "arm pain",
    "বাহুতে ব্যথা": "arm pain",
    "হাতে ব্যাথা": "arm pain",
    "হাত ব্যাথা": "arm pain",
    "বাহু ব্যথা": "arm pain",
    "বাহু ব্যাথা": "arm pain",
    "হাতের ব্যথা": "arm pain",
    "হাতের ব্যাথা": "arm pain",

    # Loss of sensation
    "অনুভূতি হারানো": "loss of sensation",
    "অবশ লাগছে": "loss of sensation",
    "অসাড় হয়ে গেছে": "loss of sensation",
    "ঝিনঝিন করছে": "loss of sensation",

    # Abnormal involuntary movements
    "শরীর কাঁপছে": "abnormal involuntary movements",
    "হাত পা নিজের থেকে নড়ছে": "abnormal involuntary movements",
    "অনিয়ন্ত্রিত নড়াচড়া": "abnormal involuntary movements",

    # Pelvic pain
    "শ্রোণী ব্যথা": "pelvic pain",
    "পেলভিকে ব্যথা": "pelvic pain",
    "কোমরের নিচে ব্যথা": "pelvic pain",
    "কোমরে ব্যথা": "pelvic pain",
    "কোমর ব্যথা": "pelvic pain",

    # Movement problems
    "নড়াচড়ায় সমস্যা": "problems with movement",
    "হাঁটতে কষ্ট": "problems with movement",
    "চলাফেরা করতে কষ্ট": "problems with movement",
    "হাত পা নড়াতে পারছি না": "problems with movement",

    # Vision loss
    "দৃষ্টিশক্তি কমে গেছে": "diminished vision",
    "কম দেখতে পাচ্ছি": "diminished vision",
    "ঝাপসা দেখছি": "diminished vision",
    "চোখে ঝাপসা": "diminished vision",

    # Painful urination
    "প্রস্রাবে ব্যথা": "painful urination",
    "প্রস্রাবে জ্বালা": "painful urination",
    "প্রস্রাবে জ্বালা": "painful urination",
    "প্রস্রাব করতে ব্যথা": "painful urination",

    # Urinary retention
    "প্রস্রাব আটকে গেছে": "retention of urine",
    "প্রস্রাব হচ্ছে না": "retention of urine",
    "প্রস্রাব বের হচ্ছে না": "retention of urine",

    # Blood in stool
    "মলে রক্ত": "blood in stool",
    "পায়খানার সাথে রক্ত": "blood in stool",
    "পায়খানায় রক্ত": "blood in stool",

    # Frequent urination
    "ঘন ঘন প্রস্রাব": "frequent urination",
    "বারবার প্রস্রাব": "frequent urination",
    "প্রস্রাব বেশি হচ্ছে": "frequent urination",

    # Hallucinations
    "হ্যালুসিনেশন": "delusions or hallucinations",
    "অদ্ভুত জিনিস দেখছি": "delusions or hallucinations",
    "কানে অদ্ভুত শব্দ শুনছি": "delusions or hallucinations",

    # Foot pain
    "পায়ের পাতায় ব্যথা": "foot or toe pain",
    "পায়ের আঙুলে ব্যথা": "foot or toe pain",
    "পা'র আঙুলে ব্যথা": "foot or toe pain",

    # Vaginal discharge
    "যোনিপথে স্রাব": "vaginal discharge",
    "সাদা স্রাব": "vaginal discharge",
    "অস্বাভাবিক স্রাব": "vaginal discharge",

    # Blood in urine
    "প্রস্রাবে রক্ত": "blood in urine",
    "প্রসাবে রক্ত": "blood in urine",
    "লাল প্রস্রাব": "blood in urine",

    # Involuntary urination
    "প্রস্রাব ধরে রাখতে পারছি না": "involuntary urination",
    "নিজে থেকেই প্রস্রাব হয়ে যাচ্ছে": "involuntary urination",

    # Irregular heartbeat
    "অনিয়মিত হৃদস্পন্দন": "irregular heartbeat",
    "হার্টবিট অনিয়মিত": "irregular heartbeat",
    "হৃদস্পন্দন এদিক ওদিক হচ্ছে": "irregular heartbeat",

    # Difficulty speaking
    "কথা বলতে কষ্ট": "difficulty speaking",
    "ঠিকমতো কথা বলতে পারছি না": "difficulty speaking",
    "বাক সমস্যা": "difficulty speaking",

    # Leg swelling
    "পা ফুলে গেছে": "leg swelling",
    "পা ফোলা": "leg swelling",
    "পায়ে পানি এসেছে": "leg swelling",

    # Allergic reaction
    "অ্যালার্জি": "allergic reaction",
    "এলার্জি": "allergic reaction",
    "অ্যালার্জিক সমস্যা": "allergic reaction",

    # Lip swelling
    "ঠোঁট ফুলে গেছে": "lip swelling",
    "ঠোঁট ফোলা": "lip swelling",

    # Difficulty swallowing
    "গিলতে কষ্ট": "difficulty in swallowing",
    "খাবার গিলতে পারছি না": "difficulty in swallowing",

    # Diminished hearing
    "কম শুনতে পাচ্ছি": "diminished hearing",
    "শ্রবণশক্তি কমে গেছে": "diminished hearing",
    "কানে কম শুনি": "diminished hearing",

    # Wheezing
    "সাঁ সাঁ শব্দ": "wheezing",
    "শ্বাসে সিটি বাজছে": "wheezing",
    "বুকে সাঁ সাঁ শব্দ": "wheezing",

    # Double vision
    "দুইটা দেখছি": "double vision",
    "দ্বৈত দৃষ্টি": "double vision",
    "একটার জায়গায় দুইটা দেখছি": "double vision",

    # Rectal bleeding
    "মলদ্বার দিয়ে রক্ত": "rectal bleeding",
    "পেছন দিক দিয়ে রক্ত": "rectal bleeding",

    # Pregnancy problems
    "গর্ভাবস্থার সমস্যা": "problems during pregnancy",
    "প্রেগন্যান্সির সমস্যা": "problems during pregnancy",

    # Sweating
    "অতিরিক্ত ঘাম": "sweating",
    "বেশি ঘাম হচ্ছে": "sweating",
    "অনেক ঘাম": "sweating",

    # Heavy menstrual flow
    "অতিরিক্ত মাসিক": "heavy menstrual flow",
    "বেশি রক্তপাত হচ্ছে": "heavy menstrual flow",
    "মাসিকে বেশি রক্ত": "heavy menstrual flow",
    "মাসিক বেশি হচ্ছে": "heavy menstrual flow",
    "পিরিয়ডে বেশি রক্ত": "heavy menstrual flow",
    "পিরিয়ডে বেশি রক্ত": "heavy menstrual flow",
    "heavy period": "heavy menstrual flow",
    "heavy bleeding period": "heavy menstrual flow",

    # Painful menstruation / period pain
    "মাসিকের ব্যথা": "painful menstruation",
    "মাসিক ব্যথা": "painful menstruation",
    "মাসিকে ব্যথা": "painful menstruation",
    "মাসিকের সময় ব্যথা": "painful menstruation",
    "মাসিকের সময় ব্যথা": "painful menstruation",
    "পিরিয়ডের ব্যথা": "painful menstruation",
    "পিরিয়ডের ব্যথা": "painful menstruation",
    "পিরিয়ড ব্যথা": "painful menstruation",
    "পিরিয়ড ব্যথা": "painful menstruation",
    "period pain": "painful menstruation",
    "painful period": "painful menstruation",
    "painful periods": "painful menstruation",
    "period cramps": "painful menstruation",
    "menstrual cramps": "painful menstruation",
    "masik betha": "painful menstruation",
    "masiker betha": "painful menstruation",
    "masike betha": "painful menstruation",
    "period betha": "painful menstruation",

    # Vomiting blood
    "রক্তবমি": "vomiting blood",
    "বমির সাথে রক্ত": "vomiting blood",
    

    # Mouth ulcer
    "মুখে ঘা": "mouth ulcer",
    "জিহ্বায় ঘা": "mouth ulcer",
    "মুখের ভেতর ঘা": "mouth ulcer",

    # Sleepiness
    "ঘুম ঘুম লাগছে": "sleepiness",
    "সবসময় ঘুম পাচ্ছে": "sleepiness",
    "ঝিমুনি": "sleepiness",

    # Ringing ear
    "কানে ভোঁ ভোঁ শব্দ": "ringing in ear",
    "কানে শব্দ হচ্ছে": "ringing in ear",
    "কানে বাঁশি বাজছে": "ringing in ear",

    # Testicular pain
    "অণ্ডকোষে ব্যথা": "pain in testicles",
    "টেস্টিকলে ব্যথা": "pain in testicles",

    # Bloating
    "পেট ফাঁপা": "stomach bloating",
    "পেট ফুলে গেছে": "stomach bloating",
    "গ্যাসে পেট ফুলে গেছে": "stomach bloating",

    # Hemoptysis
    "রক্তসহ কাশি": "hemoptysis",
    "কাশির সাথে রক্ত": "hemoptysis",
    "কফে রক্ত": "hemoptysis",

    # Blindness
    "অন্ধত্ব": "blindness",
    "দেখতে পাচ্ছি না": "blindness",
    "দৃষ্টি চলে গেছে": "blindness",

    # Scrotal swelling
    "অণ্ডথলি ফুলে গেছে": "swelling of scrotum",
    "অণ্ডথলি ফোলা": "swelling of scrotum",

    # Itchy scalp
    "মাথার ত্বকে চুলকানি": "itchy scalp",
    "স্ক্যাল্প চুলকাচ্ছে": "itchy scalp",

    # Slurred speech
    "জড়িয়ে কথা বলা": "slurring words",
    "কথা জড়িয়ে যাচ্ছে": "slurring words",
    "হঠাৎ কথা জড়িয়ে যাচ্ছে": "slurring words",

    # Eyelid swelling
    "চোখের পাতা ফুলে গেছে": "eyelid swelling",
    "চোখের পাতা ফোলা": "eyelid swelling",

    # Nosebleed
    "নাক দিয়ে রক্ত": "nosebleed",
    "নাক থেকে রক্ত পড়ছে": "nosebleed",
    "নাকে রক্ত": "nosebleed",
       
    # Headache
    "মাথা ব্যথা": "headache",
"মাথাব্যথা": "headache",
"মাথা ব্যাথা": "headache",
"মাথাব্যাথা": "headache",
"মাথায় ব্যথা": "headache",
"মাথায় ব্যথা": "headache",
"মাথায় ব্যাথা": "headache",
"মাথায় ব্যাথা": "headache",
"matha betha": "headache",
"matha bytha": "headache",
"matha betha hocche": "headache",
"matha dukhtese": "headache",
"head ache": "headache",
"headache": "headache",
"মাথা ধরছে": "headache",
"matha dhorche": "headache",
"মাথা টনটন করছে": "headache",

    # Fever
    "জ্বর": "fever",
     "গা গরম": "fever",
    "শরীর গরম": "fever",
    "জ্বর এসেছে": "fever",
    "জ্বর উঠেছে": "fever",
    "জ্বর জ্বর লাগছে": "fever",
    "তাপমাত্রা বেশি": "fever",
"jor": "fever",
"jhor": "fever",
"gorom lagche": "fever",
"body gorom": "fever",
"fever": "fever",
"fevar": "fever",
"jwar": "fever",

    # Vomiting
    "বমি": "vomiting",
    "বমি করা": "vomiting",
    "বমি হচ্ছে": "vomiting",
    "বমি করতেছি": "vomiting",
    "বারবার বমি": "vomiting",
    "বমি দিচ্ছি": "vomiting",

    # Nausea
    "বমি বমি ভাব": "nausea",
    "বমি ভাব": "nausea",
    "বমি আসছে": "nausea",
    "বমি লাগছে": "nausea",
    "গা গুলাচ্ছে": "nausea",
    "গা গোলাচ্ছে": "nausea",
    "গা গুলানি": "nausea",
    "vomit feeling": "nausea",
"bomi bomi lagche": "nausea",
"ga gulochhe": "nausea",
"ga golacche": "nausea",
"nausea": "nausea",
"feeling like vomiting": "nausea",

    # Cough
    "কাশি": "cough",
    "কাঁশি": "cough",
    "খুকখুক কাশি": "cough",
    "অনেক কাশি": "cough",
    "কাশ হচ্ছে": "cough",
    "কাশি হচ্ছে": "cough",
    "কাশতেছি": "cough",
    "কাশতেসি": "cough",
    "শুকনা কাশি": "cough",
    "শুষ্ক কাশি": "cough",
"kashi": "cough",
"kashi hocche": "cough",
"cough": "cough",
"kosi": "cough",
"kash hoitese": "cough",
"khashi": "cough",

    # Sneezing
    "হাঁচি": "sneezing",
    "হাচি": "sneezing",
    "হাঁচি হচ্ছে": "sneezing",
    "হাচি হচ্ছে": "sneezing",
    "অনেক হাঁচি": "sneezing",
    "বারবার হাঁচি": "sneezing",
    "sneezing": "sneezing",
    "sneeze": "sneezing",
    "hachi": "sneezing",
    "hanchi": "sneezing",
    "haci": "sneezing",

    # Sputum
    "কফ": "coughing up sputum",
    "কফ উঠছে": "coughing up sputum",
    "কফ হচ্ছে": "coughing up sputum",
    "বুকে কফ": "coughing up sputum",

# ---------- Difficulty Breathing (Respiratory) ----------
"শ্বাসকষ্ট": "difficulty breathing",
"শ্বাস কষ্ট": "difficulty breathing",
"শ্বাস নিতে কষ্ট": "difficulty breathing",
"নিঃশ্বাস নিতে কষ্ট": "difficulty breathing",
"শ্বাস নিতে পারছি না": "difficulty breathing",
"নিঃশ্বাস নিতে পারছি না": "difficulty breathing",
"গভীর শ্বাস নিতে কষ্ট": "difficulty breathing",
"কাশির সাথে শ্বাসকষ্ট": "difficulty breathing",
"জ্বরের সাথে শ্বাসকষ্ট": "difficulty breathing",
"হাঁপাচ্ছি": "difficulty breathing",
"হাপাচ্ছি": "difficulty breathing",
"হাঁপানি উঠেছে": "difficulty breathing",
"শ্বাসে বাঁশির শব্দ": "difficulty breathing",
"দম নিতে পারছি না": "difficulty breathing",
"দম বন্ধ হয়ে আসছে": "difficulty breathing",
"breathing problem": "difficulty breathing",
"breath problem": "difficulty breathing",
"difficulty breathing": "difficulty breathing",
"cannot breathe properly": "difficulty breathing",
"can't breathe": "difficulty breathing",
"hard to breathe": "difficulty breathing",
"shash nite kosto": "difficulty breathing",
"nihshash nite kosto": "difficulty breathing",
"hapacchi": "difficulty breathing",

# ---------- Shortness of Breath (Cardiac / Exertional) ----------
"বুকে ব্যথার সাথে শ্বাসকষ্ট": "shortness of breath",
"বুকে চাপের সাথে শ্বাসকষ্ট": "shortness of breath",
"বুকে চাপ লাগে": "shortness of breath",
"হাঁটলেই শ্বাসকষ্ট": "shortness of breath",
"সিঁড়ি উঠলে শ্বাসকষ্ট": "shortness of breath",
"হাঁটতে গেলেই শ্বাসকষ্ট": "shortness of breath",
"কাজ করলে শ্বাসকষ্ট": "shortness of breath",
"অল্প হাঁটলেই শ্বাসকষ্ট": "shortness of breath",
"দম ফুরিয়ে যায়": "shortness of breath",
"শ্বাস ছোট হয়ে যায়": "shortness of breath",
"দম নিতে কষ্ট": "shortness of breath",
"শুয়ে থাকলে শ্বাসকষ্ট": "shortness of breath",
"শুয়ে থাকলে দম বন্ধ লাগে": "shortness of breath",
"shortness of breath": "shortness of breath",
"sob": "shortness of breath",
"out of breath": "shortness of breath",
"shash kosto while walking": "shortness of breath",
"dom nite kosto while walking": "shortness of breath",

    # Sore throat
    "গলা ব্যথা": "sore throat",
    "গলাব্যথা": "sore throat",
    "গলায় ব্যথা": "sore throat",
    "গলা খুসখুস": "sore throat",
    "গলা জ্বালা": "sore throat",
    "গলা বসে গেছে": "hoarse voice",

    # Chest pain
    "বুকে ব্যথা": "sharp chest pain",
    "বুকে ব্যথা": "sharp chest pain",
    "বুক ব্যথা": "sharp chest pain",
    "বুকে তীব্র ব্যথা": "sharp chest pain",
    "আমার বুকে প্রচণ্ড ব্যথা": "sharp chest pain",
    "বুকে চিনচিন ব্যথা": "sharp chest pain",
    "বুকে ব্যথা": "sharp chest pain",
"buke betha": "sharp chest pain",
"booke betha": "sharp chest pain",
"buk betha": "sharp chest pain",
"buke jala": "sharp chest pain",
"buke tight feel": "sharp chest pain",
"chest pain": "sharp chest pain",
"chest betha": "sharp chest pain",

    # Chest tightness
    "বুকে চাপ": "chest tightness",
    "বুক ভারী": "chest tightness",
    "বুকে ভার": "chest tightness",
    "বুক চেপে আছে": "chest tightness",

    # Abdominal pain
    "পেট ব্যথা": "sharp abdominal pain",
    "পেটে ব্যথা": "sharp abdominal pain",
    "পেটের ব্যথা": "sharp abdominal pain",
    "পেটে অনেক ব্যথা": "sharp abdominal pain",
    "পেটে খুব ব্যথা": "sharp abdominal pain",
    "পেটে প্রচণ্ড ব্যথা": "sharp abdominal pain",
    "পেট কামড়াচ্ছে": "sharp abdominal pain",
    "পেট কামড়াচ্ছে": "sharp abdominal pain",
    "পেট মোচড়াচ্ছে": "sharp abdominal pain",
    "পেট মোচড়াচ্ছে": "sharp abdominal pain",
    "পেট ব্যাথা": "sharp abdominal pain",
    "পেটে ব্যাথা": "sharp abdominal pain",
    "pete betha": "sharp abdominal pain",
"pet betha": "sharp abdominal pain",
"pete byatha": "sharp abdominal pain",
"pet byatha": "sharp abdominal pain",
"pete khub betha": "sharp abdominal pain",
"pet mochrachhe": "sharp abdominal pain",
"pet kamracche": "sharp abdominal pain",

    # Burning stomach pain
    "পেটে জ্বালা": "burning abdominal pain",
    "পেট জ্বালা": "burning abdominal pain",
    "গ্যাস্ট্রিকের জ্বালা": "burning abdominal pain",
    "পাকস্থলীতে জ্বালা": "burning abdominal pain",

    # Diarrhea
    "ডায়রিয়া": "diarrhea",
    "ডায়রিয়া": "diarrhea",
    "পাতলা পায়খানা": "diarrhea",
    "বারবার পায়খানা": "diarrhea",
    "পেট খারাপ": "diarrhea",
    "লুজ মোশন": "diarrhea",
    "diarrhea": "diarrhea",
"daira": "diarrhea",
"patla paykhana": "diarrhea",
"loose motion": "diarrhea",
"bar bar potty": "diarrhea",

    # Constipation
    "কোষ্ঠকাঠিন্য": "constipation",
    "পায়খানা হচ্ছে না": "constipation",
    "পায়খানা শক্ত": "constipation",
    "পেট পরিষ্কার হচ্ছে না": "constipation",
    "pakhana hocche na": "constipation",
"pakhana hocche na bhalo vabe": "constipation",
"pet theke potty hocche na": "constipation",

    # Dizziness
    "মাথা ঘোরা": "dizziness",
    "মাথা ঘুরছে": "dizziness",
    "চক্কর": "dizziness",
    "চক্কর লাগছে": "dizziness",
    "ঘুরঘুর লাগছে": "dizziness",
    "matha ghurche": "dizziness",
"chokkor": "dizziness",
"chakkor lagche": "dizziness",
"ghurghur lagche": "dizziness",

    # Weakness
    "দুর্বলতা": "weakness",
    "দুর্বল লাগছে": "weakness",
    "শরীর দুর্বল": "weakness",
    "শক্তি পাচ্ছি না": "weakness",
    "অবসাদ": "weakness",
    "ক্লান্ত লাগছে": "weakness",
    "durbol lagche": "weakness",
"shorir durbol": "weakness",
"shokti nai": "weakness",
"clanto lagche": "weakness",
    # Chills
    "কাঁপুনি": "chills",
    "শীত শীত লাগছে": "chills",
    "ঠান্ডা লাগছে": "chills",
    "কাপুনি": "chills",

    # Palpitations
    "হৃদকম্পন": "palpitations",
    "বুক ধড়ফড়": "palpitations",
    "বুক ধরফর": "palpitations",
    "বুকে ধরফর": "palpitations",
    "বুকে ধরফর": "palpitations",
    "হার্ট বিট বেড়ে গেছে": "palpitations",
    "হার্ট দ্রুত চলছে": "palpitations",

    # Eye redness
    "চোখ লাল": "eye redness",
    "চোখ লাল হয়ে গেছে": "eye redness",

    # Eye pain
    "চোখে ব্যথা": "pain in eye",
    "চোখ ব্যথা": "pain in eye",

    # Eye itching
    "চোখ চুলকায়": "itchiness of eye",
    "চোখে চুলকানি": "itchiness of eye",

    # Ear pain
    "কানে ব্যথা": "ear pain",
    "কান ব্যথা": "ear pain",

    # Toothache
    "দাঁত ব্যথা": "toothache",
    "দাঁতে ব্যথা": "toothache",

    # Back pain
    "পিঠ ব্যথা": "back pain",
    "কোমরের পাশে ব্যথা": "back pain",
    "কোমরে ব্যথা": "back pain",
    "কোমর ব্যথা": "back pain",
    "কমর ব্যথা": "back pain",
    "পিঠে ব্যথা": "back pain",
    "কোমরের ব্যথা": "back pain",
"কোমরের পাশে ব্যথা": "back pain",
"বাম কোমরের ব্যথা": "back pain",
"ডান কোমরের ব্যথা": "back pain",
"বাম কোমরের পাশে ব্যথা": "back pain",
"ডান কোমরের পাশে ব্যথা": "back pain",
"কোমরের বাম পাশে ব্যথা": "back pain",
"কোমরের ডান পাশে ব্যথা": "back pain",
"বাম পাশের কোমরে ব্যথা": "back pain",
"ডান পাশের কোমরে ব্যথা": "back pain",

    # Knee pain
    "হাঁটু ব্যথা": "knee pain",
    "হাঁটুতে ব্যথা": "knee pain",

    # Leg pain
    "পায়ে ব্যথা": "leg pain",
    "পায়ে ব্যথা": "leg pain",
    "পায়ে ব্যাথা": "leg pain",
    "পায়ে ব্যাথা": "leg pain",
    "পা ব্যথা": "leg pain",
    "পা ব্যাথা": "leg pain",
    "পায়ের ব্যথা": "leg pain",
    "পায়ের ব্যথা": "leg pain",
    "পায়ের ব্যাথা": "leg pain",
    "পায়ের ব্যাথা": "leg pain",

    # Rash
    "ফুসকুড়ি": "skin rash",
    "ফুসকুড়ি": "skin rash",
    "চামড়ায় ফুসকুড়ি": "skin rash",
    "গায়ে ফুসকুড়ি": "skin rash",
    " লাল লাল দাগ": "skin rash",
    " লাল লাল বিচি": "skin rash",
    "র‍্যাশ": "skin rash",

    # Itching
    "চুলকানি": "itching of skin",
    "গায়ে চুলকানি": "itching of skin",
    "ত্বকে চুলকানি": "itching of skin",

    # Swelling
    "ফুলে গেছে": "skin swelling",
    "ফোলা": "skin swelling",
    "সুজে গেছে": "skin swelling",

    # Appetite loss
    "ক্ষুধা নেই": "decreased appetite",
    "ক্ষুধা কম": "decreased appetite",
    "খেতে ইচ্ছা করছে না": "decreased appetite",
    "রুচি নেই": "decreased appetite",

    # Heartburn
    "অম্বল": "heartburn",
    "বুক জ্বালা": "heartburn",
    "গ্যাস্ট্রিক": "heartburn",

    # Fainting
    "অজ্ঞান": "fainting",
    "অজ্ঞান হয়ে গেছে": "fainting",
    "জ্ঞান হারিয়েছে": "fainting",
    "gan hariyeche": "fainting",
    "gyan hariyeche": "fainting",
    

    # Seizure
    "খিঁচুনি": "seizures",
    "খিচুনি": "seizures",
    "ফিট": "seizures",
    "মৃগী": "seizures",

    # Jaundice
    "জন্ডিস": "jaundice",
    "চোখ হলুদ": "jaundice",
    "শরীর হলুদ": "jaundice",
    "jaundice": "jaundice",
"chokh holud": "jaundice",
"shorir holud": "jaundice"


}



def _contains_symptom_phrase(text, phrase):
    phrase = str(phrase).strip()
    if not phrase:
        return False

    if re.fullmatch(r"[A-Za-z0-9\s'-]+", phrase):
        escaped = re.escape(phrase.lower()).replace(r"\ ", r"\s+")
        return re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", text.lower()) is not None

    return phrase in text


def _is_negated_ascii_phrase(text, phrase):
    if not re.fullmatch(r"[A-Za-z0-9\s'-]+", str(phrase).strip()):
        return is_symptom_negated(text, phrase)

    escaped = re.escape(str(phrase).lower().strip()).replace(r"\ ", r"\s+")
    if not escaped:
        return False

    return is_symptom_negated(text, phrase)


def extract_bangla_symptoms(text, feature_cols):
    extracted = {}

    if not text:
        return extracted

    for bangla_word, feature_name in SYMPTOMS.items():
        if (
            _contains_symptom_phrase(text, bangla_word)
            and not _is_negated_ascii_phrase(text, bangla_word)
            and feature_name in feature_cols
        ):
            extracted[feature_name] = 1

    return extracted
   
