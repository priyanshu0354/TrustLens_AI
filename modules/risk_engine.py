def final_assessment(model_probability, text_score, url_score, text_signals, url_signals):
    # Prototype weighting. It is intentionally transparent for a hackathon demo.
    ml_score = model_probability * 35.0
    raw = ml_score + (text_score * 0.45) + (url_score * 0.55)
    score = int(max(0, min(100, round(raw))))

    all_signals = []
    all_signals.extend(text_signals)
    all_signals.extend(url_signals)

    # Remove duplicate messages while preserving order.
    seen = set()
    unique = []
    for level, msg in all_signals:
        if msg not in seen:
            unique.append((level, msg))
            seen.add(msg)

    if score >= 81:
        level = "CRITICAL"
        emoji = "🚨"
    elif score >= 61:
        level = "HIGH"
        emoji = "⚠️"
    elif score >= 31:
        level = "MEDIUM"
        emoji = "🟠"
    else:
        level = "LOW"
        emoji = "🟢"

    # Explain uncertainty instead of claiming certainty.
    if not unique:
        unique = [("info", "No strong warning signal was detected. This does not prove the content is safe.")]

    if "credential" in [x.lower() for x in []]:
        threat = "Credential Theft"
    else:
        joined = " ".join(m.lower() for _, m in unique)
        if "payment" in joined or "financial" in joined:
            threat = "Payment / Financial Scam"
        elif "reward" in joined or "prize" in joined:
            threat = "Reward / Lottery Scam"
        elif "credential" in joined or "password" in joined or "otp" in joined:
            threat = "Phishing / Credential Theft"
        elif "url" in joined or "domain" in joined:
            threat = "Suspicious Link"
        else:
            threat = "Potential Digital Threat"

    if score <= 30:
        recommendation = [
            "No strong warning signal was detected.",
            "Still verify unexpected requests through an official source.",
            "Never share passwords, PINs or OTPs in response to unsolicited messages."
        ]
    elif score <= 60:
        recommendation = [
            "Pause before clicking or paying.",
            "Verify the request independently using the organization's official app or website.",
            "Do not share passwords, PINs or OTPs."
        ]
    else:
        recommendation = [
            "Do not click the link or follow the requested action yet.",
            "Do not share passwords, PINs, OTPs or payment details.",
            "Verify independently through the organization's official app, website or known contact channel.",
            "If appropriate, report the suspicious content to the relevant service."
        ]

    return {
        "score": score,
        "level": level,
        "emoji": emoji,
        "threat": threat,
        "signals": unique,
        "recommendation": recommendation
    }
