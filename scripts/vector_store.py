# scripts/vector_store.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient  # noqa: F401 (kept for future persistence)
from langchain_huggingface import HuggingFaceEmbeddings

from scripts.load_markdown import load_markdown_docs
from scripts.load_drive import load_drive_docs
from scripts.load_spec_code import load_spec_macros
from scripts.load_website import load_website

# Load all docs
print("🔄 Loading documents...")
all_docs = []
all_docs += load_markdown_docs()
all_docs += load_drive_docs()
all_docs += load_spec_macros()
try:
    all_docs += load_website("https://en.wikipedia.org/wiki/Synchrotron")  # temp website
except Exception as e:
    print(f"Skipping website due to error: {e}")

# Set up embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

qdrant = Qdrant.from_documents(
    documents=all_docs,
    embedding=embedding_model,
    location=":memory:",
    collection_name="beamline-docs"
)

print("Qdrant collection created")
