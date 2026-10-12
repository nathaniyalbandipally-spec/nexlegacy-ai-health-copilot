
import requests
import streamlit as st


def explain_medical_report(report_text):
    """Explain extracted medical report text in simple language."""

    api_key = st.secrets["OPENROUTER_API_KEY"]

    prompt = f"""
You are a careful medical information assistant.

Explain the following extracted medical report in simple,
easy-to-understand language.

Include:
1. A short summary of what the report contains.
2. Important values and their stated reference ranges,
   when available.
3. Medical terms explained in simple language.
4. Questions the patient could ask their clinician.
5. Any uncertainty caused by missing or unclear text.

Rules:
- Do not diagnose diseases or prescribe medicines.
- Do not invent values or reference ranges.
- Do not treat OCR text as unquestionably accurate.
- Explain that reference ranges can vary by laboratory.
- Recommend urgent professional help when the report
  explicitly indicates a critical result, without guessing.
- Protect patient privacy.

Extracted report text:
{report_text[:12000]}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        },
        timeout=90
    )

    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]
