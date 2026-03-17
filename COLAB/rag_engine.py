# import os
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import SystemMessage, HumanMessage

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MD_DIR = os.path.join(BASE_DIR, "md_files")
# FAISS_PATH = os.path.join(BASE_DIR, "faiss_index11")

# EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
# TOP_K = 8

# # Gemini key from environment (Streamlit Secrets)
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# # ============================================================
# # BUILD / LOAD VECTORSTORE
# def build_or_load_vectorstore():
#     embeddings = HuggingFaceEmbeddings(
#         model_name=EMB_MODEL,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"batch_size": 32}
#     )

#     if os.path.exists(FAISS_PATH):
#         return FAISS.load_local(
#             FAISS_PATH,
#             embeddings,
#             allow_dangerous_deserialization=True
#         )

#     documents = []
#     for root, _, files in os.walk(MD_DIR):
#         for file in files:
#             if file.endswith(".md"):
#                 loader = TextLoader(os.path.join(root, file), encoding="utf-8")
#                 docs = loader.load()
#                 for d in docs:
#                     d.metadata["source"] = os.path.relpath(
#                         os.path.join(root, file), MD_DIR
#                     )
#                 documents.extend(docs)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=250,
#         chunk_overlap=150,
#     )

#     chunks = splitter.split_documents(documents)
#     vectorstore = FAISS.from_documents(chunks, embeddings)
#     vectorstore.save_local(FAISS_PATH)
#     return vectorstore


# VECTORSTORE = build_or_load_vectorstore()


# def ask_rag(query: str) -> str:
#     results = VECTORSTORE.similarity_search_with_score(query, k=TOP_K)

#     context = "\n\n---\n\n".join(
#         f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
#         for doc, _ in results
#     )

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         temperature=0.5,
#         max_retries=5,
#     )

#     system_prompt = """
# You are a technical assistant for a synchrotron beamline control system.

# Use ONLY the provided context.

# If the context contains:
# - direct instructions or steps → list all steps clearly AND preserve the EXACT order they appear.
# - related links or resources but no step-by-step instructions →
#   explain what information is available and point to the relevant links.
# - If the source contains a table, reproduce the full table including all columns. Do not omit columns.

# IMPORTANT:
# - Do NOT reorder, optimize, or reinterpret step sequences.
# - If the user’s question contains conditions that conflict with the document
#   (e.g., invalid temperature ranges or operating modes),
#   explicitly point out the mismatch BEFORE listing any steps.

# If nothing relevant is present at all, say:
# "Not found in the provided documents."

# Do NOT invent steps or procedures.
# """

#     response = llm.invoke(
#         [
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}")
#         ]
#     )

#     return response.content

######## ABOVE IS WORKING RAG ENGINE FOR ONLY MD FILES.

# import os
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_community.document_loaders import TextLoader, DirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import SystemMessage, HumanMessage

# # 1. API & PATH CONFIG
# load_dotenv()
# if "GOOGLE_API_KEY" in st.secrets:
#     os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
# else:
#     st.error("API key not found in Streamlit secrets")

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MD_DIR = os.path.join(BASE_DIR, "md_files")
# FAISS_PATH = os.path.join(BASE_DIR, "faiss_index_gemini")

# # TECHNICAL SPECS (Matches your Ollama configuration)
# EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
# TOP_K = 5
# CHUNK_SIZE = 400
# CHUNK_OVERLAP = 200
# TEMPERATURE = 0.0

# # 2. VECTORSTORE LOGIC
# @st.cache_resource
# def get_vectorstore():
#     embeddings = HuggingFaceEmbeddings(
#         model_name=EMB_MODEL,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"batch_size": 32}
#     )
    
#     if os.path.exists(FAISS_PATH):
#         return FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

#     # Load all MD files
#     loader = DirectoryLoader(MD_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
#     documents = loader.load()

#     # Exact metadata logic for sources
#     for d in documents:
#         d.metadata["source_file"] = os.path.basename(d.metadata["source"])
#         d.metadata["full_path"] = d.metadata["source"]

#     # Exact Chunking Specs
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=CHUNK_SIZE,
#         chunk_overlap=CHUNK_OVERLAP
#     )
#     chunks = splitter.split_documents(documents)
    
#     vectorstore = FAISS.from_documents(chunks, embeddings)
#     vectorstore.save_local(FAISS_PATH)
#     return vectorstore

# VECTORSTORE = get_vectorstore()

# # 3. QUERY FUNCTION
# def ask_rag(query: str):
#     # Similarity Search
#     results = VECTORSTORE.similarity_search_with_score(query, k=TOP_K)
    
