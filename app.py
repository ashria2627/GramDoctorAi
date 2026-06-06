import streamlit as st

from modules.model_backend import load_model_and_features, predict_triage
from modules.BanglaSymptoms import extract_bangla_symptoms
from modules.gemini_helper import generate_ai_response


st.set_page_config(
    page_title="GramDoctor AI",
    page_icon="🩺",
    layout="centered"
)


def show_triage_card(color):
    if color == "green":
        st.success("GREEN — Home care / observe")
        st.markdown("""
        **Meaning:** Current symptoms appear low risk based on triage input.  
        **Recommended action:** Rest, drink fluids, and monitor symptoms.  
        **Seek care if:** symptoms worsen, fever persists, or danger signs appear.
        """)

    elif color == "orange":
        st.warning("ORANGE — Visit doctor within 1–2 days")
        st.markdown("""
        **Meaning:** Symptoms need medical review but may not be an immediate emergency.  
        **Recommended action:** Visit a local doctor, clinic, or Upazila Health Complex within 24–48 hours.  
        **Seek urgent care if:** weakness, dehydration, severe pain, or breathing difficulty worsens.
        """)

    elif color == "red":
        st.error("RED — Emergency care now")
        st.markdown("""
        **Meaning:** Emergency red-flag symptoms may be present.  
        **Recommended action:** Go to the nearest emergency department immediately.  
        **Do not:** wait at home or delay medical care.
        """)

    else:
        st.info(f"Unknown triage result: {color}")


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


st.sidebar.title("Demo Cases")

st.sidebar.markdown("""
**Green case:**  
কাশি, নাক বন্ধ

**Orange case:**  
জ্বর, বমি, দুর্বলতা

**Red case:**  
বুকে তীব্র ব্যথা, ঘাম, শ্বাসকষ্ট
""")

st.sidebar.info(
    "Use these examples during demo to show green, orange, and red triage outputs."
)


if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if "symptoms" not in st.session_state:
    st.session_state.symptoms = None

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None


tab1, tab2 = st.tabs(["Patient Form", "Result"])


with tab1:
    st.header("Patient Information")

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=30
    )

    sex = st.selectbox(
        "Sex",
        ["Male", "Female"]
    )

    pregnancy = st.selectbox(
        "Pregnancy Status",
        ["Not applicable", "No", "Yes"]
    )

    bangla_text = st.text_area(
        "Describe symptoms in Bangla",
        placeholder="যেমন: আমার ৪ দিন ধরে জ্বর, বমি, পেট ব্যথা হচ্ছে"
    )

    uploaded_file = st.file_uploader(
        "Optional: Upload patient symptom note",
        type=["txt"]
    )

    uploaded_text = ""

    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8")
        st.text_area("Uploaded note preview", uploaded_text, height=150)

    st.header("Symptoms")

    manual_fields = ["age", "sex-no", "ispregnant"]

    symptom_features = [
        col for col in feature_cols
        if col not in manual_fields
    ]

    selected_symptoms = {}

    cols = st.columns(3)

    for index, symptom in enumerate(symptom_features[:60]):
        with cols[index % 3]:
            selected_symptoms[symptom] = 1 if st.checkbox(symptom.title()) else 0

    if st.button("Check Triage", type="primary", key="check_triage_button"):
        symptoms = {}

        symptoms["age"] = int(age)
        symptoms["sex-no"] = 1 if sex == "Female" else 0

        if pregnancy == "Yes":
            symptoms["ispregnant"] = 1
        elif pregnancy == "No":
            symptoms["ispregnant"] = 0
        else:
            symptoms["ispregnant"] = 2

        for symptom_name, value in selected_symptoms.items():
            symptoms[symptom_name] = value

        combined_text = f"{bangla_text}\n{uploaded_text}"
        bangla_extracted = extract_bangla_symptoms(combined_text, feature_cols)

        for symptom_name, value in bangla_extracted.items():
            symptoms[symptom_name] = value

        result = predict_triage(symptoms, model, feature_cols)

        st.session_state.symptoms = symptoms
        st.session_state.triage_result = result
        st.session_state.ai_response = None

        st.success("Triage completed. Open the Result tab.")


with tab2:
    st.header("Triage Result")

    if st.session_state.triage_result is None:
        st.info("No result yet. Fill the patient form first.")

    else:
        result = st.session_state.triage_result
        color = result["color"]

        show_triage_card(color)

        st.write("Decision source:", result["source"])
        st.write("Reason:", result["message"])

        active_symptoms = [
            symptom for symptom, value in st.session_state.symptoms.items()
            if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
        ]

        if active_symptoms:
            st.subheader("Detected Symptoms")
            for symptom in active_symptoms:
                st.write(f"- {symptom}")
        else:
            st.info("No specific symptom detected from the current input.")

        st.divider()

        if st.button("Generate AI Explanation", key="generate_ai_button"):
            with st.spinner("Generating AI explanation..."):
                ai_response = generate_ai_response(
                    st.session_state.symptoms,
                    st.session_state.triage_result
                )

            st.session_state.ai_response = ai_response

        if st.session_state.ai_response:
            st.subheader("AI Explanation and Referral Note")
            st.markdown(st.session_state.ai_response)