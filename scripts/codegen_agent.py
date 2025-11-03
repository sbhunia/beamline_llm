from __future__ import annotations
import os, time, statistics, uuid
from typing import Dict, Any, List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

from scripts.load_drive_code import load_drive_docs
from scripts.log_utils import log_stage, log_event
from scripts.query_rewrite import rewrite_user_query
from scripts.prompt_template import BASE_PROMPT_CODE
from scripts.spec_parser import validate_spec_code


OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("CODE_MODEL", "codellama:7b-instruct")
TOP_K = int(os.getenv("RAG_TOP_K", "8"))
PER_CHUNK_CHARS = int(os.getenv("PER_CHUNK_CHARS", "1000"))
_VS: FAISS | None = None

def _build_vs(request_id: str) -> FAISS:
    """Build or reuse a FAISS store; log vectorstore metadata."""
    global _VS
    if _VS is not None:
        return _VS

    docs: List[Document] = load_drive_docs()
    if not docs:
        docs = [Document(page_content="SPEC macro reference placeholder.", metadata={"source": "dummy"})]

    emb_model = "sentence-transformers/all-mpnet-base-v2"
    emb = HuggingFaceEmbeddings(model_name=emb_model)
    _VS = FAISS.from_documents(docs, emb)

    log_stage("vectorstore_init", "vectorstore_init", {
        "agent": "code",
        "request_id": request_id,
        "source": "load_drive_docs",
        "vector_dim": 768,
        "retrieved": f"chunks={len(docs)}, chunk_chars={PER_CHUNK_CHARS}, overlap=200, emb_model={emb_model}",
    })
    return _VS


def _search(task: str, vs: FAISS, request_id: str, k: int = TOP_K) -> List[Tuple[Document, float]]:
    """Search FAISS, apply keyword boosting, compute retrieval stats."""
    try:
        query_vec = vs.embedding_function.embed_query(task)
        log_stage(task, "embedding_query", {
            "agent": "code",
            "request_id": request_id,
            "vector_dim": len(query_vec),
            "vector_preview": [round(x, 5) for x in query_vec[:10]],
        })
    except Exception as e:
        print(f"[code] embedding query failed: {e}")

    hits = vs.similarity_search_with_score(task, k=k)
    keywords = ["def ", "ascan", "flyscan", "macro", "loop", "if", "umv", "open", "close"]
    boosted, boosted_indices = [], []

    for i, (doc, score) in enumerate(hits):
        txt = (doc.page_content or "").lower()
        if any(kw in txt for kw in keywords):
            boosted.append((doc, score * 0.9))
            boosted_indices.append(i)

    merged = sorted(hits + boosted, key=lambda x: x[1])[:k]
    scores = [float(s) for _, s in merged]
    best, avg, spread = min(scores), statistics.mean(scores), max(scores) - min(scores)
    confidence = round(1 / (1 + avg), 4)

    log_stage(task, "retrieval", {
        "agent": "code",
        "request_id": request_id,
        "retrieved": [
            {
                "source": doc.metadata.get("source", "unknown"),
                "score": float(score),
                "snippet": (doc.page_content or "")[:250],
            } for doc, score in merged
        ],
        "score": f"best={best:.3f}, avg={avg:.3f}, spread={spread:.3f}, conf={confidence}",
        "prompt_chars": len(str(scores)),
    })
    return merged, confidence


def _call_llm(prompt: str, request_id: str) -> Tuple[str, float]:
    start = time.time()
    try:
        llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
        out = llm.invoke([{"role": "user", "content": prompt}])
        latency = (time.time() - start) * 1000
        response = getattr(out, "content", str(out)) or ""
        log_stage(prompt[:60], "llm_call", {
            "agent": "code",
            "request_id": request_id,
            "source": DEFAULT_MODEL,
            "score": latency,
            "prompt_chars": len(prompt),
            "raw_output_preview": response[:200],
        })
        return response, latency
    except Exception as e:
        latency = (time.time() - start) * 1000
        print(f"[code] LLM call failed: {e}")
        return f"LLM error: {e}", latency


def run_codegen_ui(task: str) -> Dict[str, Any]:
    request_id = "REQ_" + uuid.uuid4().hex[:8]

    log_event("user_query_received", {
        "agent": "code",
        "request_id": request_id,
        "original_query": task,
        "method": "llm-rag",
    })

    normalized = normalize_macro_query(task)
    rewritten = rewrite_user_query(normalized)

    log_event("query_rewrite", {
        "agent": "code",
        "request_id": request_id,
        "original_query": task,          
        "rewritten_query": rewritten,    
        "route": "code",
    })

    vs = _build_vs(request_id)
    hits, confidence = _search(rewritten, vs, request_id, k=TOP_K)

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
    prompt_tokens_est = len(prompt) // 4

    log_stage(task, "prompt", {
        "agent": "code",
        "request_id": request_id,
        "prompt_chars": len(prompt),
        "prompt_preview": prompt[:200],
        "retrieved": [r["source"] for r in retrieved_chunks],
        "score": f"top_k={len(retrieved_chunks)}, token_est={prompt_tokens_est}",
    })

    raw_out, latency = _call_llm(prompt, request_id)
    draft = (raw_out or "").strip()
    parser_ok = validate_spec_code(draft)

    log_stage(task, "parser_check", {
        "agent": "code",
        "request_id": request_id,
        "score": str(parser_ok),
        "raw_output_preview": draft[:200],
    })

    log_stage(task, "final", {
        "agent": "code",
        "request_id": request_id,
        "final_output_preview": draft[:200],
        "score": f"conf={confidence}, latency_ms={latency:.1f}, parser_ok={parser_ok}",
    })

    log_event("ui_return", {
        "agent": "code",
        "request_id": request_id,
        "original_query": task,
        "rewritten_query": rewritten,
        "confidence": confidence,
        "parser_passed": parser_ok,
        "sources": [r["source"] for r in retrieved_chunks],
        "prompt_chars": len(prompt),
        "preview": draft[:200],
    })

    return {
        "code": draft or 'print "insufficient evidence"',
        "retrieved": retrieved_chunks,
        "debug": {
            "exact_prompt": prompt,
            "rag_context": rag_blob,
            "raw_output": raw_out,
            "confidence_est": confidence,
            "parser_ok": parser_ok,
            "latency_ms": latency,
        },
        "method": "llm-rag",
    }
