from __future__ import annotations
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd

DATA_DIR = os.getenv("DRIVE_DIR", "/home/vallurs/research/data/drive_docs")

def _pdf_paths(folder: str) -> List[str]:
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(".pdf")
    ]

def load_drive_docs(chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    docs: List[Document] = []

    # ---------------- Load PDFs ----------------
    pdf_paths = _pdf_paths(DATA_DIR)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    for path in pdf_paths:
        try:
            loader = PyPDFLoader(path)
            pages = loader.load()
            full_text = "\n\n".join(_normalize_text(d.page_content or "") for d in pages)
            for chunk in text_splitter.split_text(full_text):
                docs.append(Document(page_content=chunk, metadata={"source": os.path.basename(path)}))
        except Exception as e:
            print(f"[DEBUG] Failed to load {path}: {e}")

    # ---------------- Load Tables (XLSX + CSV) ----------------
    for f in os.listdir(DATA_DIR):
        fpath = os.path.join(DATA_DIR, f)
        if not os.path.isfile(fpath):
            continue

        try:
            if f.lower().endswith(".xlsx"):
                df = pd.read_excel(fpath, dtype=str).fillna("")
            elif f.lower().endswith(".csv"):
                df = pd.read_csv(fpath, dtype=str, encoding="utf-8").fillna("")
            else:
                continue

            for i, row in df.iterrows():
                row_text = " | ".join(str(row[col]).strip() for col in df.columns if str(row[col]).strip())
                if row_text:
                    docs.append(Document(
                        page_content=row_text,
                        metadata={"source": f"TABLE::{f}"}
                    ))
            print(f"[DEBUG] Loaded {len(df)} rows from table: {f}")

        except Exception as e:
            print(f"[DEBUG] Failed to load table {f}: {e}")

    print(f"[DEBUG] Total docs loaded for TEXT AGENT: {len(docs)}")
    return docs

def _normalize_text(txt: str) -> str:
    return (
        txt.replace("\r\n", "\n")
           .replace("\r", "\n")
           .replace("\u2018", "'")
           .replace("\u2019", "'")
           .replace("\u201C", '"')
           .replace("\u201D", '"')
           .replace("\t", " ")
           .strip()
    )

