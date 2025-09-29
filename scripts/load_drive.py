from __future__ import annotations
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = os.getenv("DRIVE_DIR", "/home/vallurs/research/data/drive_docs")

def _pdf_paths() -> List[str]:
    if not os.path.isdir(DATA_DIR):
        print(f"Directory {DATA_DIR} does not exist!")
        return []
    return [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if os.path.isfile(os.path.join(DATA_DIR, f)) and f.lower().endswith(".pdf")
    ]

def load_drive_docs(chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Load PDFs and split into overlapping text chunks.
    Each Document = one chunk of text (not one page).
    """
    docs: List[Document] = []
    pdf_paths = _pdf_paths()
    
    if not pdf_paths:
        print(f"No PDFs found in {DATA_DIR}. Creating dummy document.")
        return [Document(
            page_content="SPEC is a powerful macro language for instrument control and data acquisition.",
            metadata={"source": "dummy.pdf"}
        )]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    for path in pdf_paths:
        try:
            loader = PyPDFLoader(path)
            pages = loader.load()  # still gives per-page docs
            # Merge into one doc for splitting
            full_text = "\n\n".join(_normalize_text(d.page_content or "") for d in pages)
            
            # Split into chunks
            chunks = text_splitter.split_text(full_text)
            chunk_docs = [
                Document(
                    page_content=chunk,
                    metadata={"source": os.path.basename(path)}
                )
                for chunk in chunks
            ]
            docs.extend(chunk_docs)
            print(f"Loaded {len(chunk_docs)} chunks from {os.path.basename(path)}")
        except Exception as e:
            print(f"Failed to load {path}: {e}")

    print(f"Final total: {len(docs)} documents")
    return docs

def _normalize_text(txt: str) -> str:
    return (
        txt.replace("\u2018", "'").replace("\u2019", "'")
           .replace("\u201C", '"').replace("\u201D", '"')
           .strip()
    )
