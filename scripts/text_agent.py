from __future__ import annotations
import os, re
from typing import Dict, Any, List, Optional

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import ChatOllama

try:
    from langchain_ollama import OllamaEmbeddings
    _HAS_OLLAMA_EMB = True
except Exception:
    _HAS_OLLAMA_EMB = False

from scripts.load_drive import load_drive_docs
from scripts.load_markdown import load_markdown_docs
from scripts.load_website import load_website
from scripts.log_utils import log_stage  # <-- added

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("TEXT_MODEL", os.getenv("CODE_MODEL", "mistral:latest"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "")
WEBSITE_URL = os.getenv("WEBSITE_URL", "https://suchismitasarker.github.io/CHESS-ID4B-QM2/")
ENABLE_WEBSITE = os.getenv("ENABLE_WEBSITE", "0") not in ("0", "false", "False", "")

TOP_K = int(os.getenv("RAG_TOP_K", "20"))
PROMPT_CHUNK_LIMIT = int(os.getenv("PROMPT_CHUNK_LIMIT", "10"))
PER_CHUNK_CHARS = int(os.getenv("PER_CHUNK_CHARS", "1200"))

_VS: Optional[FAISS] = None

# ---------------- Vector store builder ----------------
def _build_vs() -> FAISS:
    global _VS
    if _VS is not None:
        return _VS

    docs: List[Document] = []
    docs += load_drive_docs()
    docs += load_markdown_docs()
    if ENABLE_WEBSITE:
        try:
            docs += load_website(WEBSITE_URL)
        except Exception as e:
            print(f"[text] Skipping website due to error: {e}")

    if not docs:
        docs = [Document(page_content="SPEC macro language reference stub.", metadata={"source":"dummy"})]

    for d in docs:
        if isinstance(d.page_content, str):
            d.page_content = (
                d.page_content.replace("\u2018", "'").replace("\u2019", "'")
                              .replace("\u201C", '"').replace("\u201D", '"')
            )

    emb = None
    if EMBED_MODEL and _HAS_OLLAMA_EMB:
        try:
            emb = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE)
            print(f"[text] Using OllamaEmbeddings: {EMBED_MODEL}")
        except Exception as e:
            print(f"[text] OllamaEmbeddings failed: {e} → falling back to HF")

    if emb is None:
        from langchain_huggingface import HuggingFaceEmbeddings
        emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("[text] Using HuggingFaceEmbeddings: all-MiniLM-L6-v2")

    _VS = FAISS.from_documents(docs, emb)
    return _VS


# ---------------- Prompt ----------------
BASE_PROMPT = """You answer questions using SPEC-related documents.

QUESTION:
{question}

Relevant excerpts:
{spec}

INSTRUCTIONS:
- Use the excerpts as your ONLY building blocks for SPEC-specific facts.
- If the answer is directly supported, state it concisely.
- If you must combine info logically across excerpts, add:
  Note: inferred from manual patterns; not explicitly stated in one place.
- If the excerpts don’t support the answer, reply exactly:
  I don’t see that in the provided documents.
- Output plain English only.
"""

def _normalize_query(q: str) -> str:
    q = q or ""
    q = q.strip()
    q = re.sub(r"\s+", " ", q)
    return q

def _call_llm(prompt: str, temperature: float = 0.0) -> str:
    try:
        llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=temperature)
        out = llm.invoke([{"role": "user", "content": prompt}])
        return getattr(out, "content", str(out)) or ""
    except Exception as e:
        print(f"[text] LLM call error: {e}")
        return ""


# ---------------- Public API ----------------
def answer(query: str) -> Dict[str, Any]:
    q_raw = (query or "").strip()
    q_lower = q_raw.lower()

    if re.fullmatch(r"(hi|hey|hello|yo|sup|hola)[.! ]*", q_lower):
        msg = "Hey! I can explain SPEC docs or help craft macros. Try “what is ascan” or “write a macro to rotate the sample 3 times”."
        return {
            "answer": msg, "grounded": False, "inferred": False,
            "sources": [], "prompt_chars": 0, "raw_prompt": "", "rag_excerpts": []
        }

    if not any(w in q_lower for w in ["spec","ascan","dscan","mesh","umv","mv","motor","detector","beamline","macro","scan"]) and "?" not in q_lower:
        return {
            "answer": "I don’t see that in the provided documents.",
            "grounded": False, "inferred": False, "sources": [],
            "prompt_chars": 0, "raw_prompt": "", "rag_excerpts": []
        }

    vs = _build_vs()
    q = _normalize_query(q_raw)

    # --- Log query embedding ---
    try:
        query_vec = vs.embedding_function.embed_query(q)
        log_stage(q, "embedding_query", {
            "agent": "text",
            "vector_dim": len(query_vec),
            "vector_preview": [round(x, 5) for x in query_vec[:10]]
        })
    except Exception as e:
        print(f"[text] Failed to embed query for logging: {e}")

    hits = vs.similarity_search_with_score(q, k=TOP_K)
    top = hits[:PROMPT_CHUNK_LIMIT]

    excerpts, sources = [], []
    for doc, score in top:
        txt = (doc.page_content or "").strip()
        if not txt:
            continue

        # --- Log doc embedding ---
        try:
            doc_vec = vs.embedding_function.embed_query(txt[:500])
            log_stage(q, "embedding_doc", {
                "agent": "text",
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score),
                "vector_dim": len(doc_vec),
                "vector_preview": [round(x, 5) for x in doc_vec[:10]]
            })
        except Exception as e:
            print(f"[text] Failed to embed doc for logging: {e}")

        excerpts.append(txt[:PER_CHUNK_CHARS])
        sources.append((doc.metadata.get("source","unknown"), float(score)))

    # --- Log retrieval summary WITH SNIPPETS ---
    log_stage(q, "retrieval", {
        "agent": "text",
        "retrieved": [
            {
                "source": doc.metadata.get("source","unknown"),
                "score": float(score),
                "snippet": (doc.page_content or "")[:300]  # capture first 300 chars
            }
            for doc, score in top if doc.page_content
        ]
    })

    if not excerpts:
        return {
            "answer": "I don’t see that in the provided documents.",
            "grounded": False, "inferred": False, "sources": [],
            "prompt_chars": 0,
            "raw_prompt": BASE_PROMPT.format(question=q, spec=""),
            "rag_excerpts": [],
        }

    rag_joined = "\n\n---\n\n".join(excerpts)
    prompt = BASE_PROMPT.format(question=q, spec=rag_joined)

    # --- Log prompt ---
    log_stage(q, "prompt", {
        "agent": "text",
        "prompt_chars": len(prompt),
        "prompt_preview": prompt[:200]
    })

    out = _call_llm(prompt, temperature=0.0).strip()

    # --- Log raw output ---
    log_stage(q, "llm_call", {
        "agent": "text",
        "raw_output_preview": out[:200]
    })

    grounded = out == "I don’t see that in the provided documents." or "Note: inferred from manual patterns" not in out
    inferred = "Note: inferred from manual patterns" in out

    # --- Log final ---
    log_stage(q, "final", {
        "agent": "text",
        "final_output_preview": out
    })

    return {
        "answer": out if out else "I don’t see that in the provided documents.",
        "grounded": out != "I don’t see that in the provided documents." and not inferred,
        "inferred": inferred,
        "sources": sources,
        "prompt_chars": len(prompt),
        "raw_prompt": prompt,
        "rag_excerpts": excerpts[:5],
    }

