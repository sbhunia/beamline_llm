from __future__ import annotations
import os, re
from typing import List, Tuple, Dict, Any

from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.documents import Document

from scripts.load_markdown import load_markdown_docs
from scripts.load_drive import load_drive_docs
from scripts.load_website import load_website

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
TEXT_MODEL = os.getenv("TEXT_MODEL", "mistral:latest")
WEBSITE_URL = os.getenv("WEBSITE_URL", "https://suchismitasarker.github.io/CHESS-ID4B-QM2/")

def _build_vs(beamline: bool) -> Qdrant:
    docs: List[Document] = []
    docs += load_drive_docs()
    docs += load_markdown_docs()
    if not beamline:
        try:
            docs += load_website(WEBSITE_URL)
        except Exception as e:
            print("Skipping website due to error:", e)
    # normalize quotes for consistency
    for d in docs:
        if isinstance(d.page_content, str):
            d.page_content = (d.page_content
                              .replace("\u2018", "'").replace("\u2019", "'")
                              .replace("\u201C", '"').replace("\u201D", '"'))
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = Qdrant.from_documents(docs, emb, location=":memory:", collection_name="text-docs")
    return vs

def answer(query: str, beamline: bool = True) -> Tuple[str, List[Tuple[str, str]], Dict[str, Any]]:
    """Return (answer_text, citations, debug). Always triple to avoid unpack issues."""
    vs = _build_vs(beamline=beamline)
    hits = vs.similarity_search_with_score(query, k=8)
    if not hits:
        return "I don’t see that in the provided documents.", [], {"k": 8, "top": []}

    cites: List[Tuple[str, str]] = []
    snippets: List[str] = []
    top_dbg = []
    for doc, score in hits:
        txt = (doc.page_content or "").strip()
        preview = re.sub(r"\s+", " ", txt)[:500]
        src = doc.metadata.get("source", "unknown")
        cites.append((src, preview))
        snippets.append(preview)
        top_dbg.append({"src": src, "score": float(score)})

    llm = ChatOllama(model=TEXT_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
    prompt = (
        "Answer ONLY using the excerpts below. If they don't contain the answer, reply exactly:\n"
        "\"I don’t see that in the provided documents.\"\n\n"
        f"QUESTION:\n{query}\n\nEXCERPTS:\n\n" + "\n\n---\n\n".join(snippets)
    )
    raw = getattr(llm.invoke([{"role": "user", "content": prompt}]), "content", "")
    text = raw.strip()

    # guardrail: if model tries to prepend an answer then that line, prefer the answer if it's longer
    if "I don’t see that in the provided documents." in text and len(text) > len("I don’t see that in the provided documents.") + 20:
        text = re.sub(r"^I don’t see that in the provided documents\.\s*", "", text).strip()

    return text, cites, {"k": 8, "top": top_dbg}
