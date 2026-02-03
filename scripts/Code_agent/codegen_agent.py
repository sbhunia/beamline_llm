from __future__ import annotations

import os
import time
import statistics
import uuid
from typing import Dict, Any, List, Tuple

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

from scripts.load_drive_code import load_drive_docs
from scripts.log_utils import log_stage, log_event
from scripts.query_rewrite import rewrite_user_query, normalize_macro_query
from scripts.prompt_template import BASE_PROMPT_CODE
from scripts.spec_parser import validate_spec_code

# ---------------- Config ----------------

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("CODE_MODEL", "llama2:latest")
TOP_K = int(os.getenv("RAG_TOP_K", "8"))

_VS: FAISS | None = None

# ---------------- Vector Store ----------------

def _build_vs(request_id: str) -> FAISS:
    global _VS
    if _VS:
        return _VS

    docs: List[Document] = load_drive_docs() or [
        Document(
            page_content="SPEC macro reference placeholder.",
            metadata={"source": "dummy", "kind": "manual"}
        )
    ]

    emb_model = "sentence-transformers/all-mpnet-base-v2"
    emb = HuggingFaceEmbeddings(model_name=emb_model)

    _VS = FAISS.from_documents(docs, emb)

    log_stage(
        "vectorstore_init",
        {
            "agent": "code",
            "request_id": request_id,
            "chunks": len(docs),
            "vector_dim": 768,
            "emb_model": emb_model,
        },
    )

    return _VS

# ---------------- Retrieval ----------------

def _search(
    retrieval_query: str,
    vs: FAISS,
    request_id: str,
    k: int = TOP_K,
) -> Tuple[List[Tuple[Document, float]], float]:

    query_vec = vs.embedding_function.embed_query(retrieval_query)

    log_stage(
        "embedding_query",
        {
            "agent": "code",
            "request_id": request_id,
            "vector_dim": len(query_vec),
            "query": retrieval_query,
        },
    )

    hits = vs.similarity_search_with_score(retrieval_query, k=k)

    # Prioritize macro / command definitions
    hits = sorted(
        hits,
        key=lambda x: (
            x[0].metadata.get("kind") not in ("macro", "command"),
            x[1],
        ),
    )

    merged = hits[:k]

    scores = [float(s) for _, s in merged]
    avg = statistics.mean(scores) if scores else None
    confidence = round(1 / (1 + max(avg, 1e-6)), 4) if avg is not None else 0.0

    log_stage(
        "retrieval",
        {
            "agent": "code",
            "request_id": request_id,
            "retrieved": [
                {
                    "source": d.metadata.get("source"),
                    "kind": d.metadata.get("kind"),
                    "score": float(s),
                    "snippet": d.page_content[:300],
                }
                for d, s in merged
            ],
            "confidence": confidence,
        },
    )

    return merged, confidence

# ---------------- LLM ----------------

def _call_llm(prompt: str, request_id: str) -> Tuple[str, float]:
    start = time.time()

    llm = ChatOllama(
        model=DEFAULT_MODEL,
        base_url=OLLAMA_BASE,
        temperature=0.0,
    )

    out = llm.invoke([{"role": "user", "content": prompt}])
    latency = (time.time() - start) * 1000
    response = getattr(out, "content", str(out)) or ""

    log_stage(
        "llm_call",
        {
            "agent": "code",
            "request_id": request_id,
            "latency_ms": round(latency, 2),
            "prompt_chars": len(prompt),
            "llm_output_full": response,
        },
    )

    return response, latency

# ---------------- Main Entry ----------------

def run_codegen_ui(task: str) -> Dict[str, Any]:
    request_id = "REQ_" + uuid.uuid4().hex[:8]

    log_event(
        "user_query_received",
        {
            "agent": "code",
            "request_id": request_id,
            "original_query": task,
        },
    )

    # ---------- Normalize ----------
    normalized = normalize_macro_query(task)
    rewritten = rewrite_user_query(normalized)

    # ---------- Detect LOOKUP intent ----------
    LOOKUP_TRIGGERS = [
        "spec command for",
        "command for",
        "what command",
        "which command",
        "read or set",
        "get the",
    ]

    is_lookup = any(t in normalized.lower() for t in LOOKUP_TRIGGERS)

    log_stage(
        "intent_detection",
        {
            "agent": "code",
            "request_id": request_id,
            "is_lookup": is_lookup,
            "normalized": normalized,
        },
    )

    # ---------- Retrieval ----------
    vs = _build_vs(request_id)
    hits, confidence = _search(
        retrieval_query=normalized.lower().strip(),
        vs=vs,
        request_id=request_id,
        k=TOP_K,
    )

    retrieved_chunks = [
        {
            "source": d.metadata.get("source"),
            "kind": d.metadata.get("kind"),
            "score": float(s),
            "snippet": d.page_content,
        }
        for d, s in hits
    ]

    rag_blob = "\n\n".join(r["snippet"] for r in retrieved_chunks[:4])

    # ---------- LOOKUP MODE (CRITICAL FIX) ----------
    if is_lookup:
        prompt = f"""
You are given SPEC documentation fragments.

TASK:
Return ONLY the SPEC command name that matches the task.

RULES:
- Output ONE command only
- No macro definitions
- No explanations
- No invented commands
- If no exact command is found, output: insufficient evidence

CONTEXT:
{rag_blob}

TASK:
{normalized}
"""
    else:
        # ---------- GENERATION MODE ----------
        prompt = BASE_PROMPT_CODE.format(
            task=rewritten,
            manual=rag_blob,
        )

    log_stage(
        "prompt",
        {
            "agent": "code",
            "request_id": request_id,
            "is_lookup": is_lookup,
            "prompt_full": prompt,
        },
    )

    # ---------- LLM ----------
    raw_out, latency = _call_llm(prompt, request_id)
    draft = (raw_out or "").strip()

    # ---------- Validate ----------
    parser_ok = validate_spec_code(draft) if not is_lookup else True

    log_stage(
        "final",
        {
            "agent": "code",
            "request_id": request_id,
            "confidence": confidence,
            "parser_ok": parser_ok,
            "final_output": draft,
        },
    )

    return {
        "code": draft or "insufficient evidence",
        "retrieved": retrieved_chunks[:4],
        "debug": {
            "is_lookup": is_lookup,
            "normalized": normalized,
            "rag_context": rag_blob,
            "raw_output": raw_out,
            "confidence": confidence,
        },
        "method": "llm-rag",
    }
