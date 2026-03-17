from __future__ import annotations
import os
import glob
import re
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


MD_DIR = r"/home/vallurs/research/data/md_files"


# ---------------- Cleaning ----------------

def _clean_markdown(txt: str) -> str:
    txt = (
        txt.replace("\r\n", "\n")
           .replace("\r", "\n")
           .replace("\u2018", "'")
           .replace("\u2019", "'")
           .replace("\u201C", '"')
           .replace("\u201D", '"')
    )

    # Remove HTML comments
    txt = re.sub(r"<!--.*?-->", "", txt, flags=re.DOTALL)

    return txt.strip()


# ---------------- Loader ----------------

def load_markdown_docs() -> List[Document]:
    paths = glob.glob(os.path.join(MD_DIR, "**/*.md"), recursive=True)

    if not paths:
        raise ValueError(f"No markdown files found in {MD_DIR}")

    docs: List[Document] = []

    # Smart splitter for NON-procedure sections
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,        # Balanced size for 7B models
        chunk_overlap=150,     # Preserve semantic continuity
        separators=[
            "\n### ",
            "\n## ",
            "\n# ",
            "\n\n",
            "\n",
            " ",
        ],
    )

    for path in paths:
        loader = TextLoader(path, encoding="utf-8")
        raw = loader.load()[0].page_content
        text = _clean_markdown(raw)

        # Split on procedure headers ONLY
        sections = re.split(
            r"(?=^###\s+Steps\s+to\s+use\s+)|(?=^\s*<b><i><u>\s*\d+K.*?temperature)",
            text,
            flags=re.MULTILINE | re.IGNORECASE,
        )

        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue

            # ---------------- Procedure Block ----------------
            if sec.lower().startswith("### steps to use"):
                docs.append(
                    Document(
                        page_content=sec,
                        metadata={
                            "source": os.path.basename(path),
                            "kind": "procedure",
                        },
                    )
                )

            # ---------------- Non-Procedure Block ----------------
            else:
                # Split safely into size-controlled chunks
                split_chunks = text_splitter.split_text(sec)

                for chunk in split_chunks:
                    chunk = chunk.strip()
                    if not chunk:
                        continue

                    docs.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                "source": os.path.basename(path),
                                "kind": "markdown",
                            },
                        )
                    )

    # ---------------- Diagnostics ----------------

    print(f"[DEBUG] Total chunks created: {len(docs)}")

    proc_count = sum(d.metadata["kind"] == "procedure" for d in docs)
    print(f"[DEBUG] Procedure chunks: {proc_count}")
    print(f"[DEBUG] Non-procedure chunks: {len(docs) - proc_count}")

    if docs:
        lengths = [len(d.page_content) for d in docs]
        print(f"[DEBUG] Avg chunk length: {sum(lengths)//len(lengths)}")
        print(f"[DEBUG] Max chunk length: {max(lengths)}")

    return docs