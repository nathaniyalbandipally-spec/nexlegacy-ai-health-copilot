import streamlit as st

from supabase_client import create_supabase_client


# ------------------------------------------------------------
# AI HEALTH COPILOT - PROTOTYPE
# Guest access works without Supabase. Auth requires Supabase.
# Uploaded reports are processed in memory and are NOT saved.
# ------------------------------------------------------------

st.set_page_config(
    page_title="AI Health Copilot",
    page_icon="🩺",
    layout="wide",
)

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
        padding: 24px;
        border-radius: 20px;
        background: linear-gradient(120deg, #dceeff, #f5f9ff);
        border: 1px solid #d5e7ff;
        margin-bottom: 20px;
    }
    .hero h1 {
        color: #123365;
        font-size: 2.25rem;
    }
    .hero p {
        color: #526b8e;
        font-size: 1.05rem;
    }
    .feature-card {
        background: white;
        border: 1px solid #e2eaf5;
        padding: 18px;
        border-radius: 16px;
        min-height: 125px;
        margin-bottom: 12px;
    }
    .feature-card h3 {
        color: #173765;
        font-size: 1.05rem;
    }
    .feature-card p {
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


# ----------------------- SESSION STATE -----------------------

DEFAULTS = {
    "sb_access_token": None,
    "sb_refresh_token": None,
    "sb_user_email": None,
    "sb_user_id": None,
    "guest_mode": False,
    "extracted_text": "",
    "report_filename": None,
    "report_explanation": None,
    "report_text_review": "",
}

for state_key, default_value in DEFAULTS.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value


def clear_user_session():
    """Clear login and temporary report data."""
    for state_key, default_value in DEFAULTS.items():
        st.session_state[state_key] = default_value


# ----------------------- SUPABASE CLIENT -----------------------

supabase = None
supabase_error = None

# Guest mode deliberately does not contact Supabase.
if not st.session_state["guest_mode"]:
    try:
        supabase = create_supabase_client(
            st.session_state["sb_access_token"],
            st.session_state["sb_refresh_token"],
        )
    except Exception as exc:
        # Keep secrets and full provider responses out of the UI.
        supabase_error = type(exc).__name__


# ----------------------- SIGN IN / SIGN UP -----------------------

is_authenticated = bool(st.session_state["sb_access_token"])
is_guest = bool(st.session_state["guest_mode"])

if not is_authenticated and not is_guest:
    st.markdown(
        """
        <div class="hero">
            <h1>🩺 AI Health Copilot</h1>
            <p>Your personal medical information assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("Welcome")
    st.write("Sign in, create an account, or explore the prototype as a guest.")

    if supabase is None:
        st.warning(
            "Supabase cannot currently be reached. Guest Mode remains "
            "available below; sign-in and account creation need a working "
            "Supabase connection."
        )

    sign_in_tab, create_account_tab = st.tabs(
        ["Sign In", "Create Account"]
    )

    with sign_in_tab:
        with st.form("login_form"):
            login_email = st.text_input("Email address", key="login_email")
            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )
            login_submitted = st.form_submit_button(
                "Sign In",
                use_container_width=True,
            )

        if login_submitted:
            if supabase is None:
                st.error(
                    "Sign-in is unavailable while Supabase cannot be reached. "
                    "Please use Guest Mode for now."
                )
            elif not login_email.strip() or not login_password:
                st.warning("Enter your email address and password.")
            else:
                try:
                    auth_result = supabase.auth.sign_in_with_password(
                        {
                            "email": login_email.strip(),
                            "password": login_password,
                        }
                    )
                    auth_session = auth_result.session
                    auth_user = auth_result.user

                    if auth_session and auth_user:
                        st.session_state["sb_access_token"] = (
                            auth_session.access_token
                        )
                        st.session_state["sb_refresh_token"] = (
                            auth_session.refresh_token
                        )
                        st.session_state["sb_user_email"] = auth_user.email
                        st.session_state["sb_user_id"] = str(auth_user.id)
                        st.rerun()
                    else:
                        st.error(
                            "No session was returned. If email confirmation "
                            "is enabled, verify your email before signing in."
                        )
                except Exception:
                    st.error(
                        "Sign-in failed. Check your credentials and email "
                        "verification status, then try again."
                    )

    with create_account_tab:
        with st.form("signup_form"):
            signup_email = st.text_input(
                "Email address",
                key="signup_email",
            )
            signup_password = st.text_input(
                "Create password",
                type="password",
                key="signup_password",
            )
            signup_password_confirm = st.text_input(
                "Confirm password",
                type="password",
                key="signup_password_confirm",
            )
            signup_submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True,
            )

        if signup_submitted:
            if supabase is None:
                st.error(
                    "Account creation needs Supabase, which is currently "
                    "unreachable. You can continue in Guest Mode."
                )
            elif not signup_email.strip() or not signup_password:
                st.warning("Enter your email address and password.")
            elif signup_password != signup_password_confirm:
                st.warning("The passwords do not match.")
            elif len(signup_password) < 8:
                st.warning("Use a password with at least 8 characters.")
            else:
                try:
                    signup_result = supabase.auth.sign_up(
                        {
                            "email": signup_email.strip(),
                            "password": signup_password,
                        }
                    )

                    if signup_result.session and signup_result.user:
                        st.session_state["sb_access_token"] = (
                            signup_result.session.access_token
                        )
                        st.session_state["sb_refresh_token"] = (
                            signup_result.session.refresh_token
                        )
                        st.session_state["sb_user_email"] = (
                            signup_result.user.email
                        )
                        st.session_state["sb_user_id"] = str(
                            signup_result.user.id
                        )
                        st.success("Account created successfully.")
                        st.rerun()
                    else:
                        st.success(
                            "Signup request accepted. Check your email for "
                            "the confirmation link, then return to Sign In."
                        )
                except Exception:
                    st.error(
                        "Account creation failed. Check that the Supabase "
                        "URL and publishable key are correct, your connection "
                        "works, and email signup is enabled. Use Guest Mode "
                        "while troubleshooting."
                    )

    st.markdown("### Or try the app without an account")
    st.caption(
        "Guest Mode does not create a user account or save reports to "
        "Supabase. Temporary work may disappear when the session ends."
    )
    if st.button("Continue as Guest", use_container_width=True):
        st.session_state["guest_mode"] = True
        st.session_state["sb_access_token"] = None
        st.session_state["sb_refresh_token"] = None
        st.session_state["sb_user_email"] = "Guest"
        st.session_state["sb_user_id"] = None
        st.rerun()

    st.info(
        "Use fictional medical reports during testing. AI explanations are "
        "informational and may be inaccurate."
    )
    st.stop()


# ----------------------- SIDEBAR -----------------------

st.sidebar.markdown("## 🩺 AI Health Copilot")
st.sidebar.markdown("---")
st.sidebar.markdown("🏠 Home")
st.sidebar.markdown("📄 Upload Report")
st.sidebar.markdown("🧠 AI Explanation")
st.sidebar.markdown("---")

if is_guest:
    st.sidebar.info("Guest Mode")
    st.sidebar.caption("Reports are not saved.")
    if st.sidebar.button("Exit Guest Mode"):
        clear_user_session()
        st.rerun()
else:
    st.sidebar.caption(
        "Signed in as: " + str(st.session_state["sb_user_email"])
    )
    if st.sidebar.button("Sign Out"):
        try:
            if supabase is not None:
                supabase.auth.sign_out()
        except Exception:
            pass
        clear_user_session()
        st.rerun()


# ----------------------- DASHBOARD -----------------------

if is_guest:
    st.warning(
        "Guest Mode: do not upload real medical records. Files and text "
        "are not saved to Supabase, but the AI provider may receive the "
        "text you submit for explanation."
    )

st.markdown(
    """
    <div class="hero">
        <h1>AI Health Copilot 🩺</h1>
        <p>Understand medical reports in clearer, simpler language.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

feature_1, feature_2, feature_3 = st.columns(3)

with feature_1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📄 Report Upload</h3>
            <p>Choose a PDF or a clear report image.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature_2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🔎 Text Extraction</h3>
            <p>Extract report text for you to review and correct.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with feature_3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>💙 Simple Explanation</h3>
            <p>Ask AI to explain terms and values in plain language.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------- REPORT UPLOAD & EXTRACTION -----------------------

st.markdown("## Upload a Medical Report")
st.write("Supported formats: PDF, PNG, JPG, and JPEG.")

uploaded_report = st.file_uploader(
    "Choose a fictional sample report for testing",
    type=["pdf", "png", "jpg", "jpeg"],
    key="medical_report_upload",
)

if uploaded_report is not None:
    filename = uploaded_report.name

    if st.session_state["report_filename"] != filename:
        st.session_state["report_filename"] = filename
        st.session_state["extracted_text"] = ""
        st.session_state["report_text_review"] = ""
        st.session_state["report_explanation"] = None

    st.success(f"Selected file: {filename}")

    if st.button("Extract Report Text", use_container_width=True):
        try:
            from report_reader import extract_report_text

            with st.spinner("Extracting text..."):
                text_result = extract_report_text(uploaded_report)

            if text_result and text_result.strip():
                st.session_state["extracted_text"] = text_result
                st.session_state["report_text_review"] = text_result
                st.session_state["report_explanation"] = None
                st.success("Text extracted. Review it carefully below.")
            else:
                st.warning(
                    "No readable text was found. Try a sharper image or "
                    "a PDF with selectable text."
                )
        except Exception as exc:
            error_name = type(exc).__name__
            if error_name in {
                "TesseractNotFoundError",
                "PDFInfoNotInstalledError",
                "PDFPageCountError",
            }:
                st.error(
                    f"Report extraction dependency error: {error_name}. "
                    "The deployed OCR system tools may be missing."
                )
            elif error_name == "ModuleNotFoundError":
                st.error(
                    "A Python package required for extraction is missing. "
                    "Check requirements.txt and the app logs."
                )
            else:
                st.error(
                    f"Report extraction failed ({error_name}). "
                    "Check the app logs for technical details."
                )

    if st.session_state["extracted_text"]:
        st.markdown("### Review extracted text")
        st.text_area(
            "Correct any OCR mistakes before requesting an explanation",
            key="report_text_review",
            height=250,
        )
        st.caption(
            "OCR may misread medical values, decimal points, units, and names. "
            "Compare the text with the original document."
        )

        if st.button("Explain My Report", use_container_width=True):
            reviewed_text = st.session_state["report_text_review"].strip()

            if not reviewed_text:
                st.warning("There is no text to explain.")
            elif not st.secrets.get("OPENROUTER_API_KEY"):
                st.error(
                    "The OpenRouter API key is missing from Streamlit Secrets."
                )
            else:
                try:
                    from ai_explainer import explain_medical_report

                    with st.spinner("Preparing a plain-language explanation..."):
                        ai_result = explain_medical_report(reviewed_text)

                    st.session_state["report_explanation"] = ai_result
                except Exception as exc:
                    st.error(
                        "AI explanation failed. Check the OpenRouter secret, "
                        "internet connection, model availability, and app logs. "
                        f"Error type: {type(exc).__name__}."
                    )

        if st.session_state["report_explanation"]:
            st.markdown("### Your Report Explained")
            st.markdown(st.session_state["report_explanation"])
            st.info(
                "This is general information, not a diagnosis or treatment "
                "recommendation. Confirm findings with a qualified clinician."
            )


# ----------------------- PRIVACY NOTICE -----------------------

st.markdown("---")
st.caption(
    "Prototype notice: uploaded reports are not saved to Supabase by this "
    "app. If you request an AI explanation, the reviewed text is sent to "
    "the configured AI provider. Use fictional data while testing."
)
