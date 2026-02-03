cleafrom __future__ import annotations

import os
import statistics
from typing import List, Tuple, Dict, Any

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from scripts.Text_agent.load_md import load_markdown_docs
from scripts.Text_agent.prompt_template import BASE_PROMPT_TEXT


# =====================================================
# Config
# =====================================================

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
MODEL = "mistral:instruct"
TOP_K = 8

_VS: FAISS | None = None


# =====================================================
# Vector Store
# =====================================================

def _build_vs() -> FAISS:
    global _VS
    if _VS is not None:
        return _VS

    docs: List[Document] = load_markdown_docs()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    _VS = FAISS.from_documents(docs, embeddings)
    return _VS


# =====================================================
# Retrieval
# =====================================================

def _search(
    query: str,
    vs: FAISS,
    k: int = TOP_K,
) -> Tuple[List[Tuple[Document, float]], float]:

    hits = vs.similarity_search_with_score(query, k=k)

    priority = {
        "procedure": 0,
        "command": 1,
        "table": 2,
        "markdown": 3,
    }

    hits = sorted(
        hits,
        key=lambda x: (
            priority.get(x[0].metadata.get("kind", "markdown"), 9),
            x[1],
        ),
    )

    scores = [float(s) for _, s in hits]
    avg = statistics.mean(scores) if scores else None
    confidence = round(1 / (1 + max(avg, 1e-6)), 4) if avg else 0.0

    return hits, confidence


# =====================================================
# LLM (ONLY used for non-extractive answers)
# =====================================================

def _call_llm(prompt: str) -> str:
    llm = ChatOllama(
        model=MODEL,
        base_url=OLLAMA_BASE,
        temperature=0.2,
    )

    out = llm.invoke([{"role": "user", "content": prompt}])
    return (getattr(out, "content", "") or "").strip()


# =====================================================
# Main Entry
# =====================================================

def run_text_ui(question: str) -> Dict[str, Any]:
    query = (question or "").strip().lower()

    vs = _build_vs()
    hits, confidence = _search(query, vs)

    # -------------------------------------------------
    # DOCUMENT-DRIVEN INTENT DETECTION (KEY FIX)
    # -------------------------------------------------

    procedure_hits: List[Tuple[Document, float]] = [
        (d, s) for d, s in hits
        if d.metadata.get("kind") == "procedure"
    ]

    lookup_hits: List[Tuple[Document, float]] = [
        (d, s) for d, s in hits
        if any(tok in d.page_content.lower() for tok in ["ip", "address:", "port", "password"])
    ]

    # -------------------------------------------------
    # MODE SELECTION (NO QUERY KEYWORDS)
    # -------------------------------------------------

    # PROCEDURE MODE
    if procedure_hits:
        filtered_hits = procedure_hits

    # LOOKUP MODE (FACT EXTRACTION)
    elif lookup_hits:
        filtered_hits = lookup_hits

    # FALLBACK (EXPLANATION)
    else:
        filtered_hits = hits

    # -------------------------------------------------
    # LOOKUP MODE → STRICT EXTRACTIVE ANSWER
    # -------------------------------------------------

    if filtered_hits is lookup_hits:
        answer = "Not found in the provided documents."

        for d, _ in filtered_hits:
            for line in d.page_content.splitlines():
                l = line.lower()
                if any(k in l for k in ["ip address", "ip:", "address:"]):
                    answer = line.strip()
                    break
            if answer != "Not found in the provided documents.":
                break

        return {
            "answer": answer,
            "confidence": confidence,
            "retrieved": [
                {
                    "source": d.metadata.get("source"),
                    "kind": d.metadata.get("kind"),
                    "score": float(s),
                    "snippet": d.page_content,
                }
                for d, s in filtered_hits[:TOP_K]
            ],
        }

    # -------------------------------------------------
    # GENERATIVE MODE (PROCEDURE OR EXPLANATION)
    # -------------------------------------------------

    context = "\n\n---\n\n".join(
        f"[Source: {d.metadata.get('source')} | Kind: {d.metadata.get('kind')}]\n"
        f"{d.page_content}"
        for d, _ in filtered_hits[:TOP_K]
    )

    prompt = f"""{BASE_PROMPT_TEXT}

Context:
{context}

Question:
{question}
"""

    answer = _call_llm(prompt)

    return {
        "answer": answer or "Not found in the provided documents.",
        "confidence": confidence,
        "retrieved": [
            {
                "source": d.metadata.get("source"),
                "kind": d.metadata.get("kind"),
                "score": float(s),
                "snippet": d.page_content,
            }
            for d, s in filtered_hits[:TOP_K]
        ],
    }
