# =========================
# codegen_agent_simple.py
# LLM with RAG over SPEC manual (PDFs)
# (Health checks removed; raw Ollama response printed)
# =========================

from __future__ import annotations
import os
from typing import Dict, Any, List, Tuple

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from scripts.load_drive_code import load_drive_docs   # <- your chunked PDF loader
from scripts.log_utils import log_stage  # keep logging, no health ping

from scripts.query_rewrite import rewrite_user_query
from scripts.log_utils import log_event 
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
                "snippet": (doc.page_content or "")[:300]
            }
            for doc, score in merged
        ]
    })
    return merged

# ---------------- Prompt ----------------
BASE_PROMPT = """
You are a domain expert in **SPEC** — the beamline control and data acquisition language developed by Certified Scientific Software (CSS). SPEC combines UNIX-style shell commands and a C-like macro system for controlling diffractometers, detectors, temperature stages, and other beamline devices.

# CONTEXT
SPEC is used for scripting complex experimental sequences through macros. It allows looping, motion control, scanning, and process automation. The syntax borrows C-like control structures and uses `def ... ' ... '` for macro definitions.

### Key Features
- Commands: UNIX-like commands (`mv`, `sleep`, `cd`, etc.) integrated with instrument actions (`ascan`, `mesh`, `tseries`, etc.)
- Control: `if ()`, `for ()`, `while ()` loops and arithmetic expressions
- IO: `printf`, `p`, `date`, `measuretemp`, `umv`, `flyscan`, `opens`, `closes`
- Detector control: `pil_on`, `pil_setdir`, `pil_settrig`
- File management: `u mkdir`, `eval()`, `sprintf()`
- User-defined parameters: `$1`, `$2`, ... for macro arguments

### Macros from SPEC Manual
- `def macroname ' statements '`: defines a macro
- `cdef("macroname", statements [, key [, flags]])`: extends existing macros
- `prdef macroname`: prints the macro’s definition
- `sleep time`: pauses execution
- `umv motor position`: move motor immediately
- `flyscan motor start stop steps time`: perform flyscan
- `if (condition) statement`
- `for (var=start; condition; increment) statement`
- `opens/closes`: open or close shutter
- `printf("text", vars...)` or `p var`
- `$1`, `$2` represent command-line arguments passed to a macro

### PURPOSE
You will be asked to write or transform SPEC macros (in `.mac` files like HDRMscans.mac) that automate data collection routines such as:
- temperature-dependent scans
- rocking curves
- multiple sample orientation scans
- automated looping over temperature or angle parameters

Use the valid SPEC constructs exactly as defined above.

# USER REQUEST
{task}

# OUTPUT REQUIREMENTS
- Output must be **only valid SPEC code**, following canonical macro style.
- Keep syntax fully compliant with SPEC standards from Certified Scientific Software manual.
- Use `def ... ' ... '` for macro definitions, not pseudocode or comments.
- Use `$1`, `$2`, etc. for macro parameters.
- When iterative or conditional logic is needed, use standard `for` or `while` loops.
- Do not invent new commands, functions, or syntax.
- Do not include comments, explanatory text, or markdown in output.

# REFERENCE EXAMPLE (from HDRMscans.mac)
def twotdepscan '
sortmypathout
_myT="$1"
te $1
sleep($2)
pil_on
eval(sprintf("u mkdir %s%s%s",_mysamplepath,_mysample,_myT))
sleep(5)
_pilrampath=_rampre _mysamplepath _mysample _myT
eval(sprintf("pil_setdir %s/",_pilrampath))
pil_settrig "Mult. Trigger"
umv chi 90 th 0 phi 0
opens
sleep(1)
flyscan phi 0 180 1800 .1
sleep(1)
closes
'

# STRICT RULES
- No English explanations.
- No comments or pseudocode.
- No markdown or code fences.
- Follow only the grammar and semantics of SPEC as documented by Certified Scientific Software (CSS).

# OUTPUT
SPEC macro code only.
"""


# ---------------- LLM Caller ----------------
def _call_llm(prompt: str) -> str:
    try:
        llm = ChatOllama(model=DEFAULT_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
        print(f"[DEBUG] Sending prompt to Ollama ({DEFAULT_MODEL})...")
        out = llm.invoke([{"role": "user", "content": prompt}])
        # Print raw return so your advisor can SEE traffic from Ollama:
        print(f"[DEBUG] Ollama raw response (CODE agent): {out}")
        return getattr(out, "content", str(out)) or ""
    except Exception as e:
        print(f"[code] LLM call error: {e}")
        return ""

# ---------------- Main Pipeline ----------------
# def run_codegen_ui(task: str) -> Dict[str, Any]:
#     vs = _build_vs()
#     hits = _search(task, vs, k=TOP_K)

def run_codegen_ui(task: str) -> Dict[str, Any]:
    # 1. rewrite the query before retrieval
    rewritten = rewrite_user_query(task)
    print(f"[DEBUG] Code Agent — Query rewritten: {task!r} → {rewritten!r}")

    #  Log the rewrite step
    log_event("query_rewrite", {
        "original_query": task,
        "rewritten_query": rewritten,
        "agent": "code",
        "confidence": 0.9
    })

    # 2. build vs and search with the rewritten query
    vs = _build_vs()
    # --- Lightweight query expansion for short or vague code requests ---
    # --- Stronger rewrite for code queries ---
    task_lower = task.strip().lower()

    if len(task_lower.split()) <= 4 and not any(
        x in task_lower for x in ["write", "code", "macro", "scan", "loop"]
    ):
        task = f"show example SPEC macro code demonstrating the usage of {task_lower}"

    elif any(x in task_lower for x in ["define", "explain", "macro"]):
        task = task_lower.replace("define", "show example SPEC macro code demonstrating the usage of")
        task = task.replace("explain", "show example SPEC macro code demonstrating the usage of")
        task = task.replace("macro", "macro using")

    hits = _search(rewritten, vs, k=TOP_K)

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

    # 3. use the rewritten query in the prompt too
    prompt = BASE_PROMPT.format(task=rewritten, manual=rag_blob)

    # --- Log prompt ---
    log_stage(task, "prompt", {
        "agent": "code",
        "prompt_chars": len(prompt),
        "prompt_preview": prompt[:200]
    })

    # --- Call LLM directly (no health check) ---
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
