# import os
# import subprocess
# import pandas as pd
# from typing import List, Dict, Tuple
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError, as_completed

# import streamlit as st

# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_ollama import ChatOllama
# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import (
#     DirectoryLoader,
#     TextLoader,
#     PyPDFLoader,
# )

# # =====================================================
# # CONFIG
# # =====================================================

# OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# TOP_K = 4

# DOCUMENTS_PATH = "/home/vallurs/research/data/md_files"
# EXTRA_PDF_PATH = "/home/vallurs/research/data/drive_docs"

# RESULTS_FILE = "/home/vallurs/research/COLAB/results.xlsx"

# FAISS_CONFIGS = [
#     ("/home/vallurs/research/COLAB/faiss_cs50_ov10", 50, 10),
#     ("/home/vallurs/research/COLAB/faiss_cs100_ov50", 100, 50),
#     ("/home/vallurs/research/COLAB/faiss_cs200_ov100", 200, 100),
#     ("/home/vallurs/research/COLAB/faiss_cs250_ov50", 250, 50),
#     ("/home/vallurs/research/COLAB/faiss_cs300_ov150", 300, 150),
#     ("/home/vallurs/research/COLAB/faiss_cs500_ov100", 500, 100),
#     ("/home/vallurs/research/COLAB/faiss_cs500_ov250", 500, 250),
#     ("/home/vallurs/research/COLAB/faiss_cs800_ov200", 800, 200),
#     ("/home/vallurs/research/COLAB/faiss_cs1000_ov500", 1000, 500),
#     ("/home/vallurs/research/COLAB/faiss_cs2000_ov800", 2000, 800),
# ]

# EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# AVAILABLE_MODELS = [
#     "phi3:mini",
#     "llama2:latest",
#     "deepseek-r1:1.5b",
#     "gemma:2b",
#     "deepseek-coder:6.7b",
#     "codellama:7b-instruct",
#     "mistral:instruct",
#     "mistral:latest",
# ]

# # =====================================================
# # UTILITIES
# # =====================================================

# def append_to_excel(model: str, question: str, answer: str):
#     new_row = pd.DataFrame(
#         [{"Model": model, "Question": question, "Answer": answer}]
#     )

#     if Path(RESULTS_FILE).exists():
#         df_existing = pd.read_excel(RESULTS_FILE)
#         df_combined = pd.concat([df_existing, new_row], ignore_index=True)
#     else:
#         df_combined = new_row

#     df_combined.to_excel(RESULTS_FILE, index=False)

# def stop_other_ollama_models(selected_model: str):
#     try:
#         result = subprocess.run(
#             ["ollama", "ps"],
#             capture_output=True,
#             text=True,
#             check=True,
#         )

#         lines = result.stdout.strip().split("\n")

#         for line in lines[1:]:
#             parts = line.split()
#             if not parts:
#                 continue
#             model_name = parts[0]
#             if model_name != selected_model:
#                 subprocess.run(["ollama", "stop", model_name])

#     except Exception as e:
#         print(f"Warning stopping models: {e}")

# # =====================================================
# # CACHED INITIALIZERS
# # =====================================================

# @st.cache_resource
# def get_embeddings():
#     return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# @st.cache_resource
# def load_or_create_vectorstores():

#     embeddings = get_embeddings()
#     stores = []
#     raw_docs = None

#     for path, chunk_size, overlap in FAISS_CONFIGS:

#         index_path = Path(path)
#         index_file = index_path / "index.faiss"
#         metadata_file = index_path / "index.pkl"

#         if index_file.exists() and metadata_file.exists():
#             store = FAISS.load_local(
#                 path,
#                 embeddings,
#                 allow_dangerous_deserialization=True,
#             )
#         else:
#             if raw_docs is None:
#                 raw_docs = load_documents()

#             splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=chunk_size,
#                 chunk_overlap=overlap,
#             )

#             split_docs = splitter.split_documents(raw_docs)

#             os.makedirs(path, exist_ok=True)
#             store = FAISS.from_documents(split_docs, embeddings)
#             store.save_local(path)

#         stores.append(store)

#     return stores

# # =====================================================
# # DOCUMENT LOADING
# # =====================================================

# def load_documents() -> List[Document]:

#     docs = []

#     if Path(DOCUMENTS_PATH).exists():
#         md_loader = DirectoryLoader(
#             DOCUMENTS_PATH,
#             glob="**/*.md",
#             loader_cls=TextLoader,
#         )
#         docs.extend(md_loader.load())

#     if Path(DOCUMENTS_PATH).exists():
#         pdf_files_main = list(Path(DOCUMENTS_PATH).rglob("*.pdf"))
#         for pdf in pdf_files_main:
#             loader = PyPDFLoader(str(pdf))
#             docs.extend(loader.load())

#     if Path(EXTRA_PDF_PATH).exists():

