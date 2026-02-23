import os
import pandas as pd
from typing import List
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
)

# =====================================================
# CONFIG
# =====================================================

DOCUMENTS_PATH = "/home/vallurs/research/data/md_files"
EXTRA_PDF_PATH = "/home/vallurs/research/data/drive_docs"

FAISS_CONFIGS = [
("/home/vallurs/research/COLAB/faiss_cs100_ov50", 100, 50),
("/home/vallurs/research/COLAB/faiss_cs200_ov100", 200, 100),
("/home/vallurs/research/COLAB/faiss_cs300_ov150", 300, 150),
("/home/vallurs/research/COLAB/faiss_cs500_ov250", 500, 250),
("/home/vallurs/research/COLAB/faiss_cs800_ov200", 800, 200),
("/home/vallurs/research/COLAB/faiss_cs1000_ov500", 1000, 500),
("/home/vallurs/research/COLAB/faiss_cs2000_ov800", 2000, 800),
]

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# =====================================================
# LOAD DOCUMENTS
# =====================================================

def load_documents() -> List[Document]:

    print("\n==============================")
    print("STARTING DOCUMENT LOADING")
    print("==============================")

    docs = []

    # -------- Markdown --------
    if Path(DOCUMENTS_PATH).exists():
        print(f"Loading markdown from: {DOCUMENTS_PATH}")
        md_loader = DirectoryLoader(
            DOCUMENTS_PATH,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
        )
        md_docs = md_loader.load()
        print(f"Loaded {len(md_docs)} markdown documents")
        docs.extend(md_docs)
    else:
        print("Markdown folder not found")

    # -------- PDFs (Main) --------
    if Path(DOCUMENTS_PATH).exists():
        pdf_files_main = list(Path(DOCUMENTS_PATH).rglob("*.pdf"))
        print(f"Found {len(pdf_files_main)} PDFs in main folder")

        for pdf in pdf_files_main:
            print(f"Loading PDF: {pdf}")
            loader = PyPDFLoader(str(pdf))
            pdf_docs = loader.load()
            print(f"  -> {len(pdf_docs)} pages loaded")
            docs.extend(pdf_docs)

    # -------- Extra Folder --------
    if Path(EXTRA_PDF_PATH).exists():

        print(f"\nLoading from extra folder: {EXTRA_PDF_PATH}")

        # PDFs
        pdf_files_extra = list(Path(EXTRA_PDF_PATH).rglob("*.pdf"))
        print(f"Found {len(pdf_files_extra)} PDFs in extra folder")

        for pdf in pdf_files_extra:
            print(f"Loading PDF: {pdf}")
            loader = PyPDFLoader(str(pdf))
            pdf_docs = loader.load()
            print(f"  -> {len(pdf_docs)} pages loaded")
            docs.extend(pdf_docs)

        # CSV
        csv_files = list(Path(EXTRA_PDF_PATH).rglob("*.csv"))
        print(f"Found {len(csv_files)} CSV files")

        for csv_file in csv_files:
            print(f"Loading CSV: {csv_file}")
            try:
                df = pd.read_csv(csv_file)
                print(f"  -> {len(df)} rows")

                for _, row in df.iterrows():
                    row_text = "\n".join(
                        [f"{col}: {row[col]}" for col in df.columns]
                    )

                    docs.append(
                        Document(
                            page_content=row_text,
                            metadata={"source": str(csv_file)},
                        )
                    )

            except Exception as e:
                print(f"Error reading {csv_file}: {e}")

    print("\nTotal raw documents loaded:", len(docs))
    return docs


# =====================================================
# BUILD FAISS INDEX
# =====================================================

def build_faiss_index(path: str, chunk_size: int, overlap: int, docs: List[Document]):

    print("\n----------------------------------------")
    print(f"Building FAISS at: {path}")
    print(f"Chunk size: {chunk_size}, Overlap: {overlap}")
    print("----------------------------------------")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )

    print("Splitting documents...")
    split_docs = splitter.split_documents(docs)

    print(f"Total chunks created: {len(split_docs)}")

    print("Initializing embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Creating FAISS index...")
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    os.makedirs(path, exist_ok=True)

    print("Saving FAISS index...")
    vectorstore.save_local(path)

    print("FAISS index saved successfully.")

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("\n========================================")
    print("FAISS INDEX BUILD PROCESS STARTED")
    print("========================================")

    raw_docs = load_documents()

    for path, chunk_size, overlap in FAISS_CONFIGS:
        build_faiss_index(path, chunk_size, overlap, raw_docs)

    print("\n========================================")
    print("ALL FAISS INDEXES CREATED SUCCESSFULLY")
    print("========================================")