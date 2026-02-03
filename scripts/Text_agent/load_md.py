from __future__ import annotations
import os, glob, re
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

MD_DIR = "/home/vallurs/research/data/md_files"


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

    # remove HTML comments
    txt = re.sub(r"<!--.*?-->", "", txt, flags=re.DOTALL)

    return txt.strip()


# ---------------- Loader ----------------

def load_markdown_docs() -> List[Document]:
    paths = glob.glob(os.path.join(MD_DIR, "**/*.md"), recursive=True)
    docs: List[Document] = []

    for path in paths:
        loader = TextLoader(path, encoding="utf-8")
        raw = loader.load()[0].page_content
        text = _clean_markdown(raw)

        # Split ONLY on top-level procedure headers
        sections = re.split(
            r"(?=^###\s+Steps\s+to\s+use\s+)",
            text,
            flags=re.MULTILINE,
        )

        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue

            # Detect procedure blocks
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
            else:
                # non-procedure content (intro, policy, etc.)
                docs.append(
                    Document(
                        page_content=sec,
                        metadata={
                            "source": os.path.basename(path),
                            "kind": "markdown",
                        },
                    )
                )

    print(f"[DEBUG] Loaded {len(docs)} markdown chunks (procedure-safe)")
    print(
        "[DEBUG] Procedure chunks:",
        sum(d.metadata["kind"] == "procedure" for d in docs),
    )

    return docs
