# models/llama/query.py
import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from utils.resources import ANSWER_TEMPLATE

def ask_question(splits, question: str, temperature=0.1, k=8, **kwargs):
    """
    Query the Llama model with RAG enhancement - memory-efficient version.
    
    Args:
        splits: Document chunks to search through
        question: The user query
        temperature: Temperature setting (0.0 to 1.0)
        k: Number of documents to retrieve
        **kwargs: Additional arguments which are ignored (allows for compatibility)
        
    Returns:
        tuple: (answer, source_documents)
    """
    print("Building RAG chain...")
    
    # Initialize embeddings model - use smaller embeddings model
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Create vector store if needed, or use existing one
    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(splits, embeddings)
        vectorstore.save_local("faiss_index")
    
    # Reduce number of chunks to save memory during retrieval
    reduced_k = min(k, 5)  # Limit to 5 documents max to reduce memory usage
    
    # Create retriever with memory-efficient settings
    print("Retrieving docs...")
    retriever = vectorstore.as_retriever(
        search_type="similarity",  # Switch to simple similarity search (less memory than MMR)
        search_kwargs={
            "k": reduced_k
        }
    )
    
    # Get relevant documents
    retrieved_docs = retriever.get_relevant_documents(question)
    
    # Format documents for context - limit context length
    context_parts = []
    total_length = 0
    max_context_length = 6000  # Limit context size
    
    for doc in retrieved_docs:
        # Add document if it won't exceed max context length
        if total_length + len(doc.page_content) <= max_context_length:
            context_parts.append(doc.page_content)
            total_length += len(doc.page_content)
        else:
            # Stop adding documents if we reach the limit
            break
    
    context = "\n\n".join(context_parts)
    
    # Create prompt from template
    prompt = PromptTemplate(
        template=ANSWER_TEMPLATE,
        input_variables=["context", "question"]
    )
    
    # Format the prompt
    formatted_prompt = prompt.format(context=context, question=question)
    
    # Setup Ollama with memory-efficient settings
    print("Getting response...")
    llm = Ollama(
        model="tinyllama",  # Use TinyLlama instead of llama3 (much lighter model)
        temperature=temperature,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        num_ctx=1024,  # Reduce context window
        num_gpu=0     # Disable GPU to use CPU only (often more stable with limited memory)
    )
    
    # Get response from LLM
    response = llm(formatted_prompt)
    print("Response received!")
    
    return response, retrieved_docs