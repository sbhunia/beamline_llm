from __future__ import annotations
import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

MD_DIR = "/home/vallurs/research/data/md_files"

EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
TOP_K = 5

def build_vectorstore():
    print("Rebuilding FAISS from scratch...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMB_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"batch_size": 32},
    )

    documents = []

    for root, _, files in os.walk(MD_DIR):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)

                loader = TextLoader(full_path, encoding="utf-8")
                docs = loader.load()

                for d in docs:
                    d.metadata["source_file"] = file
                    d.metadata["full_path"] = full_path

                documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    print("Total chunks created:", len(chunks))

    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


VECTORSTORE = build_vectorstore()

def ask_rag(query: str):

    results = VECTORSTORE.similarity_search_with_score(query, k=TOP_K)

    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source_file')}]\n"
        f"{doc.page_content}"
        for doc, _ in results
    )

    llm = ChatOllama(
        model="mistral:instruct",
        temperature=0.0,
        max_retries=5,
    )

    system_prompt = """
        You are a technical assistant for a synchrotron beamline control system.

        Use ONLY the provided context.

        RULES:

        Provide a direct answer to the question.

        Do not include information or tables that are unrelated to the specific question asked.

        If the context contains direct instructions → list only what is available.

        For multiple steps → list all steps clearly AND preserve the EXACT order they appear.

        If the context contains related links but no steps → explain available info and point to links.

        If a table contains the specific answer requested → reproduce the full table.

        IMPORTANT:

        Do NOT reorder or reinterpret steps.

        If nothing relevant is present at all, say: Not found in the provided documents.

        Do NOT invent steps or procedures.
        """

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}")
        ]
    )

    return {
        "answer": response.content.strip(),
        "retrieved": [
            {
                "content": doc.page_content,
                "score": float(score),
                "source_file": doc.metadata.get("source_file"),
                "full_path": doc.metadata.get("full_path"),
            }
            for doc, score in results
        ]
    }

