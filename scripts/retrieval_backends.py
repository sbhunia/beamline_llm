from __future__ import annotations
from typing import List, Tuple
from langchain_community.vectorstores import Qdrant, FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

def build_both(docs: List[Document], name: str):
    emb=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    qdrant=Qdrant.from_documents(docs,emb,location=":memory:",collection_name=f"{name}-qdrant")
    faiss=FAISS.from_documents(docs,emb)
    return qdrant,faiss

def dual_search(qdrant,faiss,query:str,k:int=6):
    q_hits=qdrant.similarity_search_with_score(query,k=k)
    f_hits=faiss.similarity_search_with_score(query,k=k)
    def pack(hits):
        return [(d.metadata.get("source","?"),d.page_content,float(s)) for d,s in hits]
    return pack(q_hits),pack(f_hits)
