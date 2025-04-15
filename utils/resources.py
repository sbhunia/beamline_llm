from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from typing import List, Dict, Any
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Strict technical template for procedure execution
ANSWER_TEMPLATE = """
### CRYOSTAT PROCEDURE EXECUTOR
**REQUIREMENTS:**
1. Copy EXACT steps from source
2. Preserve ALL FOURC commands
3. Maintain original numbering
4. Include safety warnings

**PROCEDURE:**
{context}

**QUESTION:**
{question}

**RESPONSE FORMAT:**
* Step [N] : *FOURC > `[command]`* [parameters]
* Verification : [condition]
* Safety : [warning]
"""

# Casual/general prompt for non-technical questions
ROUTING_PROMPT = """
You are a helpful assistant for users of a synchrotron beamline.

Answer the question clearly and concisely using information from the reference if available.

If the question is casual or general (e.g., "Where is my data?"), do not format your answer as a step-by-step instruction.

Do not fabricate information beyond the reference.

### Reference:
{context}

### Question:
{question}
"""

# Enhanced classifier using keyword rules and content analysis
def is_technical_question(q: str) -> bool:
    """
    Determines if a question requires technical procedure steps.
    Returns True for technical questions, False for general inquiries.
    """
    TECHNICAL_KEYWORDS = [
        "how to", "change temperature", "process", "run", "open", "spec", "import", 
        "beam dump", "fourc", "procedure", "command", "execute", "setup", 
        "calibrate", "align", "configure", "mount", "initialize", "steps"
    ]
    
    # Check for explicit technical terms
    if any(keyword in q.lower() for keyword in TECHNICAL_KEYWORDS):
        return True
    
    # Check for implicit procedural indicators
    if q.lower().startswith(("how do i", "what is the process", "steps to")):
        return True
        
    return False

# Create FAISS vectorstore and retriever with enhanced retrieval settings
def create_vectorstore(splits, embeddings, save_path="faiss_index"):
    """
    Creates and configures a FAISS vector store optimized for technical documentation.
    Includes MMR search for diverse results and saves the index locally.
    """
    logger.info(f"Creating vector store with {len(splits)} documents...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    logger.info("Vector store created successfully")
    
    # Configure retriever with Maximum Marginal Relevance for diverse results
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,          # Return 3 documents
            "fetch_k": 15,   # Fetch 15 candidates for diversity filtering
            "lambda_mult": 0.7  # Balance between relevance and diversity
        }
    )
    
    # Save the vector store locally
    vectorstore.save_local(save_path)
    logger.info(f"Vector store saved to '{save_path}'")
    return vectorstore, retriever

# Load existing vectorstore if available
def load_vectorstore(embeddings, load_path="faiss_index"):
    """Loads an existing FAISS vector store if available."""
    if os.path.exists(load_path):
        logger.info(f"Loading existing vector store from '{load_path}'")
        try:
            vectorstore = FAISS.load_local(load_path, embeddings)
            retriever = vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": 8,
                    "fetch_k": 15,
                    "lambda_mult": 0.7
                }
            )
            return vectorstore, retriever
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
    
    logger.warning(f"No existing vector store found at '{load_path}'")
    return None, None

# Create dynamic prompt template based on question content
def get_prompt_template(question: str) -> PromptTemplate:
    """
    Selects the appropriate prompt template based on question type.
    Returns a procedural template for technical questions or a general template otherwise.
    """
    if is_technical_question(question):
        logger.debug(f"Using technical template for: {question}")
        return PromptTemplate(template=ANSWER_TEMPLATE, input_variables=["context", "question"])
    else:
        logger.debug(f"Using general template for: {question}")
        return PromptTemplate(template=ROUTING_PROMPT, input_variables=["context", "question"])

# Filter retrieved documents based on relevance and content type
def filter_documents(docs: List[Dict[str, Any]], question: str) -> List[Dict[str, Any]]:
    """
    Filters and reranks retrieved documents based on question type and document metadata.
    Prioritizes procedural content for technical questions.
    """
    if not docs:
        return []
    
    is_technical = is_technical_question(question)
    
    # Sort documents by relevance and content type
    if is_technical:
        # For technical questions, prioritize procedure documents
        docs.sort(key=lambda d: 0 if d.metadata.get("content_type") == "procedure" else 1)
    
    # Limit to the most relevant documents
    return docs[:5]