
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
    st.success(f"File received: {uploaded_file.name}")

    if uploaded_file.type.startswith("image/"):
        st.image(
            uploaded_file,
            caption="Uploaded medical report",
            use_container_width=True
        )
    else:
        st.info("Your PDF is ready for text extraction.")

    st.warning(
        "Text extraction and AI analysis will be added next."
    )

st.markdown("---")
st.markdown("### 📋 Example Reports You Can Upload")

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown("**🩸 Blood Test**")
    st.caption("CBC, lipid profile, etc.")

with r2:
    st.markdown("**🩻 Diagnostics**")
    st.caption("X-ray and scan reports")

with r3:
    st.markdown("**💊 Prescriptions**")
    st.caption("Doctor-prescribed medicines")

with r4:
    st.markdown("**🏥 Discharge Summary**")
    st.caption("Hospital records")

st.caption(
    "Privacy first: use sample reports for demos. "
    "This tool is for informational purposes, "
    "not a substitute for professional medical advice."
)