#     # Context Construction
#     context = "\n\n---\n\n".join([
#         f"[Source: {doc.metadata.get('source_file')}]\n{doc.page_content}"
#         for doc, score in results
#     ])

#     # Gemini Model Setup (with max_retries as requested)
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=TEMPERATURE,
#         max_retries=5
#     )
    
#     system_prompt = """
#         You are a technical assistant for a synchrotron beamline control system.

#         Use ONLY the provided context.

#         RULES:

#         Provide a direct answer to the question.

#         Do not include information or tables that are unrelated to the specific question asked.

#         If the context contains direct instructions → list only what is available.

#         For multiple steps → list all steps clearly AND preserve the EXACT order they appear.

#         If the context contains related links but no steps → explain available info and point to links.

#         If a table contains the specific answer requested → reproduce the full table.

#         IMPORTANT:

#         Do NOT reorder or reinterpret steps.

#         If nothing relevant is present at all, say: Not found in the provided documents.

#         Do NOT invent steps or procedures.
#         """

#     response = llm.invoke([
#         SystemMessage(content=system_prompt),
#         HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}")
#     ])

#     # Returning dictionary for app.py evaluation compatibility
#     return {
#         "answer": response.content.strip(),
#         "retrieved": [
#             {
#                 "content": doc.page_content,
#                 "source_file": doc.metadata.get("source_file"),
#                 "score": float(score),
#                 "full_path": doc.metadata.get("full_path")
#             } for doc, score in results
#         ]
#     }

""" CLAUDEEEEE MD FILES + PDFS
rag_engine.py – Dual-index RAG backend (Markdown + PDF)

Two separate FAISS indexes with different chunking strategies:
  • MD index  – small chunks (chunk_size=300, overlap=150)
               Markdown files are short, command-heavy docs. Small chunks
               keep individual commands/steps isolated for precise retrieval.
  • PDF index – larger chunks (chunk_size=1000, overlap=300)
               PDFs are dense technical manuals (up to 317 pages). Larger
               chunks preserve the surrounding context needed to understand
               procedures, tables, and specifications.

Both indexes are queried in parallel; results are merged and deduplicated
by content before being sent to Gemini.
"""

from __future__ import annotations

import os
import hashlib
from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.documents import Document

# =====================================================================
# CONFIGURATION
# =====================================================================

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MD_DIR     = os.path.join(BASE_DIR, "md_files")
PDF_DIR    = os.path.join(BASE_DIR, "pdf_files")

FAISS_MD   = os.path.join(BASE_DIR, "faiss_index_md")
FAISS_PDF  = os.path.join(BASE_DIR, "faiss_index_pdf")

EMB_MODEL  = "sentence-transformers/all-mpnet-base-v2"

# Retrieval depth per index
TOP_K_MD   = 6
TOP_K_PDF  = 6

# Final merged results sent to LLM (after dedup + re-rank by score)
MAX_CONTEXT_CHUNKS = 10

# Gemini key – loaded from env / Streamlit secrets
os.environ.setdefault("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY", ""))

# =====================================================================
# CHUNKING STRATEGIES
# =====================================================================

MD_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=150,
    separators=["\n######", "\n####", "\n###", "\n##", "\n#", "\n\n", "\n", " "],
)

PDF_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
    separators=["\n\n", "\n", ". ", " "],
)

# =====================================================================
# EMBEDDINGS (cached at module level)
# =====================================================================

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

# =====================================================================
# DOCUMENT LOADERS
# =====================================================================

def _load_md_docs() -> List[Document]:
    """Load all .md files from MD_DIR."""
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
                d.metadata["source"] = fp.name
                d.metadata["doc_type"] = "markdown"
            documents.extend(docs)
        except Exception as e:
            print(f"[WARNING] Failed to load {fp.name}: {e}")

    print(f"[INFO] Loaded {len(documents)} markdown documents")
    return documents


def _load_pdf_docs() -> List[Document]:
    """Load all .pdf files from PDF_DIR."""
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
                d.metadata["source"] = fp.name
                d.metadata["doc_type"] = "pdf"
            documents.extend(docs)
            print(f"[INFO] Loaded {fp.name} ({len(docs)} pages)")
        except Exception as e:
            print(f"[WARNING] Failed to load {fp.name}: {e}")

    print(f"[INFO] Loaded {len(documents)} total PDF pages")
    return documents

# =====================================================================
# BUILD / LOAD VECTORSTORES
# =====================================================================

