# import os
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import SystemMessage, HumanMessage

# # -------- CONFIG --------
# MD_DIR = "markdown_docs_modified"
# # ============================================================
# # CONFIG
# # ============================================================

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MD_DIR = os.path.join(BASE_DIR, "md_files")
# FAISS_PATH = os.path.join(BASE_DIR, "faiss_index11")

# EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
# TOP_K = 8
# FAISS_PATH = "faiss_index11"

# # Gemini key from environment (Streamlit Secrets)
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# # ============================================================
# # BUILD / LOAD VECTORSTORE
# def build_or_load_vectorstore():
#     embeddings = HuggingFaceEmbeddings(
#         model_name=EMB_MODEL,
#         model_kwargs={"device": "cpu"},
#         encode_kwargs={"batch_size": 32}
#     )

#     if os.path.exists(FAISS_PATH):
#         return FAISS.load_local(
#             FAISS_PATH,
#             embeddings,
#             allow_dangerous_deserialization=True
#         )

#     documents = []
#     for root, _, files in os.walk(MD_DIR):
#         for file in files:
#             if file.endswith(".md"):
#                 loader = TextLoader(os.path.join(root, file), encoding="utf-8")
#                 docs = loader.load()
#                 for d in docs:
#                     d.metadata["source"] = os.path.relpath(
#                         os.path.join(root, file), MD_DIR
#                     )
#                 documents.extend(docs)

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=250,
#         chunk_overlap=150,
#     )

#     chunks = splitter.split_documents(documents)
#     vectorstore = FAISS.from_documents(chunks, embeddings)
#     vectorstore.save_local(FAISS_PATH)
#     return vectorstore


# VECTORSTORE = build_or_load_vectorstore()


# def ask_rag(query: str) -> str:
#     results = VECTORSTORE.similarity_search_with_score(query, k=TOP_K)

#     context = "\n\n---\n\n".join(
#         f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
#         for doc, _ in results
#     )

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-3-flash-preview",
#         temperature=0.5,
#         max_retries=5,
#     )

#     system_prompt = """
# You are a technical assistant for a synchrotron beamline control system.

# Use ONLY the provided context.

# If the context contains:
# - direct instructions or steps → list all steps clearly AND preserve the EXACT order they appear.
# - related links or resources but no step-by-step instructions →
#   explain what information is available and point to the relevant links.
# - If the source contains a table, reproduce the full table including all columns. Do not omit columns.

# IMPORTANT:
# - Do NOT reorder, optimize, or reinterpret step sequences.
# - If the user’s question contains conditions that conflict with the document
#   (e.g., invalid temperature ranges or operating modes),
#   explicitly point out the mismatch BEFORE listing any steps.

# If nothing relevant is present at all, say:
# "Not found in the provided documents."

# Do NOT invent steps or procedures.
# """

#     response = llm.invoke(
#         [
#             SystemMessage(content=system_prompt),
#             HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}")
#         ]
#     )

#     return response.content[0]["text"]



import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. API & PATH CONFIG
load_dotenv()
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_DIR = os.path.join(BASE_DIR, "md_files")
FAISS_PATH = os.path.join(BASE_DIR, "faiss_index_gemini")

# TECHNICAL SPECS (Matches your Ollama configuration)
EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
TOP_K = 5
CHUNK_SIZE = 400
CHUNK_OVERLAP = 200
TEMPERATURE = 0.0

# 2. VECTORSTORE LOGIC
@st.cache_resource
def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMB_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"batch_size": 32}
    )
    
    if os.path.exists(FAISS_PATH):
        return FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    # Load all MD files
    loader = DirectoryLoader(MD_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    documents = loader.load()

    # Exact metadata logic for sources
    for d in documents:
        d.metadata["source_file"] = os.path.basename(d.metadata["source"])
        d.metadata["full_path"] = d.metadata["source"]

    # Exact Chunking Specs
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_PATH)
    return vectorstore

VECTORSTORE = get_vectorstore()

# 3. QUERY FUNCTION
def ask_rag(query: str):
    # Similarity Search
    results = VECTORSTORE.similarity_search_with_score(query, k=TOP_K)
    
    # Context Construction
    context = "\n\n---\n\n".join([
        f"[Source: {doc.metadata.get('source_file')}]\n{doc.page_content}"
        for doc, score in results
    ])

    # Gemini Model Setup (with max_retries as requested)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=TEMPERATURE,
        max_retries=5
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

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}")
    ])

    # Returning dictionary for app.py evaluation compatibility
    return {
        "answer": response.content.strip(),
        "retrieved": [
            {
                "content": doc.page_content,
                "source_file": doc.metadata.get("source_file"),
                "score": float(score),
                "full_path": doc.metadata.get("full_path")
            } for doc, score in results
        ]
    }