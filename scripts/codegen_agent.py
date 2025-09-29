from __future__ import annotations
import os, re
from typing import Dict, Any, List, Optional

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_ollama import ChatOllama

from scripts.load_drive import load_drive_docs

# =========================
# Config
# =========================
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("CODE_MODEL", os.getenv("TEXT_MODEL", "mistral:latest"))

# Cache VS (manual docs only)
_VS: Optional[FAISS] = None


def _build_vs() -> FAISS:
    """
    Build and cache FAISS vector store from drive docs (SPEC manual).
    """
    global _VS
    if _VS is not None:
        return _VS
    docs: List[Document] = load_drive_docs()
    for d in docs:
        if isinstance(d.page_content, str):
            d.page_content = (
                d.page_content
                .replace("\u2018", "'").replace("\u2019", "'")
                .replace("\u201C", '"').replace("\u201D", '"')
            )
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    _VS = FAISS.from_documents(docs, emb)
    return _VS


# =========================
# Prompt
# =========================
BASE_PROMPT = """You are an expert in SPEC (x-ray beamline control).

USER TASK:
{task}

Relevant manual excerpts (normalized quotes):
{spec}

INSTRUCTIONS:
- Produce SPEC code ONLY. No explanations, no backticks, no prose.
- Either:
  (A) define a macro with ASCII single quotes:
      def name '
          # body
      '
  or
  (B) output a plain command block (no def) that can run in a command file.
- Use identifiers consistent with the excerpts (mv/umv/_mv, move_em, waitmove, getangles, printf/print/fprintf(PRINTER,...), for()/while(), etc.) as needed.
- If requested to "add a comment"/"printer note", include a print/printf or fprintf(PRINTER, ...).
- If excerpts are insufficient, return a minimal SPEC command that parses,
  OR a best-effort macro using primitives, but prepend:
  print "⚠ Proposed from manual primitives; not an exact recipe in the manual."
"""

REPAIR_SUFFIX = """

The code above was rejected by a validator because of these issues:
{issues}

Repair the code using the SAME excerpts.
Return SPEC code ONLY (no prose).
"""


# =========================
# LLM wrapper
# =========================
def _call_llm(prompt: str, temperature: float) -> str:
    llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=temperature)
    out = llm.invoke([{"role": "user", "content": prompt}])
    raw = getattr(out, "content", "")
    return raw if isinstance(raw, str) else str(raw)


# =========================
# Soft validator
# =========================
_SPEC_TOKENS = (
    "def ", "umv", "umvr", "mv", "move_em", "move_all",
    "waitmove", "getangles", "ascan", "dscan", "mesh", "for (", "while (",
    "print", "printf", "fprintf", "PRINTER"
)

def _looks_like_spec(code: str) -> bool:
    if not isinstance(code, str) or not code.strip():
        return False
    c = code.strip()
    if c.startswith("def "):
        if ("'" in c) or ("\u2018" in c) or ("\u2019" in c):
            return True
    hits = sum(1 for t in _SPEC_TOKENS if t in c)
    return hits >= 2


