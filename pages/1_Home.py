from io import BytesIO
import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from modules.FIRSTAID import get_first_aid
from modules.model_backend import load_model_and_features, predict_triage
from modules.BanglaSymptoms import extract_bangla_symptoms
from modules.gemini_helper import generate_ai_response
from modules.FIRSTAID import SYMPTOM_FIRST_AID, SPECIAL_FIRST_AID
from modules.triage_rules import apply_bd_rules
from modules.offline_detector import detect_local_emergency, detect_local_emergencies
from modules.Followup import FOLLOWUP_GROUPS, detect_followup_categories
from modules.symptom_normalizer import normalize_symptom_input
from modules.condition_groups import apply_condition_group_rules
from gtts import gTTS

try:
    from streamlit_mic_recorder import speech_to_text
except Exception:
    speech_to_text = None
try:
    from streamlit_js_eval import get_geolocation
except Exception:
    get_geolocation = None

import database as db
from components.login import require_login, logout_button
from components.header import load_css, render_header, render_warning_banner
from components.symptom_cards import render_symptom_selector
from components.result_card import (
    show_triage_card, normalize_color, format_prediction_driver,
    get_active_symptom_keys,
)
from components.risk_meter import render_confidence
from components.recommendation import get_specialist_referral_clustered, format_additional_concerns
from components.bottom_nav import render_nav
from utils import (
    extract_english_symptoms, detect_extra_display_symptoms, create_gray_result,
    create_structured_referral_pdf, get_tts_summary_bangla, create_tts_audio,
)
from i18n import TEXTS, BANGLA_FEATURES, EXTRA_DISPLAY_SYMPTOMS

st.set_page_config(page_title="GramDoctor AI — Home", page_icon="🩺", layout="centered")

require_login()
db.init_db()
load_css(st.session_state.get("pref_theme", "light"))

GD_LOADER_HTML = """
<style>
.wrapper {
  width: 200px;
  height: 60px;
  position: relative;
  z-index: 1;
  margin: 40px auto;
}
.circle {
  width: 20px;
  height: 20px;
  position: absolute;
  border-radius: 50%;
  background-color: #2563eb;
  left: 15%;
  transform-origin: 50%;
  animation: circle7124 .5s alternate infinite ease;
}
@keyframes circle7124 {
  0% { top: 60px; height: 5px; border-radius: 50px 50px 25px 25px; transform: scaleX(1.7); }
  40% { height: 20px; border-radius: 50%; transform: scaleX(1); }
  100% { top: 0%; }
}
.circle:nth-child(2) { left: 45%; animation-delay: .2s; }
.circle:nth-child(3) { left: auto; right: 15%; animation-delay: .3s; }
.shadow {
  width: 20px;
  height: 4px;
  border-radius: 50%;
  background-color: rgba(0,0,0,0.2);
  position: absolute;
  top: 62px;
  transform-origin: 50%;
  z-index: -1;
  left: 15%;
  filter: blur(1px);
  animation: shadow046 .5s alternate infinite ease;
}
@keyframes shadow046 {
  0% { transform: scaleX(1.5); }
  40% { transform: scaleX(1); opacity: .7; }
  100% { transform: scaleX(.2); opacity: .4; }
}
.shadow:nth-child(4) { left: 45%; animation-delay: .2s }
.shadow:nth-child(5) { left: auto; right: 15%; animation-delay: .3s; }
</style>
<div class="wrapper">
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="shadow"></div>
    <div class="shadow"></div>
    <div class="shadow"></div>
</div>
"""


#---follow up labels-----


YES_NO_LABELS = {
    "English": {"yes": "Yes", "no": "No"},
    "বাংলা": {"yes": "হ্যাঁ", "no": "না"},
}


YES_NO_STARTERS_EN = ("is ", "are ", "do ", "does ", "did ", "have ", "has ", "can ", "will ", "was ", "were ")

def is_yes_no_question(q):
    q_clean = q.strip().lower()
    if q_clean.startswith(YES_NO_STARTERS_EN):
        return True
    tokens = q.strip().rstrip("?।").split()
    if "কি" in tokens:
        return True
    return False


