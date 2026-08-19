import streamlit as st

from src.chatbot import generate_basic_response
from src.risk_engine import analyze_risk
from src.image_analyzer import validate_image
from src.vision_analyzer import analyze_image_awareness


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 40px 20px;
        text-align: center;
        border-radius: 20px;
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 20px;
        color: #555;
    }

    .feature-card {
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        min-height: 190px;
        background-color: white;
    }

    .section-title {
        font-size: 30px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    .disclaimer {
        padding: 15px;
        border-radius: 12px;
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        margin-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


# ==========================================================
# HEADER
# ==========================================================

header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("## 🩺 HealthGuard AI")

with header_col2:
    language = st.selectbox(
        "Language",
        ["English", "தமிழ்"]
    )


# ==========================================================
# HOME PAGE
# ==========================================================

if st.session_state.page == "home":

    st.markdown(
        """
        <div class="hero">

        <h1>Understand your health.<br>
        Make informed decisions.</h1>

        <p>
        AI-powered public health awareness with trusted
        information, risk-aware guidance and visual health awareness.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">How can we help?</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ------------------------------------------------------
    # CHAT CARD
    # ------------------------------------------------------

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            <h2>💬</h2>

            <h3>Ask HealthGuard AI</h3>

            <p>
            Ask questions about diseases, symptoms,
            prevention and public health.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "💬 Start Health Chat",
            use_container_width=True
        ):

            st.session_state.page = "chat"
            st.rerun()

    # ------------------------------------------------------
    # IMAGE CARD
    # ------------------------------------------------------

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            <h2>📷</h2>

            <h3>Visual Health Awareness</h3>

            <p>
            Upload an image of a visible symptom for
            educational health-awareness analysis.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "📷 Analyze Image",
            use_container_width=True
        ):

            st.session_state.page = "image"
            st.rerun()

    # ------------------------------------------------------
    # RISK LEVELS
    # ------------------------------------------------------

    st.markdown(
        '<div class="section-title">🚦 Risk-Aware Guidance</div>',
        unsafe_allow_html=True
    )

    risk1, risk2, risk3 = st.columns(3)

    with risk1:

        st.success(
            """
            🟢 **GENERAL AWARENESS**

            Information and basic health awareness.
            """
        )

    with risk2:

        st.warning(
            """
            🟡 **CAUTION**

            Monitor symptoms and consider professional advice.
            """
        )

    with risk3:

        st.error(
            """
            🔴 **URGENT ATTENTION**

            Warning signs may require prompt medical evaluation.
            """
        )

    # ------------------------------------------------------
    # TRUST SECTION
    # ------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🛡️ Built for Responsible Health Awareness'
        '</div>',
        unsafe_allow_html=True
    )

    trust1, trust2, trust3 = st.columns(3)

    with trust1:

        st.markdown(
            """
            ### 📚 Trusted Information

            Responses are grounded in a curated
            public-health knowledge base.
            """
        )

    with trust2:

        st.markdown(
            """
            ### 💡 Explainable Guidance

            The system explains why a particular
            guidance level was provided.
            """
        )

    with trust3:

        st.markdown(
            """
            ### 🔒 Safety First

            The system provides awareness information,
            not medical diagnosis.
            """
        )


# ==========================================================
# CHAT PAGE
# ==========================================================

elif st.session_state.page == "chat":

    st.title("💬 HealthGuard AI Assistant")

    st.write(
        "Ask a health-awareness question or describe your symptoms."
    )

    # ------------------------------------------------------
    # BACK BUTTON
    # ------------------------------------------------------

    if st.button(
        "← Back to Home",
        key="back_home"
    ):

        st.session_state.page = "home"
        st.rerun()

    # ------------------------------------------------------
    # QUESTION INPUT
    # ------------------------------------------------------

    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: What are the symptoms of dengue?"
        ),
        height=130
    )

    # ------------------------------------------------------
    # GET GUIDANCE
    # ------------------------------------------------------

    if st.button(
        "🔍 Get Health Guidance",
        use_container_width=True
    ):

        if question.strip():

            # --------------------------------------------------
            # HEALTH INFORMATION
            # --------------------------------------------------

            response = generate_basic_response(question)

            # --------------------------------------------------
            # RISK ANALYSIS
            # --------------------------------------------------

            risk = analyze_risk(question)

            st.markdown("---")

            # --------------------------------------------------
            # RISK RESULT
            # --------------------------------------------------

            if risk["level"] == "URGENT ATTENTION":

                st.error(
                    "🔴 **URGENT ATTENTION**\n\n"
                    + risk["message"]
                )

            else:

                st.success(
                    "🟢 **GENERAL AWARENESS**\n\n"
                    + risk["message"]
                )

            # --------------------------------------------------
            # WARNING SIGNS FROM RISK ENGINE
            # --------------------------------------------------

            if risk.get("warning_signs"):

                st.warning(
                    "⚠️ **Warning Signs Detected**"
                )

                for warning in risk["warning_signs"]:

                    st.write(
                        "•",
                        warning
                    )

            # --------------------------------------------------
            # HEALTH INFORMATION
            # --------------------------------------------------

            st.subheader(
                "🩺 Health Awareness Information"
            )

            if response.get("results"):

                # Show interpretation
                st.info(
                    response["message"]
                )

                intent = response.get(
                    "intent",
                    "general"
                )

                # ==================================================
                # SYMPTOMS
                # ==================================================

                if intent == "symptoms":

                    for information in response["results"]:

                        st.markdown(
                            f"### 🔍 {information['name']}"
                        )

                        st.markdown(
                            "**Common symptoms:**"
                        )

                        for symptom in information["symptoms"]:

                            st.write(
                                "•",
                                symptom
                            )

                        st.markdown(
                            "**Trusted sources:**"
                        )

                        for source in information["sources"]:

                            st.write(
                                "📚",
                                source
                            )

                # ==================================================
                # PREVENTION
                # ==================================================

                elif intent == "prevention":

                    for information in response["results"]:

                        st.markdown(
                            f"### 🛡️ "
                            f"{information['name']} Prevention"
                        )

                        for prevention in information["prevention"]:

                            st.write(
                                "•",
                                prevention
                            )

                        st.markdown(
                            "**Trusted sources:**"
                        )

                        for source in information["sources"]:

                            st.write(
                                "📚",
                                source
                            )

                # ==================================================
                # WARNING SIGNS
                # ==================================================

                elif intent == "warning":

                    for information in response["results"]:

                        st.markdown(
                            f"### ⚠️ "
                            f"{information['name']} Warning Signs"
                        )

                        for warning in information["warning_signs"]:

                            st.write(
                                "•",
                                warning
                            )

                        st.markdown(
                            "**Trusted sources:**"
                        )

                        for source in information["sources"]:

                            st.write(
                                "📚",
                                source
                            )

                # ==================================================
                # DESCRIPTION / GENERAL
                # ==================================================

                else:

                    for information in response["results"]:

                        st.markdown(
                            f"### 📚 {information['name']}"
                        )

                        st.write(
                            information["description"]
                        )

                        st.markdown(
                            "**Common symptoms:**"
                        )

                        for symptom in information["symptoms"]:

                            st.write(
                                "•",
                                symptom
                            )

                        st.markdown(
                            "**Prevention:**"
                        )

                        for prevention in information["prevention"]:

                            st.write(
                                "•",
                                prevention
                            )

                        st.markdown(
                            "**Warning signs:**"
                        )

                        for warning in information["warning_signs"]:

                            st.write(
                                "•",
                                warning
                            )

                        st.markdown(
                            "**Trusted sources:**"
                        )

                        for source in information["sources"]:

                            st.write(
                                "📚",
                                source
                            )

            else:

                st.info(
                    response["message"]
                )

            # --------------------------------------------------
            # SAFETY MESSAGE
            # --------------------------------------------------

            st.info(
                "⚠️ This information is for health awareness only "
                "and does not confirm a diagnosis."
            )

        else:

            st.warning(
                "Please enter a health-related question."
            )


# ==========================================================
# IMAGE PAGE
# ==========================================================

elif st.session_state.page == "image":

    st.title("📷 Visual Health Awareness")

    st.write(
        "Upload a clear image of a visible symptom "
        "for educational analysis."
    )

    # ------------------------------------------------------
    # BACK BUTTON
    # ------------------------------------------------------

    if st.button(
        "← Back to Home",
        key="back_home_image"
    ):

        st.session_state.page = "home"
        st.rerun()

    # ------------------------------------------------------
    # IMAGE UPLOAD
    # ------------------------------------------------------

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        # --------------------------------------------------
        # VALIDATE IMAGE
        # --------------------------------------------------

        validation = validate_image(
            uploaded_image
        )

        if validation["valid"]:

            # ------------------------------------------------
            # IMAGE PREVIEW
            # ------------------------------------------------

            st.image(
                uploaded_image,
                caption="Uploaded image",
                use_container_width=True
            )

            st.success(
                f"✅ Image accepted "
                f"({validation['width']} × "
                f"{validation['height']} pixels)"
            )

            st.markdown(
                "### 🔍 Visual Analysis"
            )

            st.info(
                "The image is ready for "
                "visual health-awareness analysis."
            )

            # ------------------------------------------------
            # ANALYZE BUTTON
            # ------------------------------------------------

            if st.button(
                "🔍 Analyze Image",
                use_container_width=True
            ):

                result = analyze_image_awareness(
                    uploaded_image
                )

                st.markdown("---")

                st.subheader(
                    "🧠 AI Visual Health Awareness"
                )

                # ------------------------------------------------
                # OBSERVATION
                # ------------------------------------------------

                st.info(
                    result.get(
                        "observation",
                        "No visual observation was returned."
                    )
                )

                # ------------------------------------------------
                # CATEGORY
                # ------------------------------------------------

                st.markdown(
                    f"**Possible category:** "
                    f"{result.get('possible_category', 'Unavailable')}"
                )

                # ------------------------------------------------
                # CONFIDENCE
                # ------------------------------------------------

                st.markdown(
                    f"**Confidence:** "
                    f"{result.get('confidence', 'Low')}"
                )

                # ------------------------------------------------
                # GUIDANCE
                # ------------------------------------------------

                st.markdown(
                    "### 💡 Guidance"
                )

                st.write(
                    result.get(
                        "guidance",
                        "No guidance available."
                    )
                )

                # ------------------------------------------------
                # RECOMMENDATION
                # ------------------------------------------------

                st.markdown(
                    "### 🩺 What you can do"
                )

                st.write(
                    result.get(
                        "recommendation",
                        "Please consider consulting a qualified healthcare professional if you are concerned."
                    )
                )

                # ------------------------------------------------
                # DISCLAIMER
                # ------------------------------------------------

                st.warning(
                    "⚠️ "
                    + result.get(
                        "disclaimer",
                        "This image analysis is for health awareness only and cannot provide a medical diagnosis."
                    )
                )

        else:

            st.error(
                f"❌ {validation['message']}"
            )