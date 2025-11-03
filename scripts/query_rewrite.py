import re
from scripts.log_utils import log_event  # optional: for logging intermediate normalization

def normalize_macro_query(q: str) -> str:
    """
    Normalize natural-language queries that imply macro definition intent.
    Expands to handle phrasing variants like 'create a spec macro' or
    'generate macro code to set motor speed'.
    """
    qlow = q.lower()
    action_verbs = ["change", "set", "move", "scan", "ramp", "shift", "start", "stop"]

    re_macro = re.compile(
        r"(?:write|create|make|generate|produce)\s+(?:a\s+)?(?:spec\s*)?(?:macro|macro\s*code)",
        re.IGNORECASE,
    )

    if re_macro.search(qlow) and any(v in qlow for v in action_verbs):
        q = re_macro.sub("SPEC command", q)
        q = re.sub(r"\bto\s+", "to ", q, flags=re.IGNORECASE)

    return q.strip()


def rewrite_user_query(q: str) -> str:
    """
    Lightweight rewrite for FAISS retrieval consistency.
    Expands abbreviations, standardizes phrasing, and ensures
    that short or identifier-like queries are contextually wrapped.
    """
    q = (q or "").strip()
    normalized = normalize_macro_query(q)
    q = re.sub(r"\s+", " ", normalized)

    # basic lexical harmonization
    q = re.sub(r"\btemp\b", "temperature", q, flags=re.IGNORECASE)
    q = re.sub(r"\bscan\b", "scanning", q, flags=re.IGNORECASE)

    # for single identifiers or short phrases, wrap them
    if re.fullmatch(r"[a-zA-Z0-9_]+", q):
        rewritten = f"SPEC macro example showing usage of {q}"
    elif len(q.split()) <= 4:
        rewritten = f"SPEC macro example for {q}"
    else:
        rewritten = q

    # optional logging hook for traceability
    if rewritten != q:
        log_event("query_rewritten", {
            "original_query": q,
            "rewritten_query": rewritten,
        })

    return rewritten