#         pdf_files_extra = list(Path(EXTRA_PDF_PATH).rglob("*.pdf"))
#         for pdf in pdf_files_extra:
#             loader = PyPDFLoader(str(pdf))
#             docs.extend(loader.load())

#         csv_files = list(Path(EXTRA_PDF_PATH).rglob("*.csv"))
#         for csv_file in csv_files:
#             df = pd.read_csv(csv_file)
#             for _, row in df.iterrows():
#                 row_text = "\n".join(
#                     [f"{col}: {row[col]}" for col in df.columns]
#                 )
#                 docs.append(
#                     Document(
#                         page_content=row_text,
#                         metadata={"source": str(csv_file)},
#                     )
#                 )

#     return docs

# # =====================================================
# # RETRIEVAL
# # =====================================================

# def retrieve(query: str):

#     stores = load_or_create_vectorstores()
#     all_results = []

#     for store in stores:
#         results = store.similarity_search_with_score(query, k=TOP_K)
#         all_results.extend(results)

#     unique: Dict[str, Tuple[Document, float]] = {}

#     for doc, score in all_results:
#         if doc.page_content not in unique:
#             unique[doc.page_content] = (doc, score)

#     return list(unique.values())

# # =====================================================
# # PROMPT
# # =====================================================

# BASE_PROMPT = """
#         You are a technical assistant for a synchrotron beamline control system.

#         Use ONLY the provided context.

#         RULES:

#         Provide a direct answer to the question.

#         Do not include information or tables that are unrelated to the specific question asked.

#         If the context contains direct instructions → list only what is available.

#         For multiple steps → list all steps clearly AND preserve the EXACT order they appear.

#         If the context contains related links but no steps → explain available info and point to links.

#         If a table contains the specific answer requested → reproduce the full table.

#         IMPORTANT:

#         Do NOT reorder or reinterpret steps.

#         If nothing relevant is present at all, say: Not found in the provided documents.

#         Do NOT invent steps or procedures.
#         """

# def build_prompt(context_docs: List[Document], question: str):

#     context = "\n\n".join(
#         [
#             f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
#             for doc in context_docs
#         ]
#     )

#     return f"""
# {BASE_PROMPT}

# CONTEXT:
# {context}

# QUESTION:
# {question}
# """

# # =====================================================
# # STREAMLIT APP
# # =====================================================

# st.set_page_config(
#     page_title="Beamline Documentation Assistant",
#     page_icon="📄",
#     layout="wide",
# )

# st.markdown("## Beamline Documentation Assistant")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# user_query = st.chat_input("Ask your question...")

# if user_query:

#     st.session_state.messages.append({"role": "user", "content": user_query})

#     with st.chat_message("user"):
#         st.markdown(user_query)

#     results = retrieve(user_query)
#     context_docs = [doc for doc, _ in results]
#     prompt = build_prompt(context_docs, user_query)

#     with st.chat_message("assistant"):

#         for model_name in AVAILABLE_MODELS:

#             st.markdown(f"### {model_name}")

#             stop_other_ollama_models(model_name)

#             llm = ChatOllama(
#                 model=model_name,
#                 base_url=OLLAMA_BASE,
#                 temperature=0,
#             )

#             response = llm.invoke(prompt)
#             answer = response.content

#             st.markdown(answer)

#             append_to_excel(model_name, user_query, answer)

#             with st.expander(f"🔎 References ({model_name})"):
#                 for i, (doc, score) in enumerate(results, 1):
#                     st.markdown(
#                         f"""
# **[{i}] Source:** `{doc.metadata.get('source','unknown')}`  
# **Score:** `{float(score):.4f}`  

# {doc.page_content[:500]}
# """
#                     )

#     st.session_state.messages.append(
#         {"role": "assistant", "content": "Multi-model response generated."}
#     )

import os
import subprocess
import pandas as pd
from typing import List, Dict, Tuple
from pathlib import Path

import streamlit as st

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.documents import Document

# =====================================================
# CONFIG
# =====================================================

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

TOP_K_PER_INDEX = 4
MAX_FINAL_CHUNKS = 6

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

RESULTS_FILE = "/home/vallurs/research/COLAB/results.xlsx"

FAISS_CONFIGS = [
    "/home/vallurs/research/COLAB/faiss_cs50_ov10",
    "/home/vallurs/research/COLAB/faiss_cs100_ov50",
    "/home/vallurs/research/COLAB/faiss_cs200_ov100",
    "/home/vallurs/research/COLAB/faiss_cs250_ov50",
    "/home/vallurs/research/COLAB/faiss_cs300_ov150",
    "/home/vallurs/research/COLAB/faiss_cs500_ov100",
    "/home/vallurs/research/COLAB/faiss_cs500_ov250",
    "/home/vallurs/research/COLAB/faiss_cs800_ov200",
    "/home/vallurs/research/COLAB/faiss_cs1000_ov500",
    "/home/vallurs/research/COLAB/faiss_cs2000_ov800",
]

