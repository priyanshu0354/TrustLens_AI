import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = {
    "verify", "verification", "login", "secure", "account", "update",
    "claim", "reward", "bonus", "payment", "kyc", "confirm", "unlock",
    "wallet", "refund", "otp", "password", "signin"
}
SUSPICIOUS_TLDS = {".xyz", ".top", ".click", ".work", ".zip", ".buzz", ".tk"}

def extract_url(text: str):
    if not text:
        return None
    m = re.search(r"https?://[^\s<>()]+", text)
    if not m:
        return None
    return m.group(0).rstrip(".,!?;:'\")")

def analyze_url(url: str):
    if not url:
        return {
            "found": False, "score": 0, "signals": [],
            "details": "No URL was found in the input."
        }

    signals = []
    score = 0
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        path = (parsed.path or "").lower()
        full = url.lower()

        if parsed.scheme != "https":
            score += 12
            signals.append(("medium", "The URL does not use HTTPS."))

        if len(url) > 90:
            score += 8
            signals.append(("low", "The URL is unusually long."))

        if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
            score += 20
            signals.append(("high", "The URL uses an IP address instead of a normal domain."))

        if host.count(".") >= 3:
            score += 8
            signals.append(("medium", "The domain has several subdomain levels."))

        if "@" in url:
            score += 20
            signals.append(("high", "The URL contains '@', which can be used to disguise the destination."))

        for word in SUSPICIOUS_WORDS:
            if word in host.lower() or word in path or word in full:
                score += 4
                signals.append(("low", f"Security-sensitive keyword detected: '{word}'."))

        for tld in SUSPICIOUS_TLDS:
            if host.lower().endswith(tld):
                score += 10
                signals.append(("medium", f"The domain uses the '{tld}' top-level domain. This is only a signal, not proof of abuse."))
                break

        # Keep URL score bounded.
        score = min(score, 50)
        if not signals:
            signals.append(("info", "No strong URL-level warning signal was detected."))

        return {"found": True, "score": score, "signals": signals, "details": f"Analyzed domain: {host}"}
    except Exception:
        return {
            "found": True, "score": 10,
            "signals": [("medium", "The URL could not be fully parsed.")],
            "details": "Partial URL analysis only."
        }