# =========================
# Public API
# =========================
def run_codegen_ui(task: str) -> Dict[str, Any]:
    """
    Runs retrieval + generation, returns:
      - code: final SPEC (or fallback)
      - raw_prompt: the exact prompt sent to the model
      - raw_model_outputs: {'draft': <raw>, 'repaired': <raw or ''>}
      - rag_excerpts: list of retrieved excerpt previews
      - rag_joined: the full text blob injected into the prompt
      - _debug: metadata on retrieval + attempts
    """
    vs = _build_vs()
    hits = vs.similarity_search_with_score(task, k=20)
    top = hits[:10]

    excerpts: List[str] = []
    retrieved: List[Dict[str, Any]] = []
    for doc, score in top:
        txt = (doc.page_content or "").strip()
        if not txt:
            continue
        full_excerpt = txt
        prompt_excerpt = txt[:1200]
        excerpts.append(prompt_excerpt)
        retrieved.append({
            "src": doc.metadata.get("source", "unknown"),
            "score": float(score),
            "chunk_head": full_excerpt[:500],
            "chunk_len": len(full_excerpt),
            "doc_meta": {k: v for k, v in (doc.metadata or {}).items()}
        })

    if not excerpts:
        return {
            "code": 'print "insufficient evidence"',
            "rationale": "No relevant chunks retrieved from manual.",
            "warnings": "insufficient-evidence",
            "raw_prompt": BASE_PROMPT.format(task=task, spec=""),
            "raw_model_outputs": {"draft": "", "repaired": ""},
            "rag_excerpts": [],
            "rag_joined": "",
            "_debug": {"retrieved": [], "attempts": []},
        }

    rag_joined = "\n\n---\n\n".join(excerpts)
    prompt = BASE_PROMPT.format(task=task, spec=rag_joined)

    # ===== Draft =====
    draft_raw = _call_llm(prompt, temperature=0.0)
    draft = (draft_raw or "").strip()
    attempts = [{"round": 1, "accepted": _looks_like_spec(draft), "code_head": draft[:500]}]

    if _looks_like_spec(draft):
        return {
            "code": draft,
            "rationale": "Generated from manual excerpts.",
            "warnings": "",
            "raw_prompt": prompt,
            "raw_model_outputs": {"draft": draft_raw, "repaired": ""},
            "rag_excerpts": [r.get("chunk_head") for r in retrieved],
            "rag_joined": rag_joined,
            "_debug": {"retrieved": retrieved, "attempts": attempts},
        }

    # ===== Repair =====
    issues = []
    if not draft.strip():
        issues.append("empty output")
    if "def " in draft and ("'" not in draft and "\u2018" not in draft and "\u2019" not in draft):
        issues.append("macro body not enclosed in single quotes")
    if re.search(r"\b(comment|printer)\b", (task or "").lower()) and not re.search(r"print|printf|fprintf", draft, re.I):
        issues.append("missing requested comment/log")
    if re.search(r"\bmove\b.*\bmotor\b|\bmotor\b.*\bmove\b", (task or "").lower()) and not re.search(r"\bmv\b|\bumv\b|\bmove_em\b|\bmove_all\b", draft, re.I):
        issues.append("no motor move primitive detected")

    repair_prompt = (
        BASE_PROMPT.format(task=task, spec=rag_joined)
        + REPAIR_SUFFIX.format(issues="\n- ".join(issues) or "- unspecified")
    )
    repaired_raw = _call_llm(repair_prompt, temperature=0.1)
    repaired = (repaired_raw or "").strip()
    attempts.append({"round": 2, "accepted": _looks_like_spec(repaired), "issues": issues, "code_head": repaired[:500]})

    if _looks_like_spec(repaired):
        return {
            "code": repaired,
            "rationale": "Generated after one repair pass.",
            "warnings": "",
            "raw_prompt": prompt,
            "raw_model_outputs": {"draft": draft_raw, "repaired": repaired_raw},
            "rag_excerpts": [r.get("chunk_head") for r in retrieved],
            "rag_joined": rag_joined,
            "_debug": {"retrieved": retrieved, "attempts": attempts, "repair_prompt_head": repair_prompt[:1200]},
        }

    # ===== Fallback =====
    stub = 'print "insufficient evidence"'
    attempts.append({"round": 3, "accepted": True, "issues": ["fallback"], "code_head": stub})
    return {
        "code": stub,
        "rationale": "Returned a minimal SPEC command after failed attempts.",
        "warnings": "insufficient-evidence",
        "raw_prompt": prompt,
        "raw_model_outputs": {"draft": draft_raw, "repaired": repaired_raw},
        "rag_excerpts": [r.get("chunk_head") for r in retrieved],
        "rag_joined": rag_joined,
        "_debug": {"retrieved": retrieved, "attempts": attempts, "repair_prompt_head": repair_prompt[:1200]},
    }


def explain_spec_code(code: str) -> str:
    llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
    prompt = (
        "Explain the following SPEC code clearly and concisely. "
        "Do not speculate beyond the code. If something is unclear, say so.\n\n"
        "CODE:\n```spec\n" + (code or "") + "\n```"
    )
    out = llm.invoke([{"role": "user", "content": prompt}])
    return getattr(out, "content", str(out))
