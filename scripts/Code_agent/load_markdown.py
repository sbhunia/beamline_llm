from __future__ import annotations
import os
import glob
import re
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = os.getenv("MARKDOWN_DIR", "data/markdown_docs")

def _normalize_text(txt: str) -> str:
    """
    Normalize text while preserving command structure.
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

def _is_command_definition(text: str) -> bool:
    """
    Detect SPEC command list items like:
    `te` - read or set the temperature
    """
    return bool(
        re.match(r"^`?[a-zA-Z][a-zA-Z0-9_]{0,10}`?\s+-\s+", text)
    )


def load_markdown_docs() -> List[Document]:
    """
    Load markdown documentation and split it so that
    EACH SPEC command bullet becomes its OWN vector.
    """

    paths = glob.glob(os.path.join(DATA_DIR, "**/*.md"), recursive=True)
    docs: List[Document] = []

    for path in paths:
        loader = TextLoader(path, encoding="utf-8")
        raw_docs = loader.load()

        for d in raw_docs:
            d.metadata = d.metadata or {}
            d.metadata["source"] = os.path.basename(path)
            docs.append(d)

    
    splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n* `",     
            "\n- `",
            "\n* ",
            "\n- ",
            "\n\n",
            "\n",
        ],
        chunk_size=200,
        chunk_overlap=20,
        length_function=len,
    )

    chunks: List[Document] = []

    for d in docs:
        parts = splitter.split_text(d.page_content or "")

        for part in parts:
            text = _normalize_text(part)
            if not text:
                continue

            kind = "markdown"
            if _is_command_definition(text):
                kind = "command"

            chunks.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": d.metadata.get("source"),
                        "kind": kind,
                    },
                )
            )

    print(f"[DEBUG] Loaded {len(chunks)} markdown chunks")
    print(
        f"[DEBUG] Command chunks: "
        f"{sum(1 for c in chunks if c.metadata.get('kind') == 'command')}"
    )

    return chunks