def _build_or_load(
    index_path: str,
    loader_fn,
    splitter: RecursiveCharacterTextSplitter,
    label: str,
) -> FAISS | None:
    """Build a FAISS index from scratch or load an existing one."""
    embeddings = _get_embeddings()

    if os.path.exists(os.path.join(index_path, "index.faiss")):
        print(f"[INFO] Loading existing {label} index from {index_path}")
        return FAISS.load_local(
            index_path, embeddings, allow_dangerous_deserialization=True
        )

    raw_docs = loader_fn()
    if not raw_docs:
        print(f"[WARNING] No documents found for {label} – skipping index build")
        return None

    chunks = splitter.split_documents(raw_docs)
    print(f"[INFO] {label}: {len(raw_docs)} docs → {len(chunks)} chunks")

    store = FAISS.from_documents(chunks, embeddings)
    os.makedirs(index_path, exist_ok=True)
    store.save_local(index_path)
    print(f"[INFO] {label} index saved to {index_path}")
    return store

# Global stores – initialised lazily
_store_md: FAISS | None  = None
_store_pdf: FAISS | None = None
_stores_loaded = False


def _ensure_stores():
    global _store_md, _store_pdf, _stores_loaded
    if _stores_loaded:
        return
    _store_md  = _build_or_load(FAISS_MD,  _load_md_docs,  MD_SPLITTER,  "Markdown")
    _store_pdf = _build_or_load(FAISS_PDF, _load_pdf_docs, PDF_SPLITTER, "PDF")
    _stores_loaded = True

# =====================================================================
# RETRIEVAL  (query both indexes, merge & deduplicate)
# =====================================================================

def _content_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def retrieve(query: str) -> List[Tuple[Document, float]]:
    """Retrieve from both indexes, merge, deduplicate, sort by score."""
    _ensure_stores()

    all_results: List[Tuple[Document, float]] = []

    if _store_md is not None:
        md_hits = _store_md.similarity_search_with_score(query, k=TOP_K_MD)
        all_results.extend(md_hits)

    if _store_pdf is not None:
        pdf_hits = _store_pdf.similarity_search_with_score(query, k=TOP_K_PDF)
        all_results.extend(pdf_hits)

    # Deduplicate by content hash
    seen: dict[str, Tuple[Document, float]] = {}
    for doc, score in all_results:
        h = _content_hash(doc.page_content)
        if h not in seen or score < seen[h][1]:   # lower score = closer match
            seen[h] = (doc, score)

    # Sort by relevance (ascending distance) and cap
    ranked = sorted(seen.values(), key=lambda x: x[1])
    return ranked[:MAX_CONTEXT_CHUNKS]

# =====================================================================
# PROMPT
# =====================================================================

SYSTEM_PROMPT = """
You are a technical assistant for a synchrotron beamline control system (CHESS QM2).

Use ONLY the provided context to answer questions.

RULES:
- Provide a direct answer to the question.
- Do not include information or tables that are unrelated to the specific question asked.
- If the context contains direct instructions or steps → list all steps clearly
  AND preserve the EXACT order they appear.
- If the context contains related links or resources but no step-by-step instructions →
  explain what information is available and point to the relevant links.
- If a table is present in the context that answers the question → reproduce the
  full table including all columns. Do not omit columns.
- If the user's question contains conditions that conflict with the document
  (e.g., invalid temperature ranges or operating modes), explicitly point out the
  mismatch BEFORE listing any steps.

IMPORTANT:
- Do NOT reorder, optimize, or reinterpret step sequences.
- If nothing relevant is present at all, say:
  "Not found in the provided documents."
- Do NOT invent steps or procedures.

At the end of your answer, list the source documents you referenced, like:
**Sources:** filename1, filename2
"""

# =====================================================================
# PUBLIC INTERFACE
# =====================================================================

def ask_rag(query: str) -> str:
    """Run the full RAG pipeline: retrieve → build prompt → call Gemini."""

    results = retrieve(query)

    if not results:
        return "Not found in the provided documents."

    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')} | "
        f"Type: {doc.metadata.get('doc_type', '?')}]\n{doc.page_content}"
        for doc, _ in results
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.3,
        max_retries=5,
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}"),
        ]
    )

    return response.content


# =====================================================================
# UTILITY: force re-index (call from terminal or a sidebar button)
# =====================================================================

def rebuild_indexes():
    """Delete existing indexes and rebuild from source files."""
    import shutil

    for p in [FAISS_MD, FAISS_PDF]:
        if os.path.exists(p):
            shutil.rmtree(p)
            print(f"[INFO] Deleted {p}")

    global _stores_loaded
    _stores_loaded = False
    _ensure_stores()
    print("[INFO] Rebuild complete.")


if __name__ == "__main__":
    # Quick sanity check from the command line
    rebuild_indexes()
    answer = ask_rag("How do I change the energy?")
    print("\n===== ANSWER =====")
    print(answer)