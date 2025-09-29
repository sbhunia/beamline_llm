from __future__ import annotations
import os
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_URL = os.getenv("WEBSITE_URL", "https://suchismitasarker.github.io/CHESS-ID4B-QM2/")

def load_website(url: str = DEFAULT_URL) -> List[Document]:
    """
    Load website documentation, split semantically into chunks.
    """
    loader = WebBaseLoader(url)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " "],  # HTML often has small sections
        chunk_size=1000,
        chunk_overlap=120,
        length_function=len,
    )

    chunks: List[Document] = []
    for d in docs:
        d.metadata = d.metadata or {}
        d.metadata["source"] = url
        parts = splitter.split_text(d.page_content or "")
        for c in parts:
            chunks.append(Document(
                page_content=_normalize_text(c),
                metadata=dict(d.metadata)
            ))
    return chunks

def _normalize_text(txt: str) -> str:
    return (
        txt.replace("\u2018", "'").replace("\u2019", "'")
           .replace("\u201C", '"').replace("\u201D", '"')
           .strip()
    )
