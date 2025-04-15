import os
from typing import List, Tuple
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to FAISS index
FAISS_INDEX_PATH = "faiss_index"

def ask_question(
    splits: List[Document],
    question: str,
    model: str = "gpt-4o",
    temperature: float = 0.1,
    k: int = 8
) -> Tuple[str, List[Document]]:
    """
    Ask a question to the OpenAI model using RAG
    
    Args:
        splits: List of document chunks
        question: Question to ask
        model: OpenAI model to use (e.g., "gpt-4o", "gpt-3.5-turbo")
        temperature: Sampling temperature
        k: Number of documents to retrieve
        
    Returns:
        answer: Model's response
        source_documents: Relevant source documents
    """
    # Ensure OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    
    # Create embeddings using OpenAI
    embeddings = OpenAIEmbeddings()
    
    # Try to load existing FAISS index or create a new one
    FAISS_INDEX_PATH = "faiss_index"
    if os.path.exists(FAISS_INDEX_PATH):
        print("Loading existing FAISS index...")
        vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        print("Creating new FAISS index...")
        vectorstore = FAISS.from_documents(splits, embeddings)
        vectorstore.save_local(FAISS_INDEX_PATH)
        print(f"FAISS index saved to {FAISS_INDEX_PATH}")
    
    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    # Configure callbacks - optional for streaming output
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    # Initialize OpenAI model
    llm = ChatOpenAI(
        model_name=model,
        temperature=temperature,
        openai_api_key=api_key,
        streaming=True,
        verbose=False
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        verbose=False
    )
    
    # Run the query
    result = qa_chain.invoke({"query": question})
    
    return result["result"], result["source_documents"]