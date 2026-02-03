import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_DIR = os.path.join(BASE_DIR, "markdown_docs_modified")
FAISS_PATH = os.path.join(BASE_DIR, "faiss_index11")

EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
TOP_K = 8

# Gemini key from Streamlit Secrets
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# ============================================================
# BUILD / LOAD VECTORSTORE
# ============================================================

def build_or_load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMB_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"batch_size": 32},
    )

    if os.path.exists(FAISS_PATH):
        return FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )

    documents = []
    for root, _, files in os.walk(MD_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                loader = TextLoader(path, encoding="utf-8")
                docs = loader.load()
                for d in docs:
                    d.metadata["source"] = os.path.relpath(path, MD_DIR)
                documents.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise RuntimeError(
            f"No markdown chunks found. Check that files exist in {MD_DIR}"
        )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(FAISS_PATH)
    return vectorstore


VECTORSTORE = build_or_load_vectorstore()

# ============================================================
# QUERY FUNCTION (SYSTEM PROMPT PRESERVED)
# ============================================================

def ask_rag(query: str) -> str:
    results = VECTORSTORE.similarity_search_with_score(query, k=TOP_K)

    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
        for doc, _ in results
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.5,
        max_retries=5,
    )

    system_prompt = """
You are a technical assistant for a synchrotron beamline control system.

Use ONLY the provided context.

If the context contains:
- direct instructions or steps → list all steps clearly AND preserve the EXACT order they appear.
- related links or resources but no step-by-step instructions →
  explain what information is available and point to the relevant links.
- If the source contains a table, reproduce the full table including all columns. Do not omit columns.

IMPORTANT:
- Do NOT reorder, optimize, or reinterpret step sequences.
- If the user’s question contains conditions that conflict with the document
  (e.g., invalid temperature ranges or operating modes),
  explicitly point out the mismatch BEFORE listing any steps.

If nothing relevant is present at all, say:
"Not found in the provided documents."

Do NOT invent steps or procedures.
"""

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion:\n{query}"
            ),
        ]
    )

    return response.content[0]["text"]
