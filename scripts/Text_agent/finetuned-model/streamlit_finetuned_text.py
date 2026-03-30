from __future__ import annotations

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_DATA_DIR = "/home/vallurs/research/data"
DEFAULT_EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"


def load_documents(data_dir: str):
    docs = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            path = os.path.join(root, file)
            lower = file.lower()
            if lower.endswith(".md"):
                loaded = TextLoader(path, encoding="utf-8").load()
            elif lower.endswith(".pdf"):
                loaded = PyPDFLoader(path).load()
            else:
                continue
            for d in loaded:
                d.metadata["source_file"] = file
                d.metadata["full_path"] = path
            docs.extend(loaded)
    return docs


@st.cache_resource
def build_vectorstore(data_dir: str, emb_model: str, chunk_size: int, chunk_overlap: int):
    docs = load_documents(data_dir)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=emb_model, model_kwargs={"device": "cpu"})
    return FAISS.from_documents(chunks, embeddings)


def ask_model(model_name: str, question: str, context: str):
    llm = ChatOllama(model=model_name, temperature=0.0, max_retries=3)
    system_prompt = (
        "You are a technical assistant for a synchrotron beamline control system.\n"
        "Use provided context when present. If context is insufficient, say what is missing."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion:\n{question}" if context else question
    response = llm.invoke(
        [
            ("system", system_prompt),
            ("human", user_prompt),
        ]
    )
    return response.content.strip()


st.set_page_config(page_title="Fine-Tuned Text Agent", page_icon="🧠", layout="wide")
st.title("Fine-Tuned Text Agent")
st.caption("Chat with your Ollama model, with optional retrieval from Markdown/PDF docs.")

with st.sidebar:
    st.subheader("Settings")
    model_name = st.text_input("Ollama model tag", value="text-agent-ft")
    data_dir = st.text_input("Docs folder", value=DEFAULT_DATA_DIR)
    use_retrieval = st.checkbox("Use retrieval (RAG)", value=True)
    top_k = st.slider("Top-k chunks", min_value=1, max_value=12, value=5)
    chunk_size = st.slider("Chunk size", min_value=200, max_value=1200, value=700, step=50)
    chunk_overlap = st.slider("Chunk overlap", min_value=0, max_value=400, value=120, step=20)
    emb_model = st.text_input("Embedding model", value=DEFAULT_EMB_MODEL)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever_ready" not in st.session_state:
    st.session_state.retriever_ready = False

if use_retrieval:
    if st.button("Build / Refresh Vector Index"):
        with st.spinner("Building vector index from documents..."):
            st.session_state.vectorstore = build_vectorstore(data_dir, emb_model, chunk_size, chunk_overlap)
            st.session_state.retriever_ready = True
        st.success("Vector index is ready.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            st.markdown("**Sources:**")
            for s in m["sources"]:
                st.markdown(f"- `{s}`")

question = st.chat_input("Ask your fine-tuned model...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    context = ""
    sources = []
    if use_retrieval and st.session_state.get("retriever_ready"):
        results = st.session_state.vectorstore.similarity_search_with_score(question, k=top_k)
        context = "\n\n---\n\n".join(
            f"[Source: {doc.metadata.get('source_file')}]\n{doc.page_content}"
            for doc, _ in results
        )
        seen = set()
        for doc, _ in results:
            src = doc.metadata.get("full_path", doc.metadata.get("source_file", "unknown"))
            if src not in seen:
                seen.add(src)
                sources.append(src)

    with st.chat_message("assistant"):
        with st.spinner("Querying model..."):
            try:
                answer = ask_model(model_name=model_name, question=question, context=context)
            except Exception as e:
                answer = f"Error while querying model: {e}"
        st.markdown(answer)
        if sources:
            st.markdown("**Sources:**")
            for s in sources:
                st.markdown(f"- `{s}`")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
