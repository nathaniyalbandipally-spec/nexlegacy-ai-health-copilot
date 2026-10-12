
import streamlit as st

st.set_page_config(
    page_title="AI Health Copilot",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f7ff, #ffffff);
}
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
[data-testid="stSidebar"] {
    background: #eaf3ff;
}
.hero {
    padding: 25px;
    border-radius: 22px;
    background: linear-gradient(120deg, #dceeff, #f5f9ff);
    border: 1px solid #d5e7ff;
    margin-bottom: 22px;
}
.hero h1 {
    color: #123365;
    font-size: 2.4rem;
}
.hero p {
    color: #526b8e;
    font-size: 1.1rem;
}
.card {
    background: white;
    border: 1px solid #e2eaf5;
    padding: 20px;
    border-radius: 18px;
    min-height: 130px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(25, 70, 120, .05);
}
.card h3 {
    color: #173765;
    font-size: 1.1rem;
}
.card p {
    color: #64748b;
}
.upload-box {
    background: white;
    border: 2px dashed #82b5ff;
    border-radius: 22px;
    padding: 25px;
}
.stButton button {
    border-radius: 12px;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🩺 AI Health Copilot")
    st.markdown("---")
    st.markdown("### 🏠 Home")
    st.markdown("📄 Upload Report")
    st.markdown("📁 My Reports")
    st.markdown("📊 Health Insights")
    st.markdown("📚 Medical Terms")
    st.markdown("---")
    st.info(
        "Understand and organize your "
        "medical information. This app "
        "does not diagnose diseases."
    )

st.markdown("""
<div class="hero">
    <h1>AI Health Copilot 🩺</h1>
    <p>Your personal medical information assistant</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <h3>📄 Upload Reports</h3>
        <p>Upload medical reports in PDF or image format.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <h3>🧠 AI Analysis</h3>
        <p>Get easy-to-understand medical explanations.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <h3>💙 Health Insights</h3>
        <p>Organize findings and understand key terms.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("## 📤 Upload a Medical Report")
st.markdown(
    "Choose a report below to begin exploring your health information."
)

uploaded_file = st.file_uploader(
    "Choose a PDF or image",
    type=["pdf", "png", "jpg", "jpeg"]
)



if uploaded_file:
    st.success(f"Report uploaded: {uploaded_file.name}")

    if st.button("🔍 Extract Report Text"):
        with st.spinner("Reading your report..."):
            try:
                from report_reader import extract_report_text

                text = extract_report_text(uploaded_file)

                if text:
                    st.session_state["extracted_text"] = text
                    st.session_state["report_filename"] = uploaded_file.name
                    st.success("Text extracted successfully!")
                else:
                    st.warning(
                        "No text found. Try a clearer report."
                    )

            except Exception:
                st.error(
                    "Could not read this file. Check the file "
                    "format and OCR dependencies."
                )

    extracted_text = st.session_state.get("extracted_text", "")

    if extracted_text:
        st.markdown("### 📄 Extracted Report Text")

        st.text_area(
            "Review and correct the extracted text",
            value=extracted_text,
            height=250,
            key="report_text_review"
        )

        st.caption(
            "Verify names, dates, values, and units against "
            "the original report before requesting an explanation."
        )

        if st.button("🧠 Explain My Report"):
            try:
                from ai_explainer import explain_medical_report

                corrected_text = st.session_state["report_text_review"]

                if not corrected_text.strip():
                    st.warning("Please provide report text first.")
                else:
                    with st.spinner("Preparing your explanation..."):
                        explanation = explain_medical_report(
                            corrected_text
                        )

                    st.session_state["report_explanation"] = explanation

            except Exception:
                st.error(
                    "The explanation could not be generated. "
                    "Check your API key, internet connection, "
                    "and AI provider availability."
                )

        if st.session_state.get("report_explanation"):
            st.markdown("### 💙 Your Report Explained")
            st.markdown(st.session_state["report_explanation"])

            st.info(
                "This is informational assistance, not a diagnosis. "
                "Confirm medical findings with a qualified clinician."
            )
