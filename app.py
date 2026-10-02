import re
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from modules.text_analyzer import analyze_text
from modules.url_analyzer import extract_url, analyze_url
from modules.risk_engine import final_assessment

st.set_page_config(
    page_title="TrustLens AI",
    page_icon="🛡️",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "messages.csv"

@st.cache_resource
def load_model():
    df = pd.read_csv(DATA_PATH)
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=3000,
        sublinear_tf=True
    )
    X = vectorizer.fit_transform(df["text"])
    model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    model.fit(X, df["label"])
    return vectorizer, model, df

vectorizer, model, training_df = load_model()

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Styling
# -------------------------
st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 18px; opacity: .75; margin-top: 0;}
.risk-card {padding: 20px; border-radius: 16px; border: 1px solid rgba(128,128,128,.25); margin-bottom: 16px;}
.small-note {font-size: 13px; opacity: .7;}
.signal {padding: 10px 12px; border-radius: 10px; margin: 6px 0; border: 1px solid rgba(128,128,128,.2);}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("🛡️ TrustLens AI")
page = st.sidebar.radio(
    "Navigate",
    ["Analyze", "Learn", "History", "About"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("Prototype for CODE SANGAM 2026")
st.sidebar.caption("Risk scores are estimates based on the prototype model and detected signals.")

# -------------------------
# Header
# -------------------------
st.markdown('<div class="main-title">🛡️ TRUSTLENS AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">See the threat. Understand the evidence. Decide safely.</div>', unsafe_allow_html=True)

# -------------------------
# Analyze page
# -------------------------
if page == "Analyze":
    st.markdown("### 🔍 Analyze suspicious digital content")
    st.write("Paste a message, email, payment request, social-media text, or URL.")

    examples = {
        "Bank phishing": "URGENT! Your bank account will be blocked today. Verify your KYC immediately at http://bank-verify.xyz/login",
        "Reward scam": "Congratulations! You won a ₹25,000 reward. Claim now by entering your account details.",
        "Legitimate message": "Your order has been shipped. Track it from the official shopping app."
    }

    selected = st.selectbox("Quick demo example", ["Custom input"] + list(examples.keys()))
    default_text = "" if selected == "Custom input" else examples[selected]

    text = st.text_area(
        "Content",
        value=default_text,
        height=170,
        placeholder="Example: Your account will be blocked. Verify immediately..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 ANALYZE", type="primary", use_container_width=True)

    if analyze_button:
        if not text.strip():
            st.warning("Please enter some content to analyze.")
        else:
            X = vectorizer.transform([text])
            probability = float(model.predict_proba(X)[0][1])

            text_result = analyze_text(text)
            url = extract_url(text)
            url_result = analyze_url(url)

            result = final_assessment(
                probability,
                text_result["score"],
                url_result["score"],
                text_result["signals"],
                url_result["signals"]
            )

            st.session_state.history.insert(0, {
                "score": result["score"],
                "level": result["level"],
                "threat": result["threat"],
                "preview": text[:90].replace("\n", " ")
            })
            st.session_state.history = st.session_state.history[:20]

            st.markdown("---")
            a, b, c = st.columns(3)
            a.metric("Risk Score", f'{result["score"]}/100')
            b.metric("Risk Level", result["level"])
            c.metric("Threat Type", result["threat"])

            st.progress(result["score"] / 100)

            st.markdown(f"## {result['emoji']} {result['level']} RISK")
            st.markdown(f"### Detected category: **{result['threat']}**")

            left, right = st.columns(2)

            with left:
                st.markdown("### 🔍 Why did we flag it?")
                if result["signals"]:
                    for level, message in result["signals"]:
                        icon = {"high": "🔴", "medium": "🟠", "low": "🟡", "info": "🔵"}.get(level, "•")
                        st.markdown(
                            f'<div class="signal">{icon} <b>{message}</b></div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No strong warning signal was detected.")

                if url_result["found"]:
                    st.caption(url_result["details"])

            with right:
                st.markdown("### 🛡️ What should I do?")
                for i, rec in enumerate(result["recommendation"], 1):
                    st.write(f"**{i}.** {rec}")

                st.markdown("### 🧠 What should I learn?")
                st.info(
                    "A warning is based on signals, not certainty. "
                    "Urgency, unexpected payment requests, credential requests, "
                    "and mismatched or suspicious links are useful reasons to pause "
                    "and verify independently."
                )

            with st.expander("Technical details"):
                st.write(f"ML phishing probability: **{probability:.2%}**")
                st.write(f"Text signal score: **{text_result['score']}/70**")
                st.write(f"URL signal score: **{url_result['score']}/50**")
                st.caption(
                    "Prototype note: the score is an experimental combination of a small "
                    "training dataset, NLP probability and transparent heuristic signals. "
                    "It is not a guarantee of safety or maliciousness."
                )

    st.markdown("---")
    st.markdown("### 💡 Demo flow")
    st.write("1. Paste suspicious content → 2. Analyze → 3. Show risk → 4. Open 'Why did we flag it?' → 5. Show safer action.")

# -------------------------
# Learn
# -------------------------
elif page == "Learn":
    st.markdown("## 🧠 Learn to recognize digital threats")

    tabs = st.tabs(["Phishing", "Urgency", "Credentials", "Payments", "Suspicious URLs"])

    with tabs[0]:
        st.subheader("Phishing")
        st.write("Phishing attempts try to make a user visit a fake page or reveal sensitive information.")
        st.write("Look for unexpected requests, impersonation, unusual links, and pressure to act.")

    with tabs[1]:
        st.subheader("Urgency")
        st.write('Examples: "Act immediately", "Your account will close today", "Final notice".')
        st.write("Urgency is a signal to slow down and verify rather than proof of a scam by itself.")

    with tabs[2]:
        st.subheader("Credential requests")
        st.write("Be especially cautious with unsolicited requests for passwords, PINs, CVV numbers or OTPs.")
        st.write("Never share authentication secrets because a message tells you to.")

    with tabs[3]:
        st.subheader("Payment requests")
        st.write("Unexpected fees, transfers, refunds or investment requests deserve independent verification.")

    with tabs[4]:
        st.subheader("Suspicious URLs")
        st.write("Check the domain carefully. HTTPS alone does not prove that a website is legitimate.")
        st.write("An unfamiliar domain, unusual subdomains, IP-based URLs or misleading paths can be warning signals.")

    st.markdown("---")
    st.success("TrustLens principle: Don't blindly trust a warning. Understand the evidence and verify independently.")

# -------------------------
# History
# -------------------------
elif page == "History":
    st.markdown("## 📊 Analysis History")
    if not st.session_state.history:
        st.info("No analyses yet. Go to Analyze and test a few examples.")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True, hide_index=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(df))
        c2.metric("High/Critical", int(df["level"].isin(["HIGH", "CRITICAL"]).sum()))
        c3.metric("Low", int((df["level"] == "LOW").sum()))

# -------------------------
# About
# -------------------------
else:
    st.markdown("## ℹ️ About TrustLens AI")
    st.write(
        "TrustLens AI is a hackathon prototype for explaining suspicious digital content. "
        "It combines a small NLP classifier with transparent text and URL signals."
    )

    st.markdown("### Architecture")
    st.code("""
User Input
    ↓
Input Processing
    ↓
NLP Model + URL Analyzer
    ↓
Transparent Risk Engine
    ↓
Evidence + Risk Level
    ↓
Safer Next Action
""")

    st.markdown("### Privacy")
    st.write(
        "The prototype does not require names, phone numbers, contacts or account credentials. "
        "Analysis history is kept only in the current Streamlit session."
    )

    st.markdown("### Important limitation")
    st.warning(
        "This is a hackathon prototype, not a production cybersecurity product. "
        "The small demo dataset and heuristic rules cannot detect every threat. "
        "Users should independently verify important requests."
    )
