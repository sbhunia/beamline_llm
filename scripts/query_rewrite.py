import re

def rewrite_user_query(q: str) -> str:
    q = (q or "").strip()
    lower = q.lower()

    # Normalize spacing and punctuation
    q = re.sub(r"\s+", " ", q)

    # Argument normalization (optional)
    q = re.sub(r"\bdevice\b", "addr", q, flags=re.IGNORECASE)
    q = re.sub(r"\bstring\b", "s", q, flags=re.IGNORECASE)

    # 🪄 Expansion for bare keywords or single function names
    if re.fullmatch(r"[a-zA-Z0-9_]+", q):
        return (f"Explain the meaning, usage, and behavior of the SPEC command or function {q}. "
                f"Include syntax variants like {q}(addr, s) or {q}(arguments).")

    # Expansion for short phrases
    if len(q.split()) <= 3 and not any(
        w in lower for w in ["what", "define", "explain", "describe", "elaborate", "how", "why"]
    ):
        return (f"Explain the meaning, usage, and behavior of the command or code: {q}. "
                f"Consider argument variations like (addr, s).")

    # Direct 'what/define/explain' handling
    if any(lower.startswith(w) for w in ["what", "define", "explain", "describe", "elaborate", "how", "why"]):
        return f"Explain in detail: {q}"

    # Single word 'what' and such
    if lower in ("what", "??", "?"):
        return "Explain the meaning and usage of the command or code."

    return (f"Explain the meaning, usage, and behavior of the command or code: {q}. "
            f"Also consider related variants and argument forms.")
