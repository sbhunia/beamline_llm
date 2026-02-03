from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os

def load_spec_macros():
    spec_dir = "data/mac_docs"
    docs = []

    for root, _, files in os.walk(spec_dir):
        for file in files:
            if file.endswith(".mac"):
                path = os.path.join(root, file)
                try:
                    loader = TextLoader(path)
                    docs.extend(loader.load())
                except Exception as e:
                    print(f"Failed to load {path}: {e}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)
