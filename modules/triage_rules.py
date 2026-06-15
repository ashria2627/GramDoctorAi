def check_red_flags(symptoms):
    from collections import defaultdict
    symptoms = defaultdict(int, symptoms)
    if symptoms['sharp chest pain'] == 1 and symptoms['sweating'] == 1 and symptoms['shortness of breath'] == 1:
        return 'red'
    if (symptoms['slurring words']==1 or symptoms['blindness']==1 or symptoms['diminished vision']==1) and symptoms['headache']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['ispregnant']==1 and( symptoms['spotting or bleeding during pregnancy']==1 or symptoms['headache']==1 or symptoms['abnormal involuntary movements']==1):
        return 'red'
    if symptoms['fever']==1 and symptoms['vomiting']==1 and symptoms['sharp abdominal pain']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['age']<13 and (symptoms['seizures']==1 or symptoms['abnormal involuntary movements']==1 ):
        return 'red'
    if (symptoms['blood in stool']==1 or symptoms['vomiting blood']==1 or symptoms['rectal bleeding']==1 ) and symptoms['weakness']==1:
        return 'red'
    if symptoms['irregular heartbeat']==1 and symptoms['weakness']==1 and symptoms['fainting']==1:
        return "red"
    if symptoms['sex-no']==1 and symptoms['nausea']==1 and symptoms['sweating']==1 and symptoms['arm pain']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['sex-no']==1 and symptoms['sharp abdominal pain']==1 and symptoms['dizziness']==1 and symptoms['fainting']==1:
        return 'red'
    if symptoms['sharp abdominal pain']==1 and symptoms['fever']==1 and symptoms['vomiting']==1 and symptoms['decreased appetite']==1:
        return "red"
    if symptoms['shortness of breath']==1 and( symptoms['chest pain']==1 or symptoms['sharp chest pain']==1 )and symptoms['leg swelling']==1 :
        return 'red'
    if symptoms['pain in testicles']==1 and symptoms['vomiting']==1 and symptoms['sweating']==1:
        return 'red'
    if symptoms['back pain']==1 and( symptoms['chest pain']==1 or symptoms['sharp chest pain']==1)and symptoms['sweating']==1:
        return 'red'
    if symptoms['headache']==1 and symptoms['dizziness']==1 and symptoms['nausea']==1 and symptoms['weakness']==1:
        return 'red'
    if symptoms['difficulty in swallowing']==1  and symptoms['hoarse voice']==1 :
        return "red"
    if symptoms['back pain']==1 and symptoms['involuntary urination']==1 and symptoms['loss of sensation']==1:
        return "red"
    if symptoms['age']<13 and symptoms['depressive or psychotic symptoms']==1 and symptoms['blood in stool']==1 and symptoms['vomiting']==1:
        return 'red'
    if symptoms['blindness']==1 and( symptoms['chest pain']==1 or symptoms['sharp chest pain']==1)and symptoms['weakness']==1:
        return 'red'
    if symptoms['diminished vision'] == 1 and symptoms['headache'] == 1:
        return 'red'
    if symptoms['fever'] == 1 and symptoms['weakness'] == 1 and symptoms['stomach bloating'] == 1 and symptoms['age'] > 5:
        return 'red'
    if symptoms['delusions or hallucinations'] == 1 and symptoms['sweating'] == 0 and symptoms['headache'] == 1 and symptoms['weakness'] == 1:
        return 'red'
    if symptoms['sweating'] == 1 and symptoms['vomiting'] == 1 and symptoms['seizures'] == 1:
        return 'red'
    if symptoms['age'] < 1 and symptoms['seizures'] == 1 and symptoms['difficulty in swallowing'] == 1:
        return 'red'
    if symptoms['sleepiness'] == 1 and symptoms['difficulty in swallowing'] == 1 and symptoms['weakness'] == 1:
        return 'red'
    if symptoms['ispregnant'] == 1 and symptoms['headache'] == 1 and symptoms['leg swelling'] == 1 and symptoms['spots or clouds in vision'] == 1:
       return 'red'
    if symptoms['diarrhea'] == 1 and symptoms['vomiting'] == 1 and symptoms['weakness'] == 1 and symptoms['dizziness'] == 1:
       return 'red'
    if symptoms['fever'] == 0 and symptoms['weakness'] == 1 and symptoms['sweating'] == 1 and symptoms['dizziness'] == 1:
       return 'red'
    if symptoms['age'] > 50 and symptoms['foot or toe pain'] == 0 and symptoms['skin swelling'] == 1 and symptoms['loss of sensation'] == 1:
       return 'red'
    if symptoms['age'] > 60 and symptoms['leg pain'] == 1 and symptoms['problems with movement'] == 1 and symptoms['weakness'] == 1:
       return 'red'
    if symptoms['age'] > 60 and symptoms['fever'] == 0 and symptoms['shortness of breath'] == 1 and symptoms['weakness'] == 1 and symptoms['decreased appetite'] == 1:
       return 'red'
    if symptoms['sex-no'] == 0 and symptoms['age'] > 50 and symptoms['retention of urine'] == 1 and symptoms['lower abdominal pain'] == 1:
       return 'red'
    if symptoms['sex-no'] == 0 and symptoms['swelling of scrotum'] == 1 and symptoms['back pain'] == 1 and symptoms['pain in testicles'] == 0:
      return 'red'
    if symptoms['sex-no'] == 0 and symptoms['sharp abdominal pain'] == 1 and symptoms['vomiting'] == 1 and symptoms['constipation'] == 1:
      return 'red'
    if symptoms['sweating'] == 0 and symptoms['delusions or hallucinations'] == 1 and symptoms['headache'] == 1 and symptoms['weakness'] == 1:
      return 'red'
    if symptoms['fever'] == 1 and symptoms['leg pain'] == 1 and symptoms['jaundice'] == 1:
      return 'red'
    if symptoms['pain in eye'] == 1 and symptoms['eye redness'] == 1 and symptoms['diminished vision'] == 1:
      return 'red'

    return None

