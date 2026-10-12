import streamlit as st

from supabase_client import create_supabase_client


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Health Copilot",
    page_icon="🩺",
    layout="wide",
)


# --------------------------------------------------
# 2. CUSTOM UI DESIGN
# --------------------------------------------------

st.markdown(
    """
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
    .stButton button {
        border-radius: 12px;
        min-height: 42px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# 3. SESSION INITIALIZATION
# --------------------------------------------------

defaults = {
    "sb_access_token": None,
    "sb_refresh_token": None,
    "sb_user_email": None,
    "sb_user_id": None,
    "extracted_text": "",
    "report_filename": None,
    "report_explanation": None,
    "report_text_review": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# 4. SUPABASE CONNECTION
# --------------------------------------------------

try:
    supabase = create_supabase_client(
        st.session_state["sb_access_token"],
        st.session_state["sb_refresh_token"],
    )
except Exception as exc:
    # Do not display credentials or secret values.
    st.error(
        "Supabase connection failed. Check the Streamlit secrets "
        "SUPABASE_URL and SUPABASE_KEY, and review app logs."
    )
    st.stop()


# --------------------------------------------------
# 5. AUTHENTICATION SCREEN
# --------------------------------------------------

if not st.session_state["sb_access_token"]:

    st.markdown(
        """
        <div class="hero">
            <h1>🩺 AI Health Copilot</h1>
            <p>Your personal medical information assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🔐 Welcome")
    st.write("Sign in or create an account to continue.")

    login_tab, signup_tab = st.tabs(["Sign In", "Create Account"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email address", key="login_email")
            password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )
            login_clicked = st.form_submit_button(
                "Sign In",
                use_container_width=True,
            )

        if login_clicked:
            if not email.strip() or not password:
                st.warning("Enter your email and password.")
            else:
                try:
                    result = supabase.auth.sign_in_with_password(
                        {
                            "email": email.strip(),
                            "password": password,
                        }
                    )

                    session = result.session
                    if session and result.user:
                        st.session_state["sb_access_token"] = (
                            session.access_token
                        )
                        st.session_state["sb_refresh_token"] = (
                            session.refresh_token
                        )
                        st.session_state["sb_user_email"] = (
                            result.user.email
                        )
                        st.session_state["sb_user_id"] = str(
                            result.user.id
                        )
                        st.rerun()
                    else:
                        st.error(
                            "No active session was returned. If email "
                            "confirmation is enabled, verify your email "
                            "before signing in."
                        )
                except Exception:
                    st.error(
                        "Sign-in failed. Check your email and password, "
                        "and confirm your email if required."
                    )

    with signup_tab:
        with st.form("signup_form"):
            new_email = st.text_input(
                "Email address",
                key="signup_email",
            )
            new_password = st.text_input(
                "Create password",
                type="password",
                key="signup_password",
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                key="confirm_password",
            )
            signup_clicked = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

        if signup_clicked:
            if not new_email.strip() or not new_password:
                st.warning("Enter an email and password.")
            elif new_password != confirm_password:
                st.warning("The passwords do not match.")
            elif len(new_password) < 8:
                st.warning("Use a password with at least 8 characters.")
            else:
                try:
                    result = supabase.auth.sign_up(
                        {
                            "email": new_email.strip(),
                            "password": new_password,
                        }
                    )

                    if result.session and result.user:
                        st.session_state["sb_access_token"] = (
                            result.session.access_token
                        )
                        st.session_state["sb_refresh_token"] = (
                            result.session.refresh_token
                        )
                        st.session_state["sb_user_email"] = (
                            result.user.email
                        )
                        st.session_state["sb_user_id"] = str(
                            result.user.id
                        )
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.success(
                            "Signup request accepted. Check your email "
                            "for the confirmation link, then sign in."
                        )
                except Exception as exc:
                    # Temporary diagnostic: exception text can contain
                    # provider details, so never print tokens or secrets.
                    safe_message = str(exc).replace("\n", " ")[:300]
                    st.error(
                        f"Signup error ({type(exc).__name__}): "
                        f"{safe_message}"
                    )

    st.info(
        "Your medical information is sensitive. "
        "Use fictional reports while testing this prototype."
    )
    st.stop()


# --------------------------------------------------
# 6. AUTHENTICATED USER
# --------------------------------------------------

st.sidebar.markdown("## 🩺 AI Health Copilot")
st.sidebar.markdown("---")
st.sidebar.markdown("🏠 Home")
st.sidebar.markdown("📄 Upload Report")
st.sidebar.markdown("📁 My Reports")
st.sidebar.markdown("📊 Health Insights")
st.sidebar.markdown("📚 Medical Terms")
st.sidebar.markdown("---")
st.sidebar.caption(
    "Signed in as: " + str(st.session_state["sb_user_email"])
)

if st.sidebar.button("Sign Out"):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    for key, value in defaults.items():
        st.session_state[key] = value

    st.rerun()


# --------------------------------------------------
# 7. MAIN DASHBOARD
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>AI Health Copilot 🩺</h1>
        <p>Your personal medical information assistant</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3>📄 Upload Reports</h3>
            <p>Upload medical reports in PDF or image format.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3>🧠 AI Analysis</h3>
            <p>Get easy-to-understand medical explanations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3>💙 Health Insights</h3>
            <p>Organize findings and understand key terms.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# 8. REPORT UPLOAD
# --------------------------------------------------

st.markdown("## 📤 Upload a Medical Report")
st.write("Choose a report to extract and review its text.")

uploaded_file = st.file_uploader(
    "Choose a PDF or image",
    type=["pdf", "png", "jpg", "jpeg"],
    key="medical_report_upload",
)

if uploaded_file:
    current_filename = uploaded_file.name

    if st.session_state["report_filename"] != current_filename:
        st.session_state["extracted_text"] = ""
        st.session_state["report_explanation"] = None
        st.session_state["report_text_review"] = ""
        st.session_state["report_filename"] = current_filename

    st.success(f"Report selected: {current_filename}")

    if st.button("🔍 Extract Report Text"):
        with st.spinner("Reading your report..."):
            try:
                from report_reader import extract_report_text

                extracted = extract_report_text(uploaded_file)

                if extracted.strip():
                    st.session_state["extracted_text"] = extracted
                    st.session_state["report_text_review"] = extracted
                    st.session_state["report_explanation"] = None
                    st.success("Text extraction completed!")
                else:
                    st.warning(
                        "No text was extracted. Try a clearer file."
                    )
            except Exception:
                st.error(
                    "Could not read this report. Check the file format "
                    "and OCR system dependencies in the app logs."
                )

    if st.session_state["extracted_text"]:
        st.markdown("### 📄 Extracted Report Text")

        st.text_area(
            "Review and correct the extracted text",
            height=250,
            key="report_text_review",
        )

        st.caption(
            "Verify medical values and units against the original report."
        )

        if st.button("🧠 Explain My Report"):
            corrected_text = st.session_state["report_text_review"]

            if not corrected_text.strip():
                st.warning("There is no report text to explain.")
            else:
                try:
                    from ai_explainer import explain_medical_report

                    with st.spinner("Preparing your explanation..."):
                        explanation = explain_medical_report(corrected_text)

                    st.session_state["report_explanation"] = explanation
                except Exception:
                    st.error(
                        "AI explanation failed. Check the OpenRouter "
                        "secret, model availability, and app logs."
                    )

        explanation = st.session_state["report_explanation"]
        if explanation:
            st.markdown("### 💙 Your Report Explained")
            st.markdown(explanation)
            st.info(
                "This explanation is informational, not a diagnosis. "
                "Discuss medical findings with a qualified clinician."
            )


# --------------------------------------------------
# 9. PRIVACY NOTICE
# --------------------------------------------------

st.markdown("---")
st.caption(
    "Privacy first: this prototype does not yet save uploaded reports "
    "to Supabase. Use fictional sample reports during testing. "
    "AI explanations can be incorrect and must be verified."
)
