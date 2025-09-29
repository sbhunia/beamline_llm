from __future__ import annotations
from langchain_core.documents import Document

def chunk_docs(docs,size:int,overlap:int):
    out=[]
    for d in docs:
        text=(d.page_content or "").strip()
        if not text: continue
        i=0
        while i<len(text):
            chunk=text[i:i+size]
            out.append(Document(page_content=chunk,metadata=d.metadata))
            i+=max(1,size-overlap)
    return out
