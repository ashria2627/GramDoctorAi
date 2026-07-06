

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
            st.success("GREEN — বাসায় পর্যবেক্ষণ")
            st.markdown("""
            <div class="gd-triage-body">
            <b>অর্থ:</b> বর্তমান তথ্য অনুযায়ী লক্ষণগুলো কম ঝুঁকিপূর্ণ মনে হচ্ছে। আপনি যদি এখনও <b>ফলো-আপ</b> প্রশ্নগুলোর উত্তর না দিয়ে থাকেন, তবে অনুগ্রহ করে তা দিয়ে দিন, যাতে আপনি আপনার বর্তমান অবস্থার জন্য নিখুঁত সুপারিশ পেতে পারেন।<br><br>
            <b>করণীয়:</b> বিশ্রাম, পর্যাপ্ত পানি এবং লক্ষণ পর্যবেক্ষণ।<br><br>
            <b>চিকিৎসা নিন যদি:</b> লক্ষণ বাড়ে, জ্বর থাকে, বা বিপদ সংকেত দেখা যায়।
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("GREEN — Home care / observe")
            st.markdown("""
            <div class="gd-triage-body">
            <b>Meaning:</b> Current symptoms appear low risk based on triage input. If you have not yet answered <b>follow-up</b> questions, please do so you get perfect recommendation for your current condition.<br><br>
            <b>Recommended action:</b> Rest, drink fluids, and monitor symptoms.<br><br>
            <b>Seek care if:</b> symptoms worsen, fever persists, or danger signs appear.
            </div>
            """, unsafe_allow_html=True)

    elif color == "orange":
        if language == "বাংলা":
            st.warning("ORANGE - পর্যবেক্ষণে রাখুন। উপসর্গ বেড়ে গেলে বা অবস্থার অবনতি হলে ১–২ দিনের মধ্যে চিকিৎসকের পরামর্শ নিন।  ")
            st.markdown("""
            <div class="gd-triage-body">
            <b>অর্থ:</b> লক্ষণগুলো চিকিৎসকের মূল্যায়ন প্রয়োজন হতে পারে। আপনি যদি এখনও <b>ফলো-আপ</b> প্রশ্নগুলোর উত্তর না দিয়ে থাকেন, তবে অনুগ্রহ করে তা দিয়ে দিন, যাতে আপনি আপনার বর্তমান অবস্থার জন্য নিখুঁত সুপারিশ পেতে পারেন।<br><br>
            <b>করণীয়:</b> <b>২৪-৪৮ ঘণ্টার</b> মধ্যে ডাক্তার, ক্লিনিক বা উপজেলা স্বাস্থ্য কমপ্লেক্সে যান।<br><br>
            <b>জরুরি চিকিৎসা নিন যদি:</b> দুর্বলতা, পানিশূন্যতা, তীব্র ব্যথা বা শ্বাসকষ্ট বাড়ে।
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("ORANGE — Observe and if worsen Visit doctor within 1-2 days")
            st.markdown("""
            <div class="gd-triage-body">
            <b>Meaning:</b> Symptoms need medical review but may not be an immediate emergency. If you have not yet answered <b>follow-up questions</b>, please do so you get perfect recommendation for your current condition.<br><br>
            <b>Recommended action:</b> Visit a local doctor, clinic, or Upazila Health Complex within <b>24-48 hours.</b><br><br>
            <b>Seek urgent care if:</b> weakness, dehydration, severe pain, or breathing difficulty worsens.
            </div>
            """, unsafe_allow_html=True)

    elif color == "red":
        if language == "বাংলা":
            st.error("RED — এখনই জরুরি চিকিৎসা নিন")
            st.markdown("""
            <div class="gd-triage-body">
            <b>অর্থ:</b> জরুরি বিপদ সংকেত থাকতে পারে।<br><br>
            <b>করণীয়:</b> এখনই নিকটস্থ হাসপাতাল বা <b>জরুরি বিভাগে যান।</b><br><br>
            <b>করবেন না:</b> বাসায় অপেক্ষা করবেন না বা চিকিৎসা নিতে দেরি করবেন না।
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("RED — Emergency care now")
            st.markdown("""
            <div class="gd-triage-body">
            <b>Meaning:</b> Emergency red-flag silent symptoms may be present.<br><br>
            <b>Recommended action:</b> Go to the nearest <b>emergency department immediately.</b><br><br>
            <b>Do not:</b> wait at home or delay medical care.
            </div>
            """, unsafe_allow_html=True)

    elif color == "gray":
        if language == "বাংলা":
            st.info("GRAY — লক্ষণ বোঝা যায়নি")
            st.markdown("""
            <div class="gd-triage-body">
            আপনি কি কোনো লক্ষণ বোঝাতে চেয়েছেন?<br><br>
            অনুগ্রহ করে স্পষ্টভাবে লক্ষণ লিখুন বা বলুন, যেমন: জ্বর, বমি, কাশি, শ্বাসকষ্ট।
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("GRAY — Symptom unclear")
            st.markdown("""
            <div class="gd-triage-body">
            No recognized symptom was detected from the input.<br><br>
            Are you trying to describe a symptom?<br><br>
            Please write or speak symptoms clearly, for example: fever, vomiting, cough, shortness of breath.
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info(f"Unknown triage result: {color}")