from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os

def load_drive_docs():
    drive_dir = "data/drive_docs"
    docs = []

    for file in os.listdir(drive_dir):
        path = os.path.join(drive_dir, file)

        try:
            if file.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif file.endswith((".txt", ".mac")):
                loader = TextLoader(path)
            else:
                continue

            docs.extend(loader.load())

        except Exception as e:
            print(f"Failed to load {file}: {e}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)