def get_matched_symptoms_display(cat, symptoms_dict, language):
    from modules.Followup import FOLLOWUP_GROUPS
    group_data = FOLLOWUP_GROUPS.get(cat, {})
    triggers = group_data.get("triggers_en", []) + group_data.get("triggers_bn", [])
    normalized_symptoms = {k.lower().strip(): v for k, v in symptoms_dict.items()}

    matched = []
    for trigger in triggers:
        t = trigger.lower().strip()
        for sym, val in normalized_symptoms.items():
            if val == 1 and (t == sym or t in sym or sym in t):
                display = BANGLA_FEATURES.get(sym, sym) if language == "বাংলা" else sym
                if display not in matched:
                    matched.append(display)
    return matched

def load_resources():
    return load_model_and_features()


if "app_ready" not in st.session_state:
    loader = st.empty()
    loader.markdown(GD_LOADER_HTML, unsafe_allow_html=True)
    model, feature_cols = load_resources()
    st.session_state.app_ready = True
    st.session_state._model_cache = (model, feature_cols)
    loader.empty()
else:
    model, feature_cols = st.session_state._model_cache

model, feature_cols = load_resources()

language = st.selectbox(
    "🌐 Language / ভাষা",
    ["English", "বাংলা"],
    index=0,
    key="language_selector"
)

t = TEXTS[language]

render_header(t)
render_warning_banner(t)

with st.expander(
    "ℹ️ How does GramDoctor AI decide?" if language == "English" else "ℹ️ GramDoctor AI কীভাবে সিদ্ধান্ত নেয়?",
    expanded=False
):
    if language == "English":
        st.markdown("""
**Safety comes first, AI comes last.**

1. **Fixed medical safety rules** run first — 32 hand-authored red-flag and orange-flag rules, built directly into the code. If your symptoms match a known emergency pattern, this decides the result immediately, before any AI is involved.
2. **A trained triage model** (92% accuracy, tested on 10,000+ patient records) handles the cases the safety rules don't catch.
3. **AI (Gemini) only explains** the result in plain language afterward — it can never change or override the medical decision made above it.

Same symptoms → same safety-critical answer, every time. It's never left to an AI's guess.
""")
    else:
        st.markdown("""
**নিরাপত্তা আগে, AI সবার শেষে।**

১. **নির্দিষ্ট মেডিকেল নিরাপত্তা নিয়ম** সবার আগে কাজ করে — কোডে সরাসরি তৈরি ৩২টি রেড-ফ্ল্যাগ ও অরেঞ্জ-ফ্ল্যাগ নিয়ম। লক্ষণ কোনো পরিচিত জরুরি প্যাটার্নের সাথে মিললে, AI জড়িত হওয়ার আগেই এটি ফলাফল নির্ধারণ করে।
২. **একটি প্রশিক্ষিত ট্রায়াজ মডেল** (৯৩% নির্ভুলতা) বাকি কেসগুলো পরিচালনা করে।
৩. **AI (Gemini) শুধু ফলাফল ব্যাখ্যা করে** সহজ ভাষায় — এটি কখনও উপরের চিকিৎসা সিদ্ধান্ত পরিবর্তন করতে পারে না।

একই লক্ষণে সবসময় একই নিরাপত্তা-গুরুত্বপূর্ণ উত্তর — এটি AI-এর অনুমানের উপর নির্ভর করে না।
""")

with st.sidebar:
    st.title(t["sidebar_title"])
    st.markdown(t["sidebar_help"])
    st.divider()
    st.title(t["demo_title"])
    st.markdown(t["demo_cases"])
    st.divider()
    st.caption(f"Logged in as **{st.session_state.get('username', '')}**")
    logout_button()

# ---- session state defaults (unchanged keys/behaviour) ----
for key, default in [
    ("triage_result", None), ("symptoms", None), ("ai_response", None),
    ("voice_text", ""), ("referral", None), ("alternate_referral", None),
    ("first_aid", None), ("detected_special", "none"), ("extra_symptoms", []),
    ("condition_group_matches", []), ("followup_done", False), ("history_saved", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


st.markdown(f'<div class="gd-card-heading">🧾 {t["patient_info"]}</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    age_display = st.selectbox(
        t["age"],
        [t["under_1_year"]] + list(range(1, 121)),
        index=21
    )
    age = 0 if age_display == t["under_1_year"] else int(age_display)

with col2:
    sex_display = st.selectbox(t["sex"], [t["male"], t["female"]])

with col3:
    if sex_display == t["male"]:
        pregnancy_display = t["not_applicable"]
        st.selectbox(t["pregnancy"], [t["not_applicable"]], disabled=True)
    else:
        pregnancy_display = st.selectbox(t["pregnancy"], [t["no"], t["yes"]])

st.markdown(f'<div class="gd-card-heading">✍️ {t["write"]}</div>', unsafe_allow_html=True)
st.caption(t['subwrite'])
bangla_text = st.text_area(t["text_input"], placeholder=t["text_placeholder"], label_visibility="collapsed")

# ============== VOICE INPUT (unchanged logic, only appearance restyled) ==============
st.markdown(f'<div class="gd-mic-label">🎤 {t["voice_input"]}</div>', unsafe_allow_html=True)
st.caption(t["voice_help"])

if speech_to_text is not None:
    st.markdown('<div class="gd-mic-wrap">', unsafe_allow_html=True)
    with st.spinner("Listening…" if language == "English" else "শোনা হচ্ছে…"):
     voice_result = speech_to_text(
        language="bn-BD" if language == "বাংলা" else "en-US",
        use_container_width=True,
        just_once=True,
        key="voice_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if voice_result:
        st.session_state.voice_text = voice_result

    if st.session_state.voice_text:
        st.success(st.session_state.voice_text)
        if st.button(t["clear_voice"], key="clear_voice_button"):
            st.session_state.voice_text = ""
            st.rerun()
else:
    st.info(t["voice_unavailable"])


st.markdown(f'<div class="gd-card-heading">🩺 {t["symptoms"]}</div>', unsafe_allow_html=True)
selected_symptoms, sorted_symptoms = render_symptom_selector(t, language, feature_cols)



predict_clicked = st.button(t["check_triage"], type="primary", key="check_triage_button", use_container_width=True)

if predict_clicked:
    with st.spinner("Analyzing symptoms..." if language == "English" else "লক্ষণ বিশ্লেষণ হচ্ছে..."):

        symptoms = {}
        symptoms["age"] = int(age)
        symptoms["sex-no"] = 1 if sex_display == t["female"] else 0

        if sex_display == t["male"]:
            symptoms["ispregnant"] = 2   # Not Applicable
        else:
            symptoms["ispregnant"] = 1 if pregnancy_display == t["yes"] else 0

        for symptom_name, value in selected_symptoms.items():
            symptoms[symptom_name] = value

        combined_text = f"{bangla_text}\n{st.session_state.voice_text}".strip()
        st.session_state.extra_symptoms = detect_extra_display_symptoms(combined_text)

        bangla_extracted = extract_bangla_symptoms(combined_text, feature_cols)
        english_extracted = extract_english_symptoms(combined_text, feature_cols)

        for symptom_name, value in bangla_extracted.items():
            symptoms[symptom_name] = value
        for symptom_name, value in english_extracted.items():
            symptoms[symptom_name] = value

        active_symptom_count = sum(
            value for key, value in symptoms.items()
            if key not in ["age", "sex-no", "ispregnant"]
        )

        local_specials = detect_local_emergencies(combined_text, SPECIAL_FIRST_AID)
        local_special = local_specials[0] if local_specials else None

        if local_special:
            special = local_special
        else:
            from modules.gemini_helper import detect_special_emergency
            special = detect_special_emergency(combined_text)

        if active_symptom_count > 0:
            result = predict_triage(symptoms, model, feature_cols)
        else:
            result = create_gray_result(language)

        result, group_matches = apply_condition_group_rules(
            symptoms,
            result,
            st.session_state.extra_symptoms,
            language,
        )
        st.session_state.condition_group_matches = group_matches

        if special.get("found"):
            color_messages = {
                "red": "Possible {cond} detected. This needs urgent medical attention.",
                "orange": "Possible {cond} detected. Please visit a doctor within 1-2 days.",
                "green": "Possible {cond} detected. This can usually be managed at home, but watch for worsening.",
            }
            color_messages_bn = {
                "red": "সম্ভাবনা: {cond}। এটি জরুরি চিকিৎসা প্রয়োজন।",
                "orange": "সম্ভাবনা: {cond}। ১-২ দিনের মধ্যে ডাক্তার দেখান।",
                "green": "সম্ভাবনা: {cond}। বাড়িতে যত্ন নেওয়া যায়, কিন্তু অবস্থা খারাপ হলে ডাক্তার দেখান।",
            }

            cond = ", ".join(item["condition"] for item in local_specials) if local_specials else special["condition"]
            special_color = special["color"]
            if any(item.get("color") == "red" for item in local_specials):
                special_color = "red"

            order = ["green", "orange", "red"]
            current_color = result.get("color", "green")
            if current_color not in order:
                current_color = "green"

            if order.index(special_color) >= order.index(current_color):
                if language == "বাংলা":
                    message = color_messages_bn[special_color].format(cond=cond)
                else:
                    message = color_messages[special_color].format(cond=cond)

                result = {
                    "color": special_color,
                    "source": "Special emergency detection",
                    "message": message,
                    "confidence": None
                }

            st.session_state.detected_special = special
            st.session_state.detected_specials = local_specials or [special]
        else:
            st.session_state.detected_special = None
            st.session_state.detected_specials = []

        st.session_state.symptoms = symptoms
        st.session_state.triage_result = result
        st.session_state.original_triage_color = result["color"]
        st.session_state.original_triage_message = result["message"]
        st.session_state.original_triage_source = result["source"]
        detected_special = st.session_state.get("detected_special")
        st.session_state.followup_categories = detect_followup_categories(symptoms, FOLLOWUP_GROUPS, language, detected_special)
        st.session_state.ai_response = None
        st.session_state.first_aid = None
        st.session_state.tts_audio = None
        
        st.session_state.followup_done = False
        st.session_state.history_saved = False

        if st.session_state.get("detected_special") and st.session_state.detected_special.get("found"):
            st.session_state.referral = "Emergency Department" if language == "English" else "জরুরি বিভাগ"
            st.session_state.alternate_referral = "General Physician" if language == "English" else "জেনারেল ফিজিশিয়ান"
            st.session_state.specialist_key = None
        else:
            st.session_state.referral = None
            st.session_state.alternate_referral = None


if st.session_state.triage_result is not None:

    cats = st.session_state.get("followup_categories", [])
    show_followup_gate = bool(cats) and not st.session_state.followup_done

    if show_followup_gate:
        st.markdown("<hr class='gd-divider'>", unsafe_allow_html=True)
        st.markdown(f'<div class="gd-card-heading">❓ {t["follow-up"]}</div>', unsafe_allow_html=True)
        st.caption(
            "A few quick questions help us give you a more accurate result."
            if language == "English"
            else "কয়েকটি প্রশ্নের উত্তর দিলে আরও সঠিক ফলাফল পাওয়া যাবে।"
        )

        followup_answers = {}
        for cat_idx, cat in enumerate(cats):
            matched_syms = get_matched_symptoms_display(cat, st.session_state.symptoms, language)

            if language == "English":
               st.markdown(f"**Because you mentioned:** {', '.join(matched_syms) if matched_syms else 'your symptoms'}")
               st.caption(f"We're asking a few extra questions related to **{cat.title()}** to be safe — this does *not* mean you have it.Please make sure to answer fever days otherwise we will not be able to detect your probable disease.")
            else:
               st.markdown(f"**আপনি উল্লেখ করেছেন:** {', '.join(matched_syms) if matched_syms else 'আপনার লক্ষণ'}")
               st.caption(f"নিরাপত্তার জন্য **{cat.title()}**-সম্পর্কিত কিছু অতিরিক্ত প্রশ্ন জিজ্ঞাসা করা হচ্ছে — এর মানে এই নয় যে আপনার এটি আছে।অনুগ্রহ করে জ্বরের দিনগুলোর তথ্য অবশ্যই উল্লেখ করবেন, অন্যথায় আমরা আপনার সম্ভাব্য রোগটি শনাক্ত করতে পারব না।")
            qs = FOLLOWUP_GROUPS[cat]["questions_bn" if language == "বাংলা" else "questions_en"]
            DURATION_VALUE_MAP = {
    "English": {"Less than 3 days": "2", "3–5 days": "4", "5–7 days": "6", "More than 7 days": "8"},
    "বাংলা": {"৩ দিনের কম": "2", "৩-৫ দিনের মধ্যে": "4", "৫-৭ দিনের মধ্যে": "6", "৭ দিনের বেশি": "8"},
}

            for i, q in enumerate(qs):
                key = f"fu_{cat_idx}_{cat}_{i}"
                if is_yes_no_question(q):
                    labels = YES_NO_LABELS[language]
                    answer = st.radio(q, [labels["yes"], labels["no"]], key=key, index=None, horizontal=True)
                    followup_answers[key] = answer or ""
                else:
                   followup_answers[key] = st.text_input(q, key=key)
        col_a, col_b = st.columns(2)
        with col_a:
            update_clicked = st.button(
                "Get My Result" if language == "English" else "ট্রায়াজ আপডেট করুন",
                type="primary", key="update_triage_button", use_container_width=True
            )
        with col_b:
            skip_clicked = st.button(
                "Skip — show result now" if language == "English" else "এড়িয়ে যান — ফলাফল দেখুন",
                key="skip_followup_button", use_container_width=True
            )

        if update_clicked:
            with st.spinner("Updating triage..." if language == "English" else "ট্রায়াজ আপডেট হচ্ছে..."):
                for k, v in followup_answers.items():
                    st.session_state.symptoms[k] = v

                st.session_state.followup_answers = followup_answers
                result = predict_triage(st.session_state.symptoms, model, feature_cols)
                result = apply_bd_rules(st.session_state.symptoms, result, followup_answers, language)
                result, group_matches = apply_condition_group_rules(
                    st.session_state.symptoms,
                    result,
                    st.session_state.get("extra_symptoms", []),
                    language,
                )
                from modules.FIRSTAID import get_first_aid_from_followup
                st.session_state.first_aid = get_first_aid_from_followup(
                    followup_answers,
                    language,
                    symptoms=st.session_state.symptoms,
                    triage_color=st.session_state.triage_result["color"]
                )
                st.session_state.triage_result = result
                st.session_state.condition_group_matches = group_matches
                st.session_state.tts_audio = None
                st.session_state.followup_done = True
            st.rerun()

        if skip_clicked:
            st.session_state.followup_done = True
            st.rerun()

    else:
        st.markdown("<hr class='gd-divider'>", unsafe_allow_html=True)
        if cats:  # follow-up questions exist for this result but were skipped
         if st.button(
            "↩️ Answer follow-up questions" if language == "English" else "↩️ ফলো-আপ প্রশ্নে ফিরে যান",
            key="reopen_followup_button", use_container_width=True
        ):
            st.session_state.followup_done = False
            st.rerun()
        st.markdown(f'<div class="gd-section-title">📋 {t["triage_result"]}</div>', unsafe_allow_html=True)

        result = st.session_state.triage_result
        color = normalize_color(result["color"])

        if st.session_state.referral:
            referral = st.session_state.referral
            alternate_referral = st.session_state.alternate_referral
            specialist_key = st.session_state.get("specialist_key")
        else:
            referral, alternate_referral, specialist_key = get_specialist_referral_clustered(
                result, st.session_state.symptoms, language
            )
            st.session_state.specialist_key = specialist_key
            
        special = st.session_state.get("detected_special")
        special_events = st.session_state.get("detected_specials", [])
        # ── 1. Triage card (colour + message) ──────────────────────────────
        show_triage_card(color, language)
        if result.get("source") and "***" in result.get("source", ""):
              st.markdown(f"**{result['source'].replace('***', '')}**")
        

        group_matches = st.session_state.get("condition_group_matches", [])
        if group_matches and not special_events:
            st.markdown("**Grouped symptom patterns:**" if language == "English" else "**সমন্বিত লক্ষণের প্যাটার্ন:**")
            for item in group_matches[:3]:
                st.write(f"- {item['source']}: {item['message']}")
        # ── 2. Confidence score ─────────────────────────────────────────────
        render_confidence(result.get("confidence"), language)

        # ── 3. Detected symptoms (user needs to see WHAT was found first) ───
        active_symptoms = [
            BANGLA_FEATURES.get(symptom, symptom) if language == "বাংলা" else symptom
            for symptom, value in st.session_state.symptoms.items()
            if value == 1 and symptom not in ["age", "sex-no", "ispregnant"]
        ]
        for extra_symptom in st.session_state.get("extra_symptoms", []):
            active_symptoms.append(
                BANGLA_FEATURES.get(extra_symptom, extra_symptom)
                if language == "বাংলা"
                else EXTRA_DISPLAY_SYMPTOMS.get(extra_symptom, {}).get("English", extra_symptom.replace("_", " ").title())
            )

        if active_symptoms:
            st.subheader(t["detected_symptoms"])
            cols = st.columns(3)
            for i, symptom in enumerate(active_symptoms):
                cols[i % 3].markdown(f"🔹 {symptom}")
        else:
            st.info(t["no_symptoms"])

        st.divider()

        # ── 4. Prediction drivers (explainability) ──────────────────────────
        explanation = result.get("explanation") or []
        explanation_lines = [format_prediction_driver(item, result.get("color")) for item in explanation]
        explanation_lines = [line for line in explanation_lines if line]
        if explanation_lines:
            with st.expander("🔍 Why this result?" if language == "English" else "🔍 এই ফলাফল কেন?"):
                st.caption("Decision source: " + result["source"])
                for line in explanation_lines:
                    st.write(f"- {line}")

        # ── 5. First aid ────────────────────────────────────────────────────
        

        if result["source"] == "Special emergency detection" and special_events:
            steps_en, steps_bn = [], []
            for event in special_events:
                steps_en.append(f"{event['condition']}:")
                steps_en.extend(event.get("advice_en", []))
                steps_bn.append(f"{event['condition']}:")
                steps_bn.extend(event.get("advice_bn", []))
            first_aid = {
                "condition": "Multiple Injury/Event First Aid" if len(special_events) > 1 else special_events[0]["condition"],
                "steps_en": steps_en,
                "steps_bn": steps_bn,
            }
        else:
            first_aid = st.session_state.get("first_aid") or get_first_aid(st.session_state.symptoms, language)

        label = f"🩹 First Aid: {first_aid['condition']}" if language == "English" else f"🩹 প্রাথমিক চিকিৎসা: {first_aid['condition']}"
        with st.expander(label, expanded=color == "red"):
            if "steps_en" in first_aid:
                steps = first_aid["steps_bn"] if language == "বাংলা" else first_aid["steps_en"]
            else:
                steps = first_aid["steps"]
            for i, step in enumerate(steps, 1):
                st.markdown(f"**{i}.** {step}")

        st.divider()

        if referral:
            st.markdown(f'<div class="gd-recommend-card"><b>{t["refer_to"]}</b> {referral}</div>', unsafe_allow_html=True)
        if alternate_referral:
            st.markdown(f'<div class="gd-recommend-card">{t["alternate_referral"]} {alternate_referral}</div>', unsafe_allow_html=True)
        from components.recommendation import render_doctor_suggestions
        if specialist_key:
            render_doctor_suggestions(specialist_key, language)
             
        concern_lines = format_additional_concerns(st.session_state.symptoms, language, primary_specialist=referral)
        if concern_lines and not special_events:
            st.markdown("**Additional possible concerns:**" if language == "English" else "**অতিরিক্ত সম্ভাব্য সমস্যা:**")
            for line in concern_lines:
                st.write(f"- {line}")

        
        
        st.subheader(t["ai_title"])
        if color == "gray":
              st.info(
              "No specific symptoms were detected — please describe your symptoms more clearly, or consult a doctor if you're concerned."
               if language == "English" else
              "কোনো নির্দিষ্ট লক্ষণ শনাক্ত করা যায়নি — অনুগ্রহ করে লক্ষণগুলো আরও স্পষ্টভাবে লিখুন, অথবা উদ্বিগ্ন হলে ডাক্তারের পরামর্শ নিন।"
    )  
        else :
          if st.button(t["generate_ai"], key="generate_ai_button"):
             with st.spinner(t["generating"]):
                 st.session_state.ai_response = generate_ai_response(
                 st.session_state.symptoms, st.session_state.triage_result
            )

        if st.session_state.ai_response:
          with st.container(key="gd_ai_card"):
            st.markdown(f'<div class="gd-ai-badge">🤖 {t["ai_title"]}</div>', unsafe_allow_html=True)
            st.markdown(st.session_state.ai_response)
        

            

        try:
          with st.spinner("Preparing PDF…" if language == "English" else "PDF তৈরি হচ্ছে…"):
            pdf_buffer = create_structured_referral_pdf(
            st.session_state.ai_response, st.session_state.triage_result,
            st.session_state.symptoms, referral=referral, first_aid=first_aid,
        )
            st.markdown(f'<div class="gd-card-heading">📄 {t["download_pdf"]}</div>', unsafe_allow_html=True)
            st.download_button(label=t["download_pdf"], data=pdf_buffer, file_name=t["pdf_filename"],
                        mime="application/pdf", use_container_width=True)
        except Exception:
          pass  

        # NEW: log this completed result to history once per prediction
        from components.login import is_guest
        if not st.session_state.history_saved and not is_guest():
            db.save_history_entry(
                user_id=st.session_state.user_id,
                language=language,
                symptoms=st.session_state.symptoms,
                active_symptoms=active_symptoms,
                triage_result=result,
                referral=referral,
                alternate_referral=alternate_referral,
                followup_answers=st.session_state.get("followup_answers"),
                ai_response=st.session_state.ai_response,
            )
            st.session_state.history_saved = True
else:
    st.info(t["no_result"])

render_nav(active="Home")