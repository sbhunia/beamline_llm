from __future__ import annotations

import os
import re
from typing import List
import pandas as pd

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ---------------- Paths ----------------
PRIMARY_DIR = os.getenv("DRIVE_DIR", "/home/vallurs/research/data/drive_docs_code")
SECONDARY_DIR = "/home/vallurs/research/data/drive_docs"
MACRO_DIR = "/home/vallurs/research/data/mac_docs"

# ---------------- Helpers ----------------

def _collect_paths(folder: str, ext: str) -> List[str]:
    if not os.path.isdir(folder):
        return []
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(ext)
    ]

def _normalize_text(txt: str) -> str:
    """
    IMPORTANT:
    - Preserve newlines (SPEC syntax depends on them)
    - Normalize quotes only
    """
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

def split_spec_macros(text: str) -> List[str]:
    """
    Split SPEC .mac files so that EACH macro (def ...) is one chunk.
    """
    blocks = re.split(r'(?=\bdef\s+[A-Za-z_]\w*\s*\')', text)
    return [b.strip() for b in blocks if len(b.strip()) > 50]

# ---------------- Main Loader ----------------

def load_drive_docs(
    chunk_size: int = 400,
    chunk_overlap: int = 80
) -> List[Document]:

    docs: List[Document] = []
    folders = [PRIMARY_DIR, SECONDARY_DIR]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    # ---------------- PDF LOADING ----------------
    for folder in folders:
        pdf_paths = _collect_paths(folder, ".pdf")
        for path in pdf_paths:
            try:
                loader = PyPDFLoader(path)
                pages = loader.load()

                for page in pages:
                    text = _normalize_text(page.page_content or "")
                    chunks = text_splitter.split_text(text)

                    for chunk in chunks:
                        docs.append(Document(
                            page_content=chunk,
                            metadata={
                                "source": os.path.basename(path),
                                "kind": "manual",
                                "page": page.metadata.get("page")
                            }
                        ))

                print(f"[DEBUG] Loaded PDF: {os.path.basename(path)}")

            except Exception as e:
                print(f"[DEBUG] Failed PDF {path}: {e}")

    # ---------------- TABLE LOADING ----------------
    for folder in folders:
        if not os.path.isdir(folder):
            continue

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

                for _, row in df.iterrows():
                    row_text = " | ".join(
                        str(row[col]).strip()
                        for col in df.columns
                        if str(row[col]).strip()
                    )
                    if row_text:
                        docs.append(Document(
                            page_content=row_text,
                            metadata={
                                "source": f"TABLE::{f}",
                                "kind": "table"
                            }
                        ))

                print(f"[DEBUG] Loaded table: {f}")

            except Exception as e:
                print(f"[DEBUG] Failed table {f}: {e}")

    # ---------------- MACRO FILE LOADING (CRITICAL FIX) ----------------
    if os.path.isdir(MACRO_DIR):
        mac_paths = _collect_paths(MACRO_DIR, ".mac")

        for path in mac_paths:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = _normalize_text(f.read())

                macro_blocks = split_spec_macros(content)

                for block in macro_blocks:
                    docs.append(Document(
                        page_content=block,
                        metadata={
                            "source": os.path.basename(path),
                            "kind": "macro"
                        }
                    ))

                print(f"[DEBUG] Loaded {len(macro_blocks)} macros from {os.path.basename(path)}")

            except Exception as e:
                print(f"[DEBUG] Failed MAC file {path}: {e}")
    else:
        print(f"[DEBUG] MACRO_DIR not found: {MACRO_DIR}")

    print(f"[DEBUG] TOTAL DOCS LOADED (CODE AGENT): {len(docs)}")
    return docs
