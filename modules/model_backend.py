import pickle
import pandas as pd
from modules.triage_rules import check_red_flags


LABELS = {
    0: "green",
    1: "orange",
    2: "red"
}


def load_model_and_features():
    model = pickle.load(open("used_model.pkl", "rb"))
    feature_cols = pickle.load(open("feature_cols.pkl", "rb"))
    return model, feature_cols


def load_anomaly_model():
    anomaly_model = pickle.load(open("anomaly_model.pkl", "rb"))
    anomaly_cols = pickle.load(open("deterioration_feature_cols.pkl", "rb"))
    anomaly_threshold = pickle.load(open("anomaly_threshold.pkl", "rb"))
    return anomaly_model, anomaly_cols, anomaly_threshold


def predict_deterioration(vitals, anomaly_model, anomaly_cols, threshold):
    row = {col: vitals.get(col, 0) for col in anomaly_cols}
    input_df = pd.DataFrame([row], columns=anomaly_cols)
    proba = anomaly_model.predict_proba(input_df)[0][1]
    anomaly = int(proba >= threshold)
    return anomaly, round(proba * 100, 1)

def get_deterioration_recommendations(vitals, language="English"):
    recs_en, recs_bn = [], []

    if vitals.get("heart_rate", 80) > 120 or vitals.get("heart_rate", 80) < 50:
        recs_en.append("Abnormal heart rate — continuous monitoring needed.")
        recs_bn.append("হৃদস্পন্দন অস্বাভাবিক — নিয়মিত পর্যবেক্ষণ প্রয়োজন।")

    if vitals.get("spo2_pct", 98) < 92:
        recs_en.append("Low oxygen saturation — consider oxygen support.")
        recs_bn.append("অক্সিজেন মাত্রা কম — অক্সিজেন সাপোর্ট প্রয়োজন হতে পারে।")

    if vitals.get("temperature_c", 37) > 39:
        recs_en.append("High fever — start cooling, recheck in 1 hour.")
        recs_bn.append("উচ্চ জ্বর — শরীর ঠান্ডা করুন, ১ ঘণ্টা পর পুনরায় মাপুন।")

    if vitals.get("systolic_bp", 120) < 90:
        recs_en.append("Low blood pressure — risk of shock.")
        recs_bn.append("নিম্ন রক্তচাপ — শক হওয়ার ঝুঁকি আছে।")

    if vitals.get("respiratory_rate", 16) > 24:
        recs_en.append("Fast breathing — monitor airway closely.")
        recs_bn.append("শ্বাসের গতি বেশি — শ্বাসনালী খেয়াল রাখুন।")

    if vitals.get("crp_level", 5) > 50:
        recs_en.append("High CRP — possible severe infection, blood tests advised.")
        recs_bn.append("উচ্চ CRP — গুরুতর সংক্রমণের সম্ভাবনা, রক্ত পরীক্ষা করুন।")

    if vitals.get("wbc_count", 7) > 12:
        recs_en.append("Elevated WBC count — infection markers present.")
        recs_bn.append("WBC বেশি — সংক্রমণের লক্ষণ আছে।")

    if vitals.get("hemoglobin", 13) < 9:
        recs_en.append("Low hemoglobin — anemia evaluation needed.")
        recs_bn.append("কম হিমোগ্লোবিন — রক্তশূন্যতা পরীক্ষা প্রয়োজন।")

    if vitals.get("comorbidity_index", 0) >= 2:
        recs_en.append("Multiple existing conditions — handle with extra caution.")
        recs_bn.append("একাধিক রোগ আছে — অতিরিক্ত সতর্কতা প্রয়োজন।")
    if vitals.get("oxygen_flow", 0) > 0:
      recs_en.append("Patient is on supplemental oxygen — monitor SpO2 closely for changes.")
      recs_bn.append("রোগী অক্সিজেন সাপোর্টে আছে — SpO2 নিয়মিত পর্যবেক্ষণ করুন।")
    if vitals.get("creatinine", 1) > 1.5:
        recs_en.append("Elevated creatinine — possible kidney function concern, monitor fluids.")
        recs_bn.append("ক্রিয়েটিনিন বেশি — কিডনি সমস্যার সম্ভাবনা, তরল গ্রহণ নিয়ন্ত্রণ করুন।")
    if vitals.get("hour_from_admission", 0) > 24:
       recs_en.append("Patient has been admitted over 24 hours — reassess overall trend, not just current vitals.")
       recs_bn.append("রোগী ২৪ ঘণ্টার বেশি ভর্তি আছেন — সামগ্রিক অবস্থার পরিবর্তন পর্যালোচনা করুন।")

    if not recs_en:
        recs_en.append("Vitals within normal range. Continue routine monitoring.")
        recs_bn.append("ভাইটাল স্বাভাবিক সীমার মধ্যে। নিয়মিত পর্যবেক্ষণ চালিয়ে যান।")

    return recs_bn if language == "বাংলা" else recs_en

def make_input_dataframe(symptoms, feature_cols):
    input_row = {col: symptoms.get(col, 0) for col in feature_cols}
    input_df = pd.DataFrame([input_row], columns=feature_cols)
    return input_df


