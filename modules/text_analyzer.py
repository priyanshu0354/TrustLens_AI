import re

PATTERNS = {
    "urgency": [
        "urgent", "immediately", "act now", "today", "within 30 minutes",
        "within 1 hour", "final notice", "last chance", "expires today",
        "before midnight", "as soon as possible"
    ],
    "credential": [
        "password", "pin", "cvv", "otp", "card number", "login",
        "verify your identity", "account details", "bank details"
    ],
    "money": [
        "pay", "payment", "fee", "transfer", "send ₹", "send rs",
        "cashback", "refund", "investment", "upi"
    ],
    "reward": [
        "won", "winner", "prize", "reward", "gift", "lottery",
        "cashback", "selected"
    ],
    "threat": [
        "blocked", "suspended", "deleted", "closed", "disabled",
        "disconnected", "stop working", "permanently deleted"
    ]
}

def analyze_text(text: str):
    lower = (text or "").lower()
    signals = []
    score = 0
    categories = []

    for name, phrases in PATTERNS.items():
        hits = [p for p in phrases if p in lower]
        if hits:
            categories.append(name)
            if name == "urgency":
                score += min(18, 6 * len(hits))
                signals.append(("high", f"Urgency language detected: {', '.join(hits[:3])}."))
            elif name == "credential":
                score += min(24, 8 * len(hits))
                signals.append(("high", f"Credential/sensitive-data language detected: {', '.join(hits[:3])}."))
            elif name == "money":
                score += min(18, 6 * len(hits))
                signals.append(("medium", f"Payment or financial language detected: {', '.join(hits[:3])}."))
            elif name == "reward":
                score += min(12, 6 * len(hits))
                signals.append(("medium", f"Reward/prize language detected: {', '.join(hits[:3])}."))
            elif name == "threat":
                score += min(15, 7 * len(hits))
                signals.append(("high", f"Threat/account-consequence language detected: {', '.join(hits[:3])}."))

    if re.search(r"\b(click|tap|open)\b", lower) and re.search(r"https?://", lower):
        score += 8
        signals.append(("medium", "The message combines an action request with a link."))

    return {
        "score": min(score, 70),
        "signals": signals,
        "categories": categories
    }
