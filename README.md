# 🛡️ TrustLens AI

**See the threat. Understand the evidence. Decide safely.**

Hackathon MVP for CODE SANGAM 2026 — PS-06: Understanding Digital Threats.

## What it does

TrustLens analyzes suspicious messages and URLs and returns:

- estimated risk score
- risk level
- threat category
- explainable warning signals
- safer next actions
- educational guidance
- current-session analysis history

## Tech stack

- Python
- Streamlit
- scikit-learn
- TF-IDF + Logistic Regression
- Transparent URL/text heuristics
- Pandas

## Run locally

### Windows

```bash
cd TrustLens_AI
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit, usually:

`http://localhost:8501`

## Demo cases

### High risk

```text
URGENT! Your bank account will be blocked today. Verify your KYC immediately at http://bank-verify.xyz/login
```

### Reward scam

```text
Congratulations! You won a ₹25,000 reward. Claim now by entering your account details.
```

### Legitimate

```text
Your order has been shipped. Track it from the official shopping app.
```

## Important

This is a hackathon prototype. The model is trained on a small demonstration dataset. The risk score is an estimate and does not prove that content is safe or malicious.

## Architecture

User Input
→ NLP Model + URL Analyzer
→ Risk Engine
→ Evidence
→ Recommendation

## Presentation hook

> "TrustLens doesn't ask users to blindly trust another AI. It teaches them why the content looks suspicious, so they can make the next decision themselves."
