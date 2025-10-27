# ===============================================
# CODEGEN AGENT (Final Simplified Version)
# ===============================================
# Purpose: SPEC Macro Generator (Cookbook + Manual RAG)
# Model: codellama:7b-instruct
# Logs: embeddings, retrieval, prompt, raw output, final
# ===============================================

from __future__ import annotations
import os
from typing import Dict, Any, List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

from scripts.load_drive_code import load_drive_docs
from scripts.log_utils import log_stage, log_event
from scripts.query_rewrite import rewrite_user_query
from scripts.prompt_template import BASE_PROMPT_CODE

# ---------------- Config ----------------
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("CODE_MODEL", "codellama:7b-instruct")

TOP_K = int(os.getenv("RAG_TOP_K", "8"))
PER_CHUNK_CHARS = int(os.getenv("PER_CHUNK_CHARS", "1000"))
_VS: FAISS | None = None


# ---------------- Vector Store ----------------
def _build_vs() -> FAISS:
    """Build a single FAISS store from cookbook + manual."""
    global _VS
    if _VS is not None:
        return _VS

    docs: List[Document] = load_drive_docs()  # cookbook + manual sources merged
    if not docs:
        docs = [Document(page_content="SPEC macro reference placeholder.", metadata={"source": "dummy"})]

    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    _VS = FAISS.from_documents(docs, emb)
    print(f"[DEBUG] VectorStore built: {len(docs)} docs")
    return _VS


# ---------------- Retrieval ----------------
def _search(task: str, vs: FAISS, k: int = TOP_K) -> List[Tuple[Document, float]]:
    """Search with keyword boosting."""
    try:
        query_vec = vs.embedding_function.embed_query(task)
        log_stage(task, "embedding_query", {
            "agent": "code",
            "vector_dim": len(query_vec),
            "vector_preview": [round(x, 5) for x in query_vec[:10]],
        })
    except Exception as e:
        print(f"[code] embedding query failed: {e}")

    hits = vs.similarity_search_with_score(task, k=k)
    keywords = ["def ", "ascan", "flyscan", "macro", "loop", "if", "umv", "open", "close"]
    boosted = []
    for doc, score in hits:
        txt = (doc.page_content or "").lower()
        if any(kw in txt for kw in keywords):
            boosted.append((doc, score * 0.7))

    merged = sorted(hits + boosted, key=lambda x: x[1])[:k]

    # Log retrieval details
    log_stage(task, "retrieval", {
        "agent": "code",
        "retrieved": [
            {
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score),
                "snippet": (doc.page_content or "")[:300],
            } for doc, score in merged
        ],
    })
    return merged


# ---------------- LLM Caller ----------------
def _call_llm(prompt: str) -> str:
    try:
        llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
        print(f"[DEBUG] Calling Ollama → {DEFAULT_MODEL}")
        out = llm.invoke([{"role": "user", "content": prompt}])
        print(f"[DEBUG] Ollama raw (CODE): {out}")
        return getattr(out, "content", str(out)) or ""
    except Exception as e:
        print(f"[code] LLM call failed: {e}")
        return ""


# ---------------- Main Entry ----------------
def run_codegen_ui(task: str) -> Dict[str, Any]:
    rewritten = rewrite_user_query(task)
    print(f"[DEBUG] Query rewrite: {task!r} → {rewritten!r}")

    log_event("query_rewrite", {
        "agent": "code",
        "original_query": task,
        "rewritten_query": rewritten,
    })

    vs = _build_vs()
    hits = _search(rewritten, vs, k=TOP_K)

    excerpts, retrieved_chunks = [], []
    for doc, score in hits:
        snippet = (doc.page_content or "").strip()
        if snippet:
            excerpts.append(snippet[:PER_CHUNK_CHARS])
            retrieved_chunks.append({
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score),
                "snippet": snippet[:300],
            })

    rag_blob = "\n\n---\n\n".join(excerpts)
    prompt = BASE_PROMPT_CODE.format(task=rewritten, manual=rag_blob)

    log_stage(task, "prompt", {
        "agent": "code",
        "prompt_chars": len(prompt),
        "prompt_preview": prompt[:200],
    })

    raw_out = _call_llm(prompt)
    log_stage(task, "llm_call", {
        "agent": "code",
        "raw_output_preview": raw_out[:200],
    })

    draft = (raw_out or "").strip()

    log_stage(task, "final", {
        "agent": "code",
        "final_output_preview": draft[:200],
    })

    return {
        "code": draft or 'print "insufficient evidence"',
        "retrieved": retrieved_chunks,
        "debug": {"exact_prompt": prompt, "rag_context": rag_blob, "raw_output": raw_out},
        "method": "llm-rag",
    }
