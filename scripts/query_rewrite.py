import re

def rewrite_user_query(q: str) -> str:
    """Lightweight rewrite — improve retrieval without bloating prompt."""
    q = (q or "").strip()
    q = re.sub(r"\s+", " ", q)

    # Common synonyms
    q = re.sub(r"\btemp\b", "temperature", q, flags=re.IGNORECASE)
    q = re.sub(r"\bscan\b", "scanning", q, flags=re.IGNORECASE)

    # Simple single-word expansions
    if re.fullmatch(r"[a-zA-Z0-9_]+", q):
        return f"SPEC macro example showing usage of {q}"

    # Simple short phrase rewrite
    if len(q.split()) <= 4:
        return f"SPEC macro example for {q}"

    return q
