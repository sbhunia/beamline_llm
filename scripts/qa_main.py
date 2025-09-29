# scripts/qa_main.py
import sys
import os
import re

from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

# Import sibling scripts/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.load_markdown import load_markdown_docs
from scripts.load_drive import load_drive_docs
from scripts.load_spec_code import load_spec_macros
# from scripts.load_website import load_website  # disabled to reduce drift

THINK_RE = re.compile(r"<\s*think[^>]*>.*?<\s*/\s*think\s*>", flags=re.DOTALL | re.IGNORECASE)
REFLECT_RE = re.compile(r"<\s*(analysis|reflection)[^>]*>.*?<\s*/\s*\1\s*>", flags=re.DOTALL | re.IGNORECASE)

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return s
    s = s.replace("\u200b", "").replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = THINK_RE.sub("", s)
    s = REFLECT_RE.sub("", s)
    s = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", s)
    return s

print("Loading documents...")
all_docs = []
all_docs += load_markdown_docs()
all_docs += load_drive_docs()
all_docs += load_spec_macros()
# try:
#     all_docs += load_website("https://www.chess.cornell.edu/users/qm2-beamline")
# except Exception as e:
#     print("Skipping website load due to error:", e)
print(f"Total documents loaded: {len(all_docs)}")

print("Creating embeddings...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Creating Qdrant vector store...")
qdrant = Qdrant.from_documents(
    documents=all_docs,
    embedding=embedding_model,
    location=":memory:",
    collection_name="beamline-docs",
)

# -----------------------------
# Chainlit uses this adapter
# -----------------------------
class VectorSearchAdapter:
    def __init__(self, vs): self.vs = vs
    def search(self, query: str, k: int = 6):
        results = self.vs.similarity_search_with_score(query, k=k)
        return [(doc.metadata.get("source","unknown"), doc.page_content, float(score)) for doc, score in results]

def get_retriever():
    """Return a simple adapter used by scripts/chainlit_app.py (no RetrievalQA)."""
    return VectorSearchAdapter(qdrant)

# -----------------------------
# Optional CLI (grounded, no invention)
# -----------------------------
def _prefer_mac(docs, k=8):
    mac = [d for d in docs if str(d.metadata.get("source","")).lower().endswith(".mac")]
    rest = [d for d in docs if d not in mac]
    return (mac + rest)[:k]

def _answer_grounded(query: str) -> str:
    BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")
    llm = ChatOllama(model=MODEL, base_url=BASE_URL, temperature=0.0)

    hits = qdrant.similarity_search_with_score(query, k=24)
    if not hits:
        return "I don’t see that in the provided documents."
    docs = _prefer_mac([d for d, _ in hits], k=8)
    excerpts = []
    for d in docs:
        paras = [p.strip() for p in re.split(r"\n\s*\n", d.page_content or "") if p.strip()]
        best = paras[0] if paras else (d.page_content or "")[:600]
        excerpts.append(best)

    prompt = (
        "Answer ONLY using the excerpts below.\n"
        "If the excerpts do not contain the necessary facts, reply exactly: "
        "\"I don’t see that in the provided documents.\" and nothing else.\n\n"
        f"QUESTION:\n{query}\n\nEXCERPTS:\n\n" + "\n\n---\n\n".join(excerpts)
    )
    resp = llm.invoke([{"role": "user", "content": prompt}])
    raw = getattr(resp, "content", str(resp))
    return clean_text(raw)

if __name__ == "__main__":
    print("Loading LLM via Ollama...")
    while True:
        query = input("\nAsk your question or type 'exit': ")
        if query.strip().lower() in {"exit", "quit"}:
            break
        print("\nThinking...")
        print("\nFinal answer:", _answer_grounded(query))
