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

def apply_bd_rules(symptoms, result, followup_answers=None):
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

    abdominal_pain   = yes(get("dengue", 5))
    bleeding         = yes(get("dengue", 6))
    poor_urine       = no(get("dengue", 7))
    rash             = yes(get("dengue", 11))
    confused         = yes(get("dengue", 12))
    poor_fluids      = no(get("dengue", 10))

    if fever_days >= 3 and any([abdominal_pain, bleeding, poor_urine, confused]):
        return {"color": "red", "source": "BD Rules — Dengue Warning Signs",
                "message": "Dengue warning signs detected. Go to hospital today. Do NOT take ibuprofen or aspirin."}
    if fever_days >= 7:
        return {"color": "orange", "source": "BD Rules — Typhoid Suspicion",
                "message": "Prolonged fever over 7 days — possible typhoid. See doctor within 24 hours."}
    if fever_days >= 3 and (rash or poor_fluids):
        return {"color": "orange", "source": "BD Rules — Dengue Suspected",
                "message": "Possible dengue. Monitor closely, drink ORS, avoid aspirin/ibuprofen. See doctor if worsens."}

 #  CARDIAC 
    radiates  = yes(get("cardiac", 1))
    sweating  = yes(get("cardiac", 2))
    sob       = yes(get("cardiac", 3))
    worsens   = yes(get("cardiac", 6))

    if radiates and sweating:
        return {"color": "red", "source": "Probable - ***Cardiac Emergency***",
                "message": "Pain radiating to arm/jaw + sweating, possible heart attack. Call 999 now."}
    if radiates or (sob and worsens):
        return {"color": "orange", "source": "Probable - ***Cardiac Risk***",
                "message": "Possible ***cardiac issue***. Go to hospital within ***1-2 hours***, do not exert."}

    # ── STROKE ──────────────────────────────────────────────────────────
    sudden_weakness  = yes(get("stroke", 1))
    one_side         = yes(get("stroke", 2))
    speech           = yes(get("stroke", 3))
    face_droop       = yes(get("stroke", 4))
    vision_loss      = yes(get("stroke", 5))
    worst_headache   = yes(get("stroke", 6))

    if any([one_side, speech, face_droop, vision_loss]):
        return {"color": "red", "source": "BD Rules — Stroke Emergency",
                "message": "Stroke signs detected. Call 999 immediately — every minute matters."}
    if sudden_weakness or worst_headache:
        return {"color": "orange", "source": "BD Rules — Stroke Risk",
                "message": "Possible stroke warning. Go to hospital now, do not wait."}

    # ── PREGNANCY ───────────────────────────────────────────────────────
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
        return {"color": "red", "source": "BD Rules — Pregnancy Emergency",
                "message": "Pregnancy emergency signs detected. Go to hospital immediately."}
    if swelling and headache_blur:
        return {"color": "red", "source": "BD Rules — Pre-eclampsia",
                "message": "Possible pre-eclampsia. Immediate hospital visit required."}

    # ── SNAKE BITE ──────────────────────────────────────────────────────
    swelling_bite  = yes(get("snake bite", 2))
    swallow_diff   = yes(get("snake bite", 3))
    breath_diff    = yes(get("snake bite", 4))

    if any([swallow_diff, breath_diff]):
        return {"color": "red", "source": "BD Rules — Snake Bite (Venomous)",
                "message": "Possible venomous snake bite. Go to hospital NOW — anti-venom needed urgently."}
    if swelling_bite:
        return {"color": "red", "source": "BD Rules — Snake Bite",
                "message": "Snake bite with swelling — treat as venomous. Hospital immediately."}

    # ── ANIMAL BITE ─────────────────────────────────────────────────────
    skin_break     = yes(get("animal bite", 2))
    not_vaccinated = no(get("animal bite", 3))

    if skin_break and not_vaccinated:
        return {"color": "orange", "source": "BD Rules — Rabies Risk",
                "message": "Animal bite with broken skin from unvaccinated animal — rabies vaccination needed within 24h."}

    # ── DIARRHEA ────────────────────────────────────────────────────────
    try:
        stool_count = int(get("diarrhea", 0).split()[0])
    except:
        stool_count = 0

    blood_stool    = yes(get("diarrhea", 3))
    poor_urine_d   = no(get("diarrhea", 4))
    dizzy_stand    = yes(get("diarrhea", 5))

    if blood_stool or (stool_count >= 6 and poor_urine_d):
        return {"color": "red", "source": "BD Rules — Severe Dehydration/Dysentery",
                "message": "Severe diarrhea with blood or poor urine output — hospital today."}
    if stool_count >= 4 or dizzy_stand:
        return {"color": "orange", "source": "BD Rules — Dehydration Risk",
                "message": "Risk of dehydration — drink ORS after every stool, see doctor if no improvement."}

    # ── SEIZURE ─────────────────────────────────────────────────────────
    try:
        seizure_mins = int(get("seizure", 0).split()[0])
    except:
        seizure_mins = 0

    lost_consciousness = yes(get("seizure", 1))
    not_recovered      = no(get("seizure", 5))

    if seizure_mins >= 5 or not_recovered:
        return {"color": "red", "source": "BD Rules — Seizure Emergency",
                "message": "Prolonged or unresolved seizure — emergency care now."}

    # ── HEADACHE ────────────────────────────────────────────────────────
    sudden_headache = yes(get("headache", 1))
    worst_ever      = yes(get("headache", 2))
    neck_stiff      = yes(get("headache", 4))
    blurred_vis     = yes(get("headache", 5))

    if worst_ever or (sudden_headache and neck_stiff):
        return {"color": "red", "source": "BD Rules — Possible Meningitis/Aneurysm",
                "message": "Sudden severe headache with neck stiffness — go to hospital immediately."}
    if blurred_vis and sudden_headache:
        return {"color": "orange", "source": "BD Rules — Headache with Visual Symptoms",
                "message": "Headache with blurred vision — see doctor today."}

    # ── PESTICIDE POISONING ──────────────────────────────────────────────
    breath_pest  = yes(get("pesticide poisoning", 4))
    confused_pest = yes(get("pesticide poisoning", 5))

    if breath_pest or confused_pest:
        return {"color": "red", "source": "BD Rules — Pesticide Poisoning",
                "message": "Pesticide poisoning with breathing difficulty or confusion — emergency now."}

    # ── ABDOMINAL PAIN ───────────────────────────────────────────────────
    blood_vomit_stool = yes(get("abdominal pain", 7))
    pain_spreads      = yes(get("abdominal pain", 9))
    sudden_pain       = yes(get("abdominal pain", 2)) and "sudden" in get("abdominal pain", 2)

    if blood_vomit_stool or (sudden_pain and pain_spreads):
        return {"color": "red", "source": "BD Rules — Acute Abdomen",
                "message": "Severe abdominal signs — possible surgical emergency. Go to hospital now."}

    # ── MENSURATION ──────────────────────────────────────────────────────
    heavy_bleeding  = yes(get("mensuration", 1)) and "more" in get("mensuration", 1)
    large_clots     = yes(get("mensuration", 3))
    dizzy_menses    = yes(get("mensuration", 5))
    fever_discharge = yes(get("mensuration", 8))

    if large_clots and dizzy_menses:
        return {"color": "red", "source": "BD Rules — Severe Menstrual Bleeding",
                "message": "Heavy menstrual bleeding with dizziness — possible anemia emergency, see doctor today."}
    if fever_discharge:
        return {"color": "orange", "source": "BD Rules — Possible Infection",
                "message": "Fever with abnormal discharge — possible pelvic infection, see doctor within 24h."}

    return result