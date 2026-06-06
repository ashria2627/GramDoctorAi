# GramDoctor AI

GramDoctor AI is a Bangla AI-powered triage and referral assistant for rural Bangladesh. It accepts Bangla symptom input, detects red-flag symptoms, predicts triage urgency using a trained machine learning model, and generates patient-friendly advice with a referral note.

## Features

- Streamlit web interface
- Patient information form
- Bangla symptom input
- Bangla symptom-to-model feature mapping
- Optional patient note file upload
- Rule-based red-flag safety layer
- Machine learning triage prediction
- Gemini AI explanation and referral note
- Fallback response if Gemini API is unavailable

## Triage Levels

- Green: Home care / observe
- Orange: Visit doctor within 1–2 days
- Red: Emergency care now

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Gemini API
- Rule-based safety logic

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt