# ==================================================
# DECISION SERVICE
# ==================================================

def decide(total_score: int) -> str:
    """
    Convert total score into hiring decision.

    Rules:
    - 0–39  → rejected
    - 40–64 → manual_review
    - 65+   → shortlisted
    """

    # Safety check for invalid values
    try:
        score = int(total_score)
    except (TypeError, ValueError):
        return "failed"

    if score < 40:
        return "rejected"
    elif score < 65:
        return "manual_review"
    return "shortlisted"