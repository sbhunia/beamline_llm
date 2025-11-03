import re

def normalize_macro_query(q: str) -> str:
    """
    Normalize natural-language queries that accidentally suggest macro definition.
    Converts phrases like 'write a spec macro code to ...'
    into 'SPEC command to ...' if the intent sounds actionable
    (change, set, move, scan, ramp, shift, start, stop, etc.).
    """
    qlow = q.lower()

    action_verbs = ["change", "set", "move", "scan", "ramp", "shift", "start", "stop"]

    if "macro" in qlow and any(v in qlow for v in action_verbs):
        q = re.sub(r"spec\s*macro\s*code", "SPEC command", q, flags=re.IGNORECASE)
        q = re.sub(r"write\s+a\s*", "", q, flags=re.IGNORECASE)

    return q.strip()


def rewrite_user_query(q: str) -> str:
    """
    Lightweight rewrite — improve retrieval without bloating prompt.
    Combines query normalization + compact semantic rewrites
    for consistent FAISS retrieval performance.
    """
    q = (q or "").strip()
    q = normalize_macro_query(q)
    q = re.sub(r"\s+", " ", q)

    q = re.sub(r"\btemp\b", "temperature", q, flags=re.IGNORECASE)
    q = re.sub(r"\bscan\b", "scanning", q, flags=re.IGNORECASE)

    
    if re.fullmatch(r"[a-zA-Z0-9_]+", q):
        return f"SPEC macro example showing usage of {q}"

    # Simple short phrase rewrite
    if len(q.split()) <= 4:
        return f"SPEC macro example for {q}"

    return q