AVAILABLE_MODELS = [
    "phi3:mini",
    "llama2:latest",
    "deepseek-r1:1.5b",
    "gemma:2b",
    "deepseek-coder:6.7b",
    "codellama:7b-instruct",
    "mistral:instruct",
    "mistral:latest",
]

# =====================================================
# UTILITIES
# =====================================================

def append_to_excel(model: str, question: str, answer: str):
    new_row = pd.DataFrame(
        [{"Model": model, "Question": question, "Answer": answer}]
    )

    if Path(RESULTS_FILE).exists():
        df_existing = pd.read_excel(RESULTS_FILE)
        df_combined = pd.concat([df_existing, new_row], ignore_index=True)
    else:
        df_combined = new_row

    df_combined.to_excel(RESULTS_FILE, index=False)


def stop_other_ollama_models(selected_model: str):
    try:
        result = subprocess.run(
            ["ollama", "ps"],
            capture_output=True,
            text=True,
            check=True,
        )

        lines = result.stdout.strip().split("\n")

        for line in lines[1:]:
            parts = line.split()
            if not parts:
                continue
            model_name = parts[0]
            if model_name != selected_model:
                subprocess.run(["ollama", "stop", model_name])

    except Exception as e:
        print(f"Warning stopping models: {e}")

# =====================================================
# CACHED INITIALIZATION
# =====================================================

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


@st.cache_resource
def load_vectorstores():
    embeddings = get_embeddings()
    stores = []

    for path in FAISS_CONFIGS:
        index_path = Path(path)
        index_file = index_path / "index.faiss"
        metadata_file = index_path / "index.pkl"

        if index_file.exists() and metadata_file.exists():
            store = FAISS.load_local(
                path,
                embeddings,
                allow_dangerous_deserialization=True,
            )
            stores.append(store)

    return stores

# =====================================================
# FIXED RETRIEVAL WITH GLOBAL RERANKING
# =====================================================

def retrieve(query: str):

    stores = load_vectorstores()
    all_results = []

    # 1️⃣ Retrieve from each index
    for store in stores:
        results = store.similarity_search_with_score(
            query,
            k=TOP_K_PER_INDEX
        )
        all_results.extend(results)

    # 2️⃣ Deduplicate by content
    unique: Dict[str, Tuple[Document, float]] = {}

    for doc, score in all_results:
        key = doc.page_content.strip()

        if key not in unique or score < unique[key][1]:
            unique[key] = (doc, score)

    deduped = list(unique.values())

    # 3️⃣ GLOBAL SORT (lower score = better)
    deduped.sort(key=lambda x: x[1])

    # 4️⃣ Keep best N total
    final_results = deduped[:MAX_FINAL_CHUNKS]

    return final_results

# =====================================================
# STRUCTURED PROMPT
# =====================================================

def build_prompt(context_docs: List[Document], question: str):

    context_blocks = []

    for i, doc in enumerate(context_docs, 1):
        source = doc.metadata.get("source", "unknown")

        block = (
            f"---\n"
            f"[Chunk {i} | Source: {source}]\n"
            f"{doc.page_content.strip()}\n"
        )

        context_blocks.append(block)

    context = "\n".join(context_blocks)

    return f"""
You are a technical assistant for a synchrotron beamline control system.

STRICT RULES:

- Use ONLY the provided context.
- Provide a direct answer to the question.
- Do NOT include unrelated information.
- If listing steps, preserve the EXACT order as written.
- Do NOT merge or reinterpret steps.
- If nothing relevant exists, respond exactly with:
  Not found in the provided documents.

CONTEXT:
{context}

QUESTION:
{question}
"""

# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(
    page_title="Beamline Documentation Assistant",
    page_icon="📄",
    layout="wide",
)

st.markdown("## Beamline Documentation Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_query = st.chat_input("Ask your question...")

if user_query:

    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    results = retrieve(user_query)
    context_docs = [doc for doc, _ in results]
    prompt = build_prompt(context_docs, user_query)

    with st.chat_message("assistant"):

        for model_name in AVAILABLE_MODELS:

            st.markdown(f"### {model_name}")

            stop_other_ollama_models(model_name)

            llm = ChatOllama(
                model=model_name,
                base_url=OLLAMA_BASE,
                temperature=0,
                num_predict=512,
            )

            response = llm.invoke(prompt)
            answer = response.content

            st.markdown(answer)

            append_to_excel(model_name, user_query, answer)

            with st.expander(f"🔎 References ({model_name})"):
                for i, (doc, score) in enumerate(results, 1):
                    st.markdown(
                        f"""
**[{i}] Score:** `{float(score):.4f}`  
{doc.page_content[:500]}
"""
                    )

    st.session_state.messages.append(
        {"role": "assistant", "content": "Multi-model response generated."}
    )