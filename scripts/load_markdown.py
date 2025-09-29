from __future__ import annotations
import os, glob
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = os.getenv("MARKDOWN_DIR", "data/markdown_docs")

def load_markdown_docs() -> List[Document]:
    """
    Load markdown documentation, split semantically into chunks.
    """
    paths = glob.glob(os.path.join(DATA_DIR, "**/*.md"), recursive=True)
    docs: List[Document] = []
    for path in paths:
        loader = TextLoader(path, encoding="utf-8")
        parts = loader.load()
        for d in parts:
            d.metadata = d.metadata or {}
            d.metadata["source"] = os.path.basename(path)
        docs.extend(parts)

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n# ", "\n\n", "\n", ". ", " "],  # respect markdown sections
        chunk_size=1000,
        chunk_overlap=120,
        length_function=len,
    )

    chunks: List[Document] = []
    for d in docs:
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
