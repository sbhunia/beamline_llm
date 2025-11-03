from __future__ import annotations
import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd

# Directories
PRIMARY_DIR = os.getenv("DRIVE_DIR", "/home/vallurs/research/data/drive_docs_code")
SECONDARY_DIR = "/home/vallurs/research/data/drive_docs"  # shared folder for tables
MACRO_DIR = "/home/vallurs/research/data/mac_docs"         # your local .mac directory

def _collect_paths(folder: str, ext: str) -> List[str]:
    if not os.path.isdir(folder):
        return []
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(ext)
    ]

def _normalize_text(txt: str) -> str:
    return (
        txt.replace("\u2018", "'")
           .replace("\u2019", "'")
           .replace("\u201C", '"')
           .replace("\u201D", '"')
           .replace("\n", " ")
           .replace("\t", " ")
           .strip()
    )

def load_drive_docs(chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    docs: List[Document] = []
    folders = [PRIMARY_DIR, SECONDARY_DIR]

    # ---------------- PDF loading ----------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    for folder in folders:
        pdf_paths = _collect_paths(folder, ".pdf")
        for path in pdf_paths:
            try:
                loader = PyPDFLoader(path)
                pages = loader.load()
                full_text = "\n\n".join(_normalize_text(d.page_content or "") for d in pages)
                chunks = text_splitter.split_text(full_text)
                for chunk in chunks:
                    docs.append(Document(page_content=chunk, metadata={"source": os.path.basename(path)}))
                print(f"[DEBUG] Loaded {len(chunks)} chunks from {os.path.basename(path)} in {folder}")
            except Exception as e:
                print(f"[DEBUG] Failed to load {path}: {e}")

    # ---------------- Table loading (XLSX + CSV) ----------------
    for folder in folders:
        for f in os.listdir(folder):
            fpath = os.path.join(folder, f)
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

                print(f"[DEBUG] Loaded {len(df)} rows from table: {f} in {folder}")

            except Exception as e:
                print(f"[DEBUG] Failed to load table {f}: {e}")

    # ---------------- MAC file loading ----------------
    if os.path.isdir(MACRO_DIR):
        mac_paths = _collect_paths(MACRO_DIR, ".mac")
        for path in mac_paths:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = _normalize_text(f.read())
                # You can optionally split long .mac files into smaller logical chunks
                chunks = text_splitter.split_text(content)
                for chunk in chunks:
                    docs.append(Document(
                        page_content=chunk,
                        metadata={"source": os.path.basename(path)}
                    ))
                print(f"[DEBUG] Loaded {len(chunks)} chunks from {os.path.basename(path)} in {MACRO_DIR}")
            except Exception as e:
                print(f"[DEBUG] Failed to load {path}: {e}")
    else:
        print(f"[DEBUG] MACRO_DIR not found: {MACRO_DIR}")

    print(f"[DEBUG] Total docs loaded for CODE AGENT: {len(docs)}")
    return docs
