import streamlit as st
from modules.model_backend import load_model_and_features, predict_triage


st.set_page_config(
    page_title="GramDoctor AI",
    page_icon="🩺",
    layout="centered"
)


@st.cache_resource
def load_resources():
    return load_model_and_features()


model, feature_cols = load_resources()


st.title("GramDoctor AI")
st.subheader("Bangla AI Triage and Referral Assistant")

st.warning(
    "This tool does not provide a final diagnosis. "
    "It only gives triage guidance. "
    "For emergency symptoms, seek immediate medical care."
)


if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if "symptoms" not in st.session_state:
    st.session_state.symptoms = None


tab1, tab2 = st.tabs(["Patient Form", "Result"])


with tab1:
    st.header("Patient Information")

    age = st.number_input("Age", min_value=0, max_value=120, value=30)

    sex = st.selectbox(
        "Sex",
        ["Male", "Female"]
    )

    pregnancy = st.selectbox(
        "Pregnancy Status",
        ["Not applicable", "No", "Yes"]
    )

    st.header("Symptoms")

    fever = st.checkbox("Fever")
    chest_pain = st.checkbox("Chest pain")
    weakness = st.checkbox("Weakness")
    headache = st.checkbox("Headache")
    sweating = st.checkbox("Sweating")
    shortness_of_breath = st.checkbox("Shortness of breath")
    vomiting = st.checkbox("Vomiting")

    if st.button("Check Triage", type="primary"):
        symptoms = {}

        symptoms["age"] = int(age)
        symptoms["sex-no"] = 1 if sex == "Female" else 0

        if pregnancy == "Yes":
            symptoms["ispregnant"] = 1
        elif pregnancy == "No":
            symptoms["ispregnant"] = 0
        else:
            symptoms["ispregnant"] = 2

        symptoms["fever"] = 1 if fever else 0
        symptoms["sharp chest pain"] = 1 if chest_pain else 0
        symptoms["weakness"] = 1 if weakness else 0
        symptoms["headache"] = 1 if headache else 0
        symptoms["sweating"] = 1 if sweating else 0
        symptoms["shortness of breath"] = 1 if shortness_of_breath else 0
        symptoms["vomiting"] = 1 if vomiting else 0

        result = predict_triage(symptoms, model, feature_cols)

        st.session_state.symptoms = symptoms
        st.session_state.triage_result = result

        st.success("Triage completed. Open the Result tab.")


with tab2:
    st.header("Triage Result")

    if st.session_state.triage_result is None:
        st.info("No result yet. Fill the patient form first.")
    else:
        result = st.session_state.triage_result
        color = result["color"]

        if color == "green":
            st.success("GREEN — Stay at home and observe")
            st.write("Suggested action: rest, fluids, symptom monitoring, and follow-up if symptoms worsen.")

        elif color == "orange":
            st.warning("ORANGE — Visit doctor within 1–2 days")
            st.write("Suggested action: visit a local doctor, clinic, or Upazila Health Complex within 24–48 hours.")

        elif color == "red":
            st.error("RED — Emergency visit now")
            st.write("Suggested action: go to the nearest emergency department immediately.")

        st.write("Decision source:", result["source"])
        st.write("Reason:", result["message"])