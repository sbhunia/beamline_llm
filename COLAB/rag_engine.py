"""
rag_engine.py – Dual-index RAG backend (Markdown + PDF)

Two separate FAISS indexes with different chunking strategies:
  • MD index  – small chunks (chunk_size=300, overlap=150)  ← precise for FAQ/command lookups
  • PDF index – larger chunks (chunk_size=1000, overlap=300) ← for manuals
"""

from __future__ import annotations

import os
import hashlib
from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document

# CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_DIR   = os.path.join(BASE_DIR, "md_files")
PDF_DIR  = os.path.join(BASE_DIR, "pdf_files")

FAISS_MD  = os.path.join(BASE_DIR, "faiss_index_md")
FAISS_PDF = os.path.join(BASE_DIR, "faiss_index_pdf")

EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"

TOP_K_MD          = 8    # was 6 — grab more MD hits for command lookups
TOP_K_PDF         = 6
MAX_CONTEXT_CHUNKS = 12  # was 10

os.environ.setdefault("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY", ""))

# CHUNKING  –  RESTORED to the values that worked

MD_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=300,        # ← was incorrectly bumped to 800; small = precise
    chunk_overlap=150,
    separators=["\n######", "\n#####", "\n####", "\n###", "\n##", "\n#", "\n\n", "\n", " "],
)

PDF_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
    separators=["\n\n", "\n", ". ", " "],
)

# EMBEDDINGS  (singleton) 

_embeddings = None

def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMB_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"batch_size": 32},
        )
    return _embeddings

# LOADERS

def _load_md_docs() -> List[Document]:
    documents: List[Document] = []
    md_path = Path(MD_DIR)
    if not md_path.exists():
        print(f"[WARNING] MD directory not found: {MD_DIR}")
        return documents

    for fp in sorted(md_path.rglob("*.md")):
        try:
            loader = TextLoader(str(fp), encoding="utf-8")
            docs = loader.load()
            for d in docs:
                d.metadata["source"]   = fp.name
                d.metadata["doc_type"] = "markdown"
            documents.extend(docs)
        except Exception as e:
            print(f"[WARNING] Failed to load {fp.name}: {e}")

    print(f"[INFO] Loaded {len(documents)} markdown documents")
    return documents


def _load_pdf_docs() -> List[Document]:
    documents: List[Document] = []
    pdf_path = Path(PDF_DIR)
    if not pdf_path.exists():
        print(f"[WARNING] PDF directory not found: {PDF_DIR}")
        return documents

    for fp in sorted(pdf_path.rglob("*.pdf")):
        try:
            loader = PyPDFLoader(str(fp))
            docs = loader.load()
            for d in docs:
                d.metadata["source"]   = fp.name
                d.metadata["doc_type"] = "pdf"
            documents.extend(docs)
            print(f"[INFO] Loaded {fp.name} ({len(docs)} pages)")
        except Exception as e:
            print(f"[WARNING] Failed to load {fp.name}: {e}")

    print(f"[INFO] Loaded {len(documents)} total PDF pages")
    return documents

# BUILD / LOAD INDEX 

def _build_or_load(index_path: str, loader_fn, splitter) -> FAISS | None:
    embeddings = _get_embeddings()

    if os.path.exists(os.path.join(index_path, "index.faiss")):
        print(f"[INFO] Loading existing index from {index_path}")
        return FAISS.load_local(
            index_path, embeddings, allow_dangerous_deserialization=True
        )

    raw_docs = loader_fn()
    if not raw_docs:
        print(f"[WARNING] No documents found for {index_path} — skipping")
        return None

    chunks = splitter.split_documents(raw_docs)
    print(f"[INFO] {index_path}: {len(raw_docs)} docs → {len(chunks)} chunks")

    store = FAISS.from_documents(chunks, embeddings)
    os.makedirs(index_path, exist_ok=True)
    store.save_local(index_path)
    return store


_store_md:  FAISS | None = None
_store_pdf: FAISS | None = None
_loaded = False


def _ensure_stores():
    global _store_md, _store_pdf, _loaded
    if _loaded:
        return
    _store_md  = _build_or_load(FAISS_MD,  _load_md_docs,  MD_SPLITTER)
    _store_pdf = _build_or_load(FAISS_PDF, _load_pdf_docs, PDF_SPLITTER)
    _loaded = True

# RETRIEVAL 

def _hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def retrieve(query: str):
    _ensure_stores()

    results = []
    if _store_md:
        results += _store_md.similarity_search_with_score(query, k=TOP_K_MD)
    if _store_pdf:
        results += _store_pdf.similarity_search_with_score(query, k=TOP_K_PDF)

    # Deduplicate by content hash, keep best (lowest) score
    seen: dict = {}
    for doc, score in results:
        h = _hash(doc.page_content)
        if h not in seen or score < seen[h][1]:
            seen[h] = (doc, score)

    ranked = sorted(seen.values(), key=lambda x: x[1])
    return ranked[:MAX_CONTEXT_CHUNKS]

# SYSTEM PROMPT 

SYSTEM_PROMPT = """
You are a technical assistant for a synchrotron beamline control system (CHESS QM2).

Use ONLY the provided context to answer questions.

RULES:
1. Provide a direct, complete answer to the question.
2. If the context contains a command or macro explanation → explain what it does clearly,
   including its syntax and any relevant examples from the context.
3. If the context contains direct instructions or steps → list ALL steps clearly
   AND preserve the EXACT order they appear. Do NOT skip steps.
4. If the context contains related links or resources but no step-by-step instructions →
   explain what information is available and point to the relevant links.
5. If a table is present in the context that answers the question → reproduce the
   FULL table including ALL columns. Do not omit any columns.
6. If the user's question contains conditions that conflict with the document
   (e.g., invalid temperature ranges or operating modes), explicitly point out the
   mismatch BEFORE listing any steps.
7. If a command or macro is mentioned in the context, ALWAYS explain:
   - What it does
   - Its syntax / arguments
   - Any example usages shown in the context

IMPORTANT:
- Do NOT reorder, optimize, or reinterpret step sequences.
- Do NOT omit information that is present in the context.
- Do NOT say "not found" if the information IS present — read the context carefully.
- If truly nothing relevant is present, say: "Not found in the provided documents."
- Do NOT invent steps, commands, or procedures.

At the end of your answer, list the source documents you referenced:
**Sources:** filename1, filename2
"""

# MAIN RAG FUNCTION

def ask_rag(query: str) -> str:
    results = retrieve(query)

    if not results:
        return "Not found in the provided documents."

    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')} | "
        f"Type: {doc.metadata.get('doc_type', '?')}]\n{doc.page_content}"
        for doc, _ in results
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,   # ← restored to 0 for deterministic, precise answers
        max_retries=5,
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}"),
        ]
    )

    return response.content

# REBUILD  (called from sidebar button in app.py)

def rebuild_indexes():
    import shutil

    for p in [FAISS_MD, FAISS_PDF]:
        if os.path.exists(p):
            shutil.rmtree(p)
            print(f"[INFO] Deleted {p}")

    global _loaded
    _loaded = False
    _ensure_stores()
    print("[INFO] Rebuild complete.")


if __name__ == "__main__":
    rebuild_indexes()
    print(ask_rag("What does te 300 mean?"))
    print(ask_rag("How do I change the energy?"))