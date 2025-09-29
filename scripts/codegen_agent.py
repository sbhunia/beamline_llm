# =========================
# codegen_agent_simple.py
# LLM with RAG over SPEC manual (PDFs)
# =========================

from __future__ import annotations
import os
from typing import Dict, Any, List, Tuple

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from scripts.load_drive_code import load_drive_docs   # <- your chunked PDF loader
from scripts.log_utils import log_stage  # <-- added

# ---------------- Config ----------------
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("CODE_MODEL", os.getenv("TEXT_MODEL", "mistral:latest"))

TOP_K = int(os.getenv("RAG_TOP_K", "8"))         # number of chunks to pull per query
PER_CHUNK_CHARS = int(os.getenv("PER_CHUNK_CHARS", "1200"))

# Cache vectorstore
_VS: FAISS | None = None

# ---------------- Vector Store ----------------
def _build_vs() -> FAISS:
    global _VS
    if _VS is not None:
        return _VS

    docs: List[Document] = load_drive_docs()
    if not docs:
        docs = [Document(
            page_content="SPEC is a powerful macro language for instrument control.",
            metadata={"source": "dummy.pdf"}
        )]

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    _VS = FAISS.from_documents(docs, emb)
    return _VS


# ---------------- Retriever ----------------
def _search(task: str, vs: FAISS, k: int = TOP_K) -> List[Tuple[Document, float]]:
    """Hybrid search: similarity + keyword boosting + filtering, with embedding logging."""

    # --- Step 1: compute and log query embedding ---
    try:
        query_vec = vs.embedding_function.embed_query(task)
        log_stage(task, "embedding_query", {
            "agent": "code",
            "vector_dim": len(query_vec),
            "vector_preview": [round(x, 5) for x in query_vec[:10]]
        })
    except Exception as e:
        print(f"[code] Failed to embed query for logging: {e}")

    # --- Step 2: similarity search ---
    hits = vs.similarity_search_with_score(task, k=k)
    hits = [(doc, score) for doc, score in hits if score < 1.3]

    # Step 3: keyword boosting
    keywords = ["def ", "macro", "setor", "calcg", "for ("]
    boosted = []
    for doc, score in hits:
        txt = (doc.page_content or "").lower()
        if any(kw in txt for kw in keywords):
            boosted.append((doc, score * 0.7))

    merged = hits + boosted
    merged = sorted(merged, key=lambda x: x[1])[:k]

    # --- Step 4: log doc embeddings ---
    for doc, score in merged:
        try:
            doc_vec = vs.embedding_function.embed_query(doc.page_content[:500])
            log_stage(task, "embedding_doc", {
                "agent": "code",
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score),
                "vector_dim": len(doc_vec),
                "vector_preview": [round(x, 5) for x in doc_vec[:10]]
            })
        except Exception as e:
            print(f"[code] Failed to embed doc for logging: {e}")

    # --- Step 5: log retrieval summary ---
    log_stage(task, "retrieval", {
    "agent": "code",
    "retrieved": [
        {
            "source": doc.metadata.get("source","unknown"),
            "score": float(score),
            "snippet": (doc.page_content or "")[:300]  # log first 300 chars of chunk
        }
        for doc, score in merged
    ]
})
    return merged


# ---------------- Prompt ----------------
BASE_PROMPT = """You are an expert in SPEC (beamline control macros).

Your task is to carefully study and learn the rules, syntax, and examples from the SPEC manual provided below. 
Use that manual as the single source of truth for how SPEC works.

-Relevant excerpts from the SPEC manual:
{manual}

-USER REQUEST:
{task}

- Output the code only in SPEC language syntax

INSTRUCTIONS:
- Base your answer only after understanding the spec code manual.
- Generate valid SPEC code that satisfies the user request.
- Output SPEC code ONLY (no explanations, no prose, no backticks).
- Output the code only in SPEC language syntax
"""


# ---------------- LLM Caller ----------------
def _call_llm(prompt: str) -> str:
    llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
    out = llm.invoke([{"role": "user", "content": prompt}])
    return getattr(out, "content", str(out)) or ""


# ---------------- Main Pipeline ----------------
def run_codegen_ui(task: str) -> Dict[str, Any]:
    vs = _build_vs()
    hits = _search(task, vs, k=TOP_K)

    retrieved_chunks, excerpts = [], []
    for doc, score in hits:
        snippet = (doc.page_content or "").strip()
        if snippet:
            excerpts.append(snippet[:PER_CHUNK_CHARS])
            retrieved_chunks.append({
                "score": float(score),
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "n/a"),
                "snippet": snippet[:300]
            })

    rag_blob = "\n\n---\n\n".join(excerpts)
    prompt = BASE_PROMPT.format(task=task, manual=rag_blob)

    # --- Log prompt ---
    log_stage(task, "prompt", {
        "agent": "code",
        "prompt_chars": len(prompt),
        "prompt_preview": prompt[:200]
    })

    raw_out = _call_llm(prompt)

    # --- Log raw output ---
    log_stage(task, "llm_call", {
        "agent": "code",
        "raw_output_preview": raw_out[:200]
    })

    draft = (raw_out or "").strip()

    # --- Log final output ---
    log_stage(task, "final", {
        "agent": "code",
        "final_output_preview": draft
    })

    if draft:
        return {
            "code": draft,
            "method": "llm-rag",
            "retrieved": retrieved_chunks,
            "debug": {
                "exact_prompt": prompt,
                "rag_context": rag_blob,
                "raw_output": raw_out
            }
        }

    return {
        "code": 'print "insufficient evidence"',
        "method": "fallback",
        "retrieved": retrieved_chunks,
        "debug": {
            "exact_prompt": prompt,
            "rag_context": rag_blob,
            "raw_output": raw_out
        }
    }