def check_orange_flags(symptoms):
    """
    Orange means the patient should visit a doctor within 24-48 hours.
    These are not immediate emergency rules, but symptoms need clinical review.
    """

    # Fever-related moderate risk
    if symptoms.get("fever", 0) == 1 or  symptoms.get("vomiting", 0) == 1 or symptoms.get("weakness", 0) == 1 or symptoms.get("headache", 0) == 1 or symptoms.get("chills", 0) == 1:
        return "orange"

    # Gastrointestinal symptoms needing review
    if symptoms.get("diarrhea", 0) == 1 and (
        symptoms.get("vomiting", 0) == 1
        or symptoms.get("weakness", 0) == 1
        or symptoms.get("sharp abdominal pain", 0) == 1
    ):
        return "orange"

    # Urinary symptoms
    if symptoms.get("painful urination", 0) == 1 or symptoms.get("frequent urination", 0) == 1:
        return "orange"

    # Eye symptoms that are not red alone
    if symptoms.get("diminished vision", 0) == 1 or symptoms.get("pain in eye", 0) == 1:
        return "orange"

    # Bleeding symptoms without severe weakness/red combination
    if (
        symptoms.get("nosebleed", 0) == 1
        or symptoms.get("blood in stool", 0) == 1
        or symptoms.get("blood in urine", 0) == 1
        or symptoms.get("heavy menstrual flow", 0) == 1
    ):
        return "orange"

    # Pregnancy-related symptoms should be reviewed
    if symptoms.get("ispregnant", 2) == 1 and (
        symptoms.get("nausea", 0) == 1
        or symptoms.get("vomiting", 0) == 1
        or symptoms.get("lower abdominal pain", 0) == 1
        or symptoms.get("pelvic pain", 0) == 1
    ):
        return "orange"

    # Respiratory symptoms needing doctor visit if not red
    if symptoms.get("cough", 0) == 1 and (
        symptoms.get("fever", 0) == 1
        or symptoms.get("wheezing", 0) == 1
        or symptoms.get("coughing up sputum", 0) == 1
    ):
        return "orange"

    # Persistent/general weakness with other symptoms
    if symptoms.get("weakness", 0) == 1 and (
        symptoms.get("decreased appetite", 0) == 1
        or symptoms.get("dizziness", 0) == 1
        or symptoms.get("palpitations", 0) == 1
    ):
        return "orange"

    # # Pain symptoms that may need clinical evaluation
    if (
        symptoms.get("back pain", 0) == 1
        or symptoms.get("leg pain", 0) == 1
        or symptoms.get("knee pain", 0) == 1
        or symptoms.get("arm pain", 0) == 1
        or symptoms.get("lower abdominal pain", 0) == 1
        or symptoms.get("pelvic pain", 0) == 1
    ):
        return "orange"

    return None

def predict_triage(symptoms, model, feature_cols):

    # Normalize keys (VERY IMPORTANT)
    symptoms = {k.lower().strip(): v for k, v in symptoms.items()}

    SERIOUS_SINGLE_SYMPTOMS = [
        "shortness of breath", "blindness", "seizures", "fainting",
        "vomiting blood", "rectal bleeding", "blood in stool",
        "involuntary urination", "loss of sensation", "slurring words",
        "irregular heartbeat", "spots or clouds in vision",
        "difficulty breathing","sharp chest pain"
    ]

    SERIOUS_SINGLE_SYMPTOMS = [s.lower().strip() for s in SERIOUS_SINGLE_SYMPTOMS]

    
    if any(symptoms.get(s, 0) == 1 for s in SERIOUS_SINGLE_SYMPTOMS):
        return {
            "color": "red",
            "source": "Safety rules",
            "message": "Emergency symptoms detected. Seek medical care."
        }
    active_symptoms = [
        k for k, v in symptoms.items()
        if v == 1 and k not in ["age", "sex-no", "ispregnant"]
    ]

    
    if len(active_symptoms) < 1:
        return {
            "color": "grey",
            "source": "Minimum symptom threshold",
            "message": "Too few symptoms. Monitor or visit clinic if persists."
        }
    orange_result = check_orange_flags(symptoms)
    if orange_result == "orange":
        return {
            "color": "orange",
            "source": "Warning rules",
            "message": "Observe your condition. If worsen in the next 1-2days then Visit a doctor."
        }
    if len(active_symptoms) < 2:
        return {
            "color": "green",
            "source": "Symptom threshold",
            "message": "You are fine. Drink water and take rest !"
        }
    
    red_result = check_red_flags(symptoms)
    if red_result == "red":
        return {
            "color": "red",
            "source": "Safety rules",
            "message": "Emergency red-flag symptoms detected. Immediately visit a doctor . YOu might be showing silent symptoms of something serious"
        }

    
 
        
    
    input_df = make_input_dataframe(symptoms, feature_cols)
    prediction = model.predict(input_df)[0]
    confidence = round(max( model.predict_proba(input_df)[0]) * 100, 1)
    color = LABELS.get(prediction, str(prediction))

    if confidence<95 and color== 'red':
        return{
            "color": "orange",
            "source": "Low confidence fallback",
            "message": f"Uncertain prediction ({confidence}%). Please consult a doctor."
        }
    
    if confidence < 40:
        return {
            "color": "orange",
            "source": "Low confidence fallback",
            "message": f"Uncertain prediction ({confidence}%). Please consult a doctor."
        }
    

    if color=='orange':
        return {
            "color": "orange",
            "source": "Machine Learning Model",
            "message": f"Observe your condition. If worsen then visit a doctor within 24–48 hours."
        }
    if color=='red':
        return {
            "color": "red",
            "source": "Machine Learning Model",
            "message": f"Emergency symptoms detected . Please consult a doctor within few hours."
        }
    if color=='green':
        return {
            "color": "green",
            "source": "Machine Learning Model",
            "message": f"Do not worry!! you are doing fine. Overthinking will make it worse."
        }
