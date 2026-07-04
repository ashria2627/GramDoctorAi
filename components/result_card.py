"""
components/result_card.py
Renders the colored triage/diagnosis card and small display helpers.
Functions moved verbatim from the original app.py — no logic changed.
"""

import streamlit as st
from i18n import BANGLA_FEATURES

def normalize_color(color):
    if not color:
        return "gray"

    color = str(color).lower().strip()

    if color == "grey":
        return "gray"

    return color


def get_symptom_display(symptom, language):
    if language == "বাংলা":
        return BANGLA_FEATURES.get(symptom, symptom)
    return symptom.title()


def get_active_symptom_keys(symptoms):
    if not symptoms:
        return []

    return [
        symptom for symptom, value in symptoms.items()
        if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
    ]



def format_prediction_driver(item, triage_color=None):
    feature = str(item.get("feature", "This factor")).replace("_", " ").title()
    impact = float(item.get("impact", 0))

    if abs(impact) < 0.0001:
        return None

    direction = "increased" if impact > 0 else "reduced"
    target = f" the {triage_color} result" if triage_color else " this triage result"
    return f"{feature} {direction} confidence in{target}."


def show_triage_card(color, language):
    if color == "green":
        if language == "বাংলা":
            st.success("GREEN — বাসায় পর্যবেক্ষণ")
            st.markdown("""
            **অর্থ:** বর্তমান তথ্য অনুযায়ী লক্ষণগুলো কম ঝুঁকিপূর্ণ মনে হচ্ছে। আপনি যদি এখনও ***ফলো-আপ*** প্রশ্নগুলোর উত্তর না দিয়ে থাকেন, তবে অনুগ্রহ করে তা দিয়ে দিন, যাতে আপনি আপনার বর্তমান অবস্থার জন্য নিখুঁত সুপারিশ পেতে পারেন।
             
            **করণীয়:** বিশ্রাম, পর্যাপ্ত পানি এবং লক্ষণ পর্যবেক্ষণ।  
            
            **চিকিৎসা নিন যদি:** লক্ষণ বাড়ে, জ্বর থাকে, বা বিপদ সংকেত দেখা যায়।
            """)
        else:
            st.success("GREEN — Home care / observe")
            st.markdown("""
            **Meaning:** Current symptoms appear low risk based on triage input. If you have not yet answered ***follow-up*** questions ,please do so you get perfect recommendation for your current condition.  
             
            **Recommended action:** Rest, drink fluids, and monitor symptoms.  
            
            **Seek care if:** symptoms worsen, fever persists, or danger signs appear.
            """)

    elif color == "orange":
        if language == "বাংলা":
            st.warning("ORANGE - পর্যবেক্ষণে রাখুন। উপসর্গ বেড়ে গেলে বা অবস্থার অবনতি হলে ১–২ দিনের মধ্যে চিকিৎসকের পরামর্শ নিন।  ")
            st.markdown("""
            **অর্থ:** লক্ষণগুলো চিকিৎসকের মূল্যায়ন প্রয়োজন হতে পারে। আপনি যদি এখনও ***ফলো-আপ*** প্রশ্নগুলোর উত্তর না দিয়ে থাকেন, তবে অনুগ্রহ করে তা দিয়ে দিন, যাতে আপনি আপনার বর্তমান অবস্থার জন্য নিখুঁত সুপারিশ পেতে পারেন। 
            
            **করণীয়:** **২৪-৪৮ ঘণ্টার** মধ্যে ডাক্তার, ক্লিনিক বা উপজেলা স্বাস্থ্য কমপ্লেক্সে যান। 
             
            **জরুরি চিকিৎসা নিন যদি:** দুর্বলতা, পানিশূন্যতা, তীব্র ব্যথা বা শ্বাসকষ্ট বাড়ে।
            """)
        else:
            st.warning("ORANGE — Observe and if worsen Visit doctor within 1-2 days")
            st.markdown("""
            **Meaning:** Symptoms need medical review but may not be an immediate emergency. If you have not yet answered  ***follow-up questions*** ,please do so you get perfect recommendation for your current condition.
            
            **Recommended action:** Visit a local doctor, clinic, or Upazila Health Complex within **24-48 hours.**
            
            **Seek urgent care if:** weakness, dehydration, severe pain, or breathing difficulty worsens.
            """)

    elif color == "red":
        if language == "বাংলা":
            st.error("RED — এখনই জরুরি চিকিৎসা নিন")
            st.markdown("""
            **অর্থ:** জরুরি বিপদ সংকেত থাকতে পারে।
              
            **করণীয়:** এখনই নিকটস্থ হাসপাতাল বা ***জরুরি বিভাগে যান।*** 
            
            **করবেন না:** বাসায় অপেক্ষা করবেন না বা চিকিৎসা নিতে দেরি করবেন না।
            """)
        else:
            st.error("RED — Emergency care now")
            st.markdown("""
            **Meaning:** Emergency red-flag silent symptoms may be present. 
             
            **Recommended action:** Go to the nearest ***emergency department immediately.***
             
            **Do not:** wait at home or delay medical care.
            """)

    elif color == "gray":
        if language == "বাংলা":
            st.info("GRAY — লক্ষণ বোঝা যায়নি")
            st.markdown("""
            আপনি কি কোনো লক্ষণ বোঝাতে চেয়েছেন?  
            
            অনুগ্রহ করে স্পষ্টভাবে লক্ষণ লিখুন বা বলুন, যেমন: জ্বর, বমি, কাশি, শ্বাসকষ্ট।
            """)
        else:
            st.info("GRAY — Symptom unclear")
            st.markdown("""
            No recognized symptom was detected from the input.  
             
            Are you trying to describe a symptom?  
            
            Please write or speak symptoms clearly, for example: fever, vomiting, cough, shortness of breath.
            """)

    else:
        st.info(f"Unknown triage result: {color}")

