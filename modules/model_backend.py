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


def make_input_dataframe(symptoms, feature_cols):
    input_row = {col: symptoms.get(col, 0) for col in feature_cols}
    input_df = pd.DataFrame([input_row], columns=feature_cols)
    return input_df


def predict_triage(symptoms, model, feature_cols):
    rule_result = check_red_flags(symptoms)

    if rule_result == "red":
        return {
            "color": "red",
            "source": "Safety rule",
            "message": "Emergency red-flag symptoms detected."
        }

    input_df = make_input_dataframe(symptoms, feature_cols)
    prediction = model.predict(input_df)[0]

    color = LABELS.get(prediction, str(prediction))

    return {
        "color": color,
        "source": "Machine learning model",
        "message": "Prediction generated from selected symptoms."
    }