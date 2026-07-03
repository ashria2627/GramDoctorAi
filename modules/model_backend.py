import pickle
import pandas as pd
from modules.triage_rules import check_red_flags

try:
    import shap
except Exception:
    shap = None


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


def red_flag_scope_limiter(symptoms):
    """
    Prevents broad symptoms such as difficulty breathing from becoming emergency
    by themselves. Emergency is reserved for serious standalone symptoms or
    clinically meaningful symptom combinations.
    """
    symptoms = {k.lower().strip(): v for k, v in symptoms.items()}

    serious_single_symptoms = [
        "blindness",
        "seizures",
        "fainting",
        "vomiting blood",
        "rectal bleeding",
        "blood in stool",
        "involuntary urination",
        "loss of sensation",
        "slurring words",
        "irregular heartbeat",
        "spots or clouds in vision",
    ]

    if any(symptoms.get(symptom, 0) == 1 for symptom in serious_single_symptoms):
        return {
            "color": "red",
            "source": "Safety rules",
            "message": "Emergency symptoms detected. Seek medical care.",
            "confidence": None,
        }

    breathing_symptom = (
        symptoms.get("shortness of breath", 0) == 1
        or symptoms.get("difficulty breathing", 0) == 1
    )
    breathing_danger_pair = any(
        symptoms.get(symptom, 0) == 1
        for symptom in ["sharp chest pain", "chest pain", "fainting", "sweating", "hemoptysis"]
    )

    if breathing_symptom and breathing_danger_pair:
        return {
            "color": "red",
            "source": "Safety rules",
            "message": "Breathing difficulty with danger signs detected. Seek emergency care.",
            "confidence": None,
        }

    return None


def red_flag_override(symptoms):
    scoped_result = red_flag_scope_limiter(symptoms)
    if scoped_result:
        return scoped_result

    red_result = check_red_flags(symptoms)
    if red_result == "red":
        return {
            "color": "red",
            "source": "Safety rules",
            "message": "Emergency red-flag symptoms detected. Immediately visit a doctor. You might be showing silent symptoms of something serious.",
            "confidence": None,
        }

    return None


def explain_prediction(model, input_df, feature_cols, top_n=5):
    if shap is None:
        return []

    try:
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(input_df)

        if isinstance(values, list):
            predicted_class = int(model.predict(input_df)[0])
            values = values[predicted_class]

        row_values = values[0]
        meta_features = {"age", "sex-no", "ispregnant"}
        ranked = sorted(
            [
                (feature, value)
                for feature, value in zip(feature_cols, row_values)
                if feature not in meta_features and abs(float(value)) > 0.0001
            ],
            key=lambda item: abs(float(item[1])),
            reverse=True,
        )
        return [
            {"feature": feature, "impact": round(float(value), 4)}
            for feature, value in ranked[:top_n]
        ]
    except Exception:
        return []


def check_orange_flags(symptoms):
    """
    Orange means the patient should visit a doctor within 24-48 hours.
    These are not immediate emergency rules, but symptoms need clinical review.
    """

    # Common symptoms become orange only when they cluster or persist with warning signs.
    fever_cluster = (
        symptoms.get("fever", 0) == 1
        and (
            symptoms.get("vomiting", 0) == 1
            or symptoms.get("weakness", 0) == 1
            or symptoms.get("chills", 0) == 1
            or symptoms.get("skin rash", 0) == 1
            or symptoms.get("cough", 0) == 1
            or symptoms.get("headache", 0) == 1
        )
    )
    headache_cluster = (
        symptoms.get("headache", 0) == 1
        and (
            symptoms.get("dizziness", 0) == 1
            or symptoms.get("vomiting", 0) == 1
            or symptoms.get("diminished vision", 0) == 1
            or symptoms.get("fever", 0) == 1
        )
    )
    weakness_cluster = (
        symptoms.get("weakness", 0) == 1
        and (
            symptoms.get("dizziness", 0) == 1
            or symptoms.get("decreased appetite", 0) == 1
            or symptoms.get("palpitations", 0) == 1
            or symptoms.get("fever", 0) == 1
        )
    )

    if fever_cluster or headache_cluster or weakness_cluster:
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

    
    symptoms = {k.lower().strip(): v for k, v in symptoms.items()}

    override_result = red_flag_override(symptoms)
    if override_result:
        return override_result

    active_symptoms = [
        k for k, v in symptoms.items()
        if v == 1 and k not in ["age", "sex-no", "ispregnant"]
    ]

    
    if len(active_symptoms) < 1:
        return {
            "color": "grey",
            "source": "Minimum symptom threshold",
            "message": "Too few symptoms. Monitor or visit clinic if persists.",
            "confidence": None
        }
    orange_result = check_orange_flags(symptoms)
    if orange_result == "orange":
        return {
            "color": "orange",
            "source": "Warning rules",
            "message": "Observe your condition. If worsen in the next 1-2days then Visit a doctor.",
            "confidence": None
        }
    if len(active_symptoms) < 2:
        return {
            "color": "green",
            "source": "Symptom threshold",
            "message": "You are fine. Drink water and take rest !",
            "confidence": None
        }
    input_df = make_input_dataframe(symptoms, feature_cols)
    prediction = model.predict(input_df)[0]
    confidence = round(max( model.predict_proba(input_df)[0]) * 100, 1)
    color = LABELS.get(prediction, str(prediction))
    shap_drivers = explain_prediction(model, input_df, feature_cols)

    if confidence<95 and color== 'red':
        return{
            "color": "orange",
            "source": "Low confidence fallback",
            "message": f"Uncertain prediction ({confidence}%). Please consult a doctor.",
            "confidence": confidence,
            "explanation": shap_drivers
        }
    
    if confidence < 40:
        return {
            "color": "orange",
            "source": "Low confidence fallback",
            "message": f"Uncertain prediction ({confidence}%). Please consult a doctor.",
            "confidence": confidence,
            "explanation": shap_drivers
        }
    

    if color=='orange':
        return {
            "color": "orange",
            "source": "Machine Learning Model",
            "message": f"Observe your condition. If worsen then visit a doctor within 24-48 hours.",
            "confidence": confidence,
            "explanation": shap_drivers
        }
    if color=='red':
        return {
            "color": "red",
            "source": "Machine Learning Model",
            "message": f"Emergency symptoms detected . Please consult a doctor within few hours.",
            "confidence": confidence,
            "explanation": shap_drivers
        }
    if color=='green':
        return {
            "color": "green",
            "source": "Machine Learning Model",
            "message": f"Do not worry!! you are doing fine. Overthinking will make it worse.",
            "confidence": confidence,
            "explanation": shap_drivers
        }