def apply_bd_rules(symptoms, result, followup_answers=None ,lang="English"):
    if not followup_answers:
        return result

    def get(cat, idx):
        for k, v in followup_answers.items():
            if f"_{cat}_" in k and k.endswith(f"_{idx}"):
                return str(v).lower().strip()
        return ""

    def yes(val):
        return any(w in val for w in ["yes", "হ্যাঁ", "আছে", "হয়েছে", "হচ্ছে", "y"])

    def no(val):
        return any(w in val for w in ["no", "না", "নেই", "n"])

#  DENGUE
    try:
        fever_days = int(get("dengue", 0).split()[0])
    except:
        fever_days = 0
 
    abdominal_pain = yes(get("dengue", 5))
    bleeding = yes(get("dengue", 6))
    poor_urine = no(get("dengue", 7))
    poor_fluids = no(get("dengue", 10))
    rash = yes(get("dengue", 11))
    confused = yes(get("dengue", 12))
 
    severe_joint_pain = yes(get("dengue", 13))
    fever_7_days = yes(get("dengue", 14)) or fever_days >= 7
    weight_loss = yes(get("dengue", 15))
    spleen_fullness = yes(get("dengue", 16))
    jaundice = yes(get("dengue", 17))
    flood_water = yes(get("dengue", 18))
    muscle_pain = yes(get("dengue", 19))
    eschar = yes(get("dengue", 20))
    post_sore_throat_joint = yes(get("dengue", 21))
    mouth_sores = yes(get("dengue", 22))
    hand_foot_rash = yes(get("dengue", 23))
    newborn_poor_feeding = yes(get("dengue", 24))
 
    age = int(symptoms.get("age", 0))
 
    if age < 1 and symptoms.get("fever", 0) == 1 and newborn_poor_feeding:
        return {
            "color": "red",
            "source": "Possible - ***Neonatal Sepsis***" if lang == "English" else "সম্ভাব্য - ***নবজাতকের সেপসিস***",
            "message": "Newborn fever with poor feeding is dangerous. Go to hospital immediately." if lang == "English" else "নবজাতকের জ্বর ও দুধ না খাওয়া বিপজ্জনক। অবিলম্বে হাসপাতালে যান।"
        }
 
    if fever_days >= 3 and any([abdominal_pain, bleeding, poor_urine, confused]):
        return {
            "color": "red",
            "source": "Possible - ***Dengue Warning Signs***" if lang == "English" else "সম্ভাব্য - ***ডেঙ্গুর সতর্কীকরণ লক্ষণ***",
            "message": "Dengue warning signs detected. Go to hospital today. Do NOT take ibuprofen or aspirin." if lang == "English" else "ডেঙ্গুর সতর্কীকরণ লক্ষণ দেখা গেছে। আজই হাসপাতালে যান। আইবুপ্রোফেন বা অ্যাসপিরিন খাবেন না।"
        }
 
    if fever_days >= 3 and (rash or poor_fluids):
        return {
            "color": "orange",
            "source": "***Dengue*** Suspected" if lang == "English" else "***ডেঙ্গু*** সন্দেহ করা হচ্ছে",
            "message": "Possible dengue. Drink ORS, avoid aspirin/ibuprofen, and see a doctor if symptoms worsen." if lang == "English" else "ডেঙ্গু হতে পারে। ওআরএস পান করুন, অ্যাসপিরিন/আইবুপ্রোফেন এড়িয়ে চলুন এবং অবস্থা খারাপ হলে ডাক্তার দেখান।"
        }
 
    if fever_7_days:
        return {
            "color": "orange",
            "source": "***Typhoid Suspicion***" if lang == "English" else "***টাইফয়েড সন্দেহ***",
            "message": "Prolonged fever for 7 days or more may suggest typhoid. See a doctor within 24 hours." if lang == "English" else "৭ দিন বা তার বেশি জ্বর থাকলে টাইফয়েড হতে পারে। ২৪ ঘণ্টার মধ্যে ডাক্তার দেখান।"
        }
 
    if symptoms.get("fever", 0) == 1 and severe_joint_pain and rash:
        return {
            "color": "orange",
            "source": "***Chikungunya Suspicion***" if lang == "English" else "***চিকুনগুনিয়া সন্দেহ***",
            "message": "Fever with severe joint pain and rash may suggest chikungunya. See a doctor and maintain fluids." if lang == "English" else "জ্বরের সাথে তীব্র জয়েন্ট ব্যথা ও র‍্যাশ থাকলে চিকুনগুনিয়া হতে পারে। ডাক্তার দেখান এবং পর্যাপ্ত তরল পান করুন।"
        }
 
    if fever_7_days and weight_loss and spleen_fullness:
        return {
            "color": "orange",
            "source": "***Kala-azar Suspicion***" if lang == "English" else "***কালা-আজার সন্দেহ***",
            "message": "Prolonged fever with weight loss and left upper abdominal fullness may suggest kala-azar. Medical testing is needed." if lang == "English" else "দীর্ঘদিনের জ্বর, ওজন কমা ও বাম ওপরের পেট ভারী লাগলে কালা-আজার হতে পারে। পরীক্ষা দরকার।"
        }
 
    if symptoms.get("fever", 0) == 1 and jaundice and muscle_pain and flood_water:
        return {
            "color": "red",
            "source": "***Leptospirosis Suspicion***" if lang == "English" else "***লেপ্টোস্পাইরোসিস সন্দেহ***",
            "message": "Fever with jaundice and severe muscle pain after flood/dirty water exposure can be serious. Go to hospital today." if lang == "English" else "বন্যা/নোংরা পানির সংস্পর্শের পর জ্বর, জন্ডিস ও তীব্র পেশি ব্যথা গুরুতর হতে পারে। আজই হাসপাতালে যান।"
        }
 
    if symptoms.get("fever", 0) == 1 and rash and eschar:
        return {
            "color": "orange",
            "source": "***Scrub Typhus Suspicion***" if lang == "English" else "***স্ক্রাব টাইফাস সন্দেহ***",
            "message": "Fever with rash and black scab/eschar after insect bite may suggest scrub typhus. See a doctor within 24 hours." if lang == "English" else "পোকা কামড়ের পর জ্বর, র‍্যাশ ও কালো দাগ/খোসা হলে স্ক্রাব টাইফাস হতে পারে। ২৪ ঘণ্টার মধ্যে ডাক্তার দেখান।"
        }
 
    if age <= 15 and symptoms.get("fever", 0) == 1 and post_sore_throat_joint:
        return {
            "color": "orange",
            "source": "***Acute Rheumatic Fever Suspicion***" if lang == "English" else "***একিউট রিউম্যাটিক ফিভার সন্দেহ***",
            "message": "Fever and joint pain after sore throat in a child may suggest acute rheumatic fever. Doctor review is needed." if lang == "English" else "শিশুর গলা ব্যথার পর জ্বর ও জয়েন্ট ব্যথা হলে একিউট রিউম্যাটিক ফিভার হতে পারে। ডাক্তার দেখানো দরকার।"
        }
 
    if age <= 12 and symptoms.get("fever", 0) == 1 and mouth_sores and hand_foot_rash:
        return {
            "color": "orange",
            "source": "***Hand Foot Mouth Disease Suspicion***" if lang == "English" else "***হ্যান্ড ফুট মাউথ ডিজিজ সন্দেহ***",
            "message": "Fever with mouth sores and rash/blisters on hands or feet may suggest hand foot mouth disease. Maintain fluids and see a doctor if poor feeding or worsening." if lang == "English" else "জ্বরের সাথে মুখে ঘা এবং হাত/পায়ে র‍্যাশ বা ফোসকা হলে হ্যান্ড ফুট মাউথ ডিজিজ হতে পারে। তরল দিন, খাবার কমে গেলে বা অবস্থা খারাপ হলে ডাক্তার দেখান।"
        }
 #  CARDIAC 
    radiates  = yes(get("cardiac", 1))
    sweating  = yes(get("cardiac", 2))
    sob       = yes(get("cardiac", 3))
    worsens   = yes(get("cardiac", 6))

    if radiates and sweating:
        return {"color": "red", "source": "Probable - ***Cardiac Emergency***"if lang=='English' else "***কার্ডিয়াক ইমার্জেন্সি***",
                "message":( "Pain radiating to arm/jaw + sweating, possible heart attack. Call 999 now." if lang=='English' else "বাহু/চোয়ালে ব্যথা ছড়িয়ে পড়া + ঘাম হওয়া, হার্ট অ্যাটাক হতে পারে। ***এখনই ৯৯৯ নম্বরে ফোন করুন।***")}
    if radiates or (sob and worsens):
        return {"color": "orange", "source": "Probable - ***Cardiac Risk***" if lang=='English' else "***হৃদরোগের ঝুঁকি***",
                "message": ("Possible ***cardiac issue***. Go to hospital within ***1-2 hours***, do not exert.")if lang=='English' else "সম্ভবত হৃদযন্ত্রের সমস্যা। ***১-২ ঘণ্টার মধ্যে হাসপাতালে যান***, কোনো রকম পরিশ্রম করবেন না।"}

 # STROKE 
    sudden_weakness  = yes(get("stroke", 1))
    one_side         = yes(get("stroke", 2))
    speech           = yes(get("stroke", 3))
    face_droop       = yes(get("stroke", 4))
    vision_loss      = yes(get("stroke", 5))
    worst_headache   = yes(get("stroke", 6))

    if any([one_side, speech, face_droop, vision_loss]):
        return {"color": "red", "source": " *** Stroke Emergency ***"if lang=='English' else "স্ট্রোক জরুরি অবস্থা",
                "message": ("Stroke signs detected. ***Call 999 immediately*** — every minute matters."if lang=='English' else "স্ট্রোকের লক্ষণ শনাক্ত হয়েছে। ***অবিলম্বে ৯৯৯ নম্বরে ফোন করুন*** — প্রতিটি মুহূর্ত মূল্যবান।")}
    if sudden_weakness or worst_headache:
        return {"color": "orange", "source": "***Stroke Risk***"if lang=='English' else "স্ট্রোকের ঝুঁকি",
                "message": ("Possible stroke warning. ***Go to hospital now,*** do not wait."if lang=='English' else "স্ট্রোকের সম্ভাব্য সতর্কতা। ***এখনই হাসপাতালে যান***, অপেক্ষা করবেন না।")}

    # PREGNANCY 
    try:
        weeks = int(get("pregnancy", 0).split()[0])
    except:
        weeks = 0

    bleeding_preg  = yes(get("pregnancy", 1))
    no_movement    = no(get("pregnancy", 2))
    severe_pain    = yes(get("pregnancy", 3))
    fluid_leak     = yes(get("pregnancy", 4))
    swelling       = yes(get("pregnancy", 5))
    headache_blur  = yes(get("pregnancy", 6))

    if any([bleeding_preg, severe_pain, fluid_leak, no_movement]):
        return {"color": "red", "source": "Possible-*** Pregnancy Emergency***"if lang=='English' else "সম্ভাব্য-*** গর্ভাবস্থার জরুরি অবস্থা***",
                "message": ("Pregnancy emergency signs detected. Go to hospital immediately."if lang=='English' else "গর্ভাবস্থায় জরুরি লক্ষণ দেখা গেছে। অবিলম্বে হাসপাতালে যান।")}
    if swelling and headache_blur:
        return {"color": "red", "source": "Possible - ***Pre-eclampsia***"if lang=='English' else "সম্ভাব্য - ***প্রি-এক্লাম্পসিয়া***",
                "message": ("Possible pre-eclampsia. ***Immediate hospital visit required.***"if lang=='English' else "প্রি-এক্লাম্পসিয়া হওয়ার সম্ভাবনা আছে। ***অবিলম্বে হাসপাতালে যাওয়া আবশ্যক।***")}

    # SNAKE BITE
    swelling_bite  = yes(get("snake bite", 2))
    swallow_diff   = yes(get("snake bite", 3))
    breath_diff    = yes(get("snake bite", 4))

    if any([swallow_diff, breath_diff]):
        return {"color": "red", "source": "Snake Bite ***(Venomous)***"if lang=='English' else "সাপের কামড় ***(বিষাক্ত)***",
                "message": ("Possible venomous snake bite. ***Go to hospital NOW*** — anti-venom needed urgently."if lang=='English' else "বিষধর সাপের কামড় হতে পারে। ***এখনই হাসপাতালে যান*** — জরুরি ভিত্তিতে প্রতিষেধক প্রয়োজন।")}
    if swelling_bite:
        return {"color": "red", "source": "***Snake Bite***"if lang=='English' else "***সাপের কামড়***",
                "message": ("Snake bite with swelling — treat as venomous. Hospital immediately."if lang=='English' else "সাপের কামড়ে ফোলা দেখা দিলে, বিষধর সাপ হিসেবে বিবেচনা করুন। অবিলম্বে হাসপাতালে নিয়ে যান।")}

    # ANIMAL BITE 
    skin_break     = yes(get("animal bite", 2))
    not_vaccinated = no(get("animal bite", 3))

    if skin_break and not_vaccinated:
        return {"color": "orange", "source": "Possible ***Rabies Risk***"if lang=='English' else '***জলাতঙ্কের*** সম্ভাব্য ঝুঁকি',
                "message": ("Animal bite with broken skin from unvaccinated animal — ***rabies vaccination needed within 24h.***"if lang=='English' else "টিকা না দেওয়া পশুর কামড়ে চামড়া ফেটে গেলে — ***২৪ ঘণ্টার মধ্যে জলাতঙ্কের টিকা নেওয়া আবশ্যক।***")}

    #  DIARRHEA 
    try:
        stool_count = int(get("diarrhea", 0).split()[0])
    except:
        stool_count = 0

    blood_stool    = yes(get("diarrhea", 3))
    poor_urine_d   = no(get("diarrhea", 4))
    dizzy_stand    = yes(get("diarrhea", 5))

    if blood_stool or (stool_count >= 6 and poor_urine_d):
        return {"color": "red", "source": "*** Severe Dehydration/Dysentery***"if lang=='English' else "*** তীব্র পানিশূন্যতা/আমাশয়***",
                "message": ("Severe diarrhea with blood or poor urine output — ***hospital today.***"if lang=='English' else "রক্তাক্ত বা অল্প প্রস্রাবসহ তীব্র ডায়রিয়া — ***আজ হাসপাতালে।***")}
    if stool_count >= 4 or dizzy_stand:
        return {"color": "orange", "source": "*** Dehydration*** Risk"if lang=='English' else "***পানিশূন্যতার*** ঝুঁকি",
                "message": ("Risk of dehydration — drink ORS after every stool, see doctor if no improvement."if lang=='English' else "পানিশূন্যতার ঝুঁকি — প্রতিবার মলত্যাগের পর ওআরএস পান করুন, অবস্থার উন্নতি না হলে ডাক্তারের পরামর্শ নিন।")}

    #  SEIZURE 
    try:
        seizure_mins = int(get("seizure", 0).split()[0])
    except:
        seizure_mins = 0

    lost_consciousness = yes(get("seizure", 1))
    not_recovered      = no(get("seizure", 5))

    if seizure_mins >= 5 or not_recovered:
        return {
        "color": "red",
        "source": "Possible ***Seizure Emergency***" if lang=='English' else "***খিঁচুনির জরুরি অবস্থা***",
        "message": (
            "Prolonged or unresolved seizure — ***emergency care needed immediately.***"
            if lang=='English'
            else "দীর্ঘস্থায়ী বা না থামা খিঁচুনি — ***তাৎক্ষণিক জরুরি চিকিৎসা প্রয়োজন।***"
        )
    }

    #  HEADACHE 
    sudden_headache = yes(get("headache", 1))
    worst_ever      = yes(get("headache", 2))
    neck_stiff      = yes(get("headache", 4))
    blurred_vis     = yes(get("headache", 5))

    if worst_ever or (sudden_headache and neck_stiff):
         return {
        "color": "red",
        "source": "Possible ***Meningitis / Brain Emergency***" if lang=='English'
                  else "***মস্তিষ্ক/মেনিনজাইটিস জরুরি ঝুঁকি***",
        "message": (
            "Sudden severe headache with neck stiffness — ***go to hospital immediately.***"
            if lang=='English'
            else "হঠাৎ তীব্র মাথাব্যথা ও ঘাড় শক্ত — ***অবিলম্বে হাসপাতালে যান।***"
        )
    }
    if blurred_vis and sudden_headache:
        return {
        "color": "orange",
        "source": "Possible ***Neurological Warning***" if lang=='English'
                  else "***স্নায়বিক সতর্কতা***",
        "message": (
            "Headache with blurred vision — ***seek medical care today.***"
            if lang=='English'
            else "মাথাব্যথার সাথে দৃষ্টিশক্তি ঝাপসা — ***আজই চিকিৎসা নিন।***"
        )
    }

    # PESTICIDE POISONING 
    breath_pest  = yes(get("pesticide poisoning", 4))
    confused_pest = yes(get("pesticide poisoning", 5))

    if breath_pest or confused_pest:
         return {
        "color": "red",
        "source": "Possible ***Pesticide Poisoning***" if lang=='English'
                  else "***কীটনাশক বিষক্রিয়া***",
        "message": (
            "Pesticide exposure with breathing difficulty or confusion — ***emergency treatment required now.***"
            if lang=='English'
            else "কীটনাশক বিষক্রিয়া + শ্বাসকষ্ট/বিভ্রান্তি — ***তাৎক্ষণিক জরুরি চিকিৎসা প্রয়োজন।***"
        )
    }

    #  ABDOMINAL PAIN 
    blood_vomit_stool = yes(get("abdominal pain", 7))
    pain_spreads      = yes(get("abdominal pain", 9))
    sudden_pain       = yes(get("abdominal pain", 2)) and "sudden" in get("abdominal pain", 2)

    if blood_vomit_stool or (sudden_pain and pain_spreads):
        return {
        "color": "red",
        "source": "Possible ***Acute Abdomen Emergency***" if lang=='English'
                  else "***তীব্র পেটের জরুরি অবস্থা***",
        "message": (
            "Severe abdominal symptoms — ***possible surgical emergency, go to hospital now.***"
            if lang=='English'
            else "তীব্র পেটের উপসর্গ — ***সম্ভাব্য সার্জিক্যাল জরুরি অবস্থা, এখনই হাসপাতালে যান।***"
        )
    }

    #  MENSURATION 
    heavy_bleeding  = yes(get("mensuration", 1)) and "more" in get("mensuration", 1)
    large_clots     = yes(get("mensuration", 3))
    dizzy_menses    = yes(get("mensuration", 5))
    regular = yes(get("mensuration", 7))
    fever_discharge = yes(get("mensuration", 8))

    if large_clots and dizzy_menses and heavy_bleeding:
        return {
        "color": "red",
        "source": "Possible ***Severe Menstrual Bleeding***" if lang=='English'
                  else "***তীব্র মাসিক রক্তক্ষরণ***",
        "message": (
            "Heavy menstrual bleeding with dizziness — ***possible anemia emergency, seek care now.***"
            if lang=='English'
            else "অতিরিক্ত মাসিক রক্তক্ষরণ + মাথা ঘোরা — ***সম্ভাব্য অ্যানিমিয়া জরুরি অবস্থা, এখনই চিকিৎসা নিন।***"
        )
    }
    if regular and  heavy_bleeding:
        return {
        "color": "orange",
        "source": "Possible ***Severe Bleeding***" if lang=='English'
                  else "***তীব্র মাসিক রক্তক্ষরণ***",
        "message": (
            "Heavy menstrual bleeding with dizziness — ***possible anemia emergency, seek care now.***"
            if lang=='English'
            else "অতিরিক্ত মাসিক রক্তক্ষরণ + মাথা ঘোরা — ***সম্ভাব্য অ্যানিমিয়া জরুরি অবস্থা, এখনই চিকিৎসা নিন।***"
        )
    }
    if fever_discharge:
         return {
        "color": "orange",
        "source": "Possible ***Pelvic Infection***" if lang=='English'
                  else "***পেলভিক সংক্রমণের সম্ভাবনা***",
        "message": (
            "Fever with abnormal discharge — ***possible infection, see doctor within 24h.***"
            if lang=='English'
            else "জ্বর ও অস্বাভাবিক স্রাব — ***সম্ভাব্য সংক্রমণ, ২৪ ঘণ্টার মধ্যে ডাক্তার দেখান।***"
        )
    }

    return result