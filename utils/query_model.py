# utils/query_model.py
import os
import re
import logging
from typing import List, Tuple, Optional
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import Document
from .resources import get_prompt_template

# Configure logging
logger = logging.getLogger(__name__)

# Configuration constants
MAX_CONTEXT_LENGTH = 6000
SUPPORTED_MODELS = {
    "deepseek": "deepseek-r1:1.5b",
    "tiny": "tinyllama:latest"
}

def validate_model(model: str) -> str:
    """Validate and resolve model name from shorthand"""
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Invalid model '{model}'. Choices: {list(SUPPORTED_MODELS.keys())}")
    return SUPPORTED_MODELS[model]

def safe_get_metadata(doc) -> dict:
    """Safely retrieve metadata from Document or dict"""
    return doc.metadata if hasattr(doc, 'metadata') else doc.get('metadata', {})

def safe_get_content(doc) -> str:
    """Safely retrieve content from Document or dict"""
    return doc.page_content if hasattr(doc, 'page_content') else doc.get('page_content', '')

def filter_relevant_docs(docs: List[Document], query: str) -> List[Document]:
    """Filter documents based on relevance to query with less strict criteria"""
    # Core keyphrases for procedure identification
    procedure_keyphrases = ["FOURC >", "Step", "Verification", "Procedure:", "Cryocooler"]
    
    # Data processing and location related terms
    data_keyphrases = ["data", "process", "analyze", "measurement", "collection"]
    location_pattern = re.compile(r'lnx\d{3}|lab\d{1,3}|station\d{1,3}', re.IGNORECASE)
    
    filtered = []
    
    # Extract potential location from query
    location_match = location_pattern.search(query)
    location_term = location_match.group(0).lower() if location_match else None
    
    for doc in docs:
        content = safe_get_content(doc)
        metadata = safe_get_metadata(doc)
        content_lower = content.lower()
        
        # Check for procedure content
        is_procedure = any(kp in content for kp in procedure_keyphrases)
        
        # Check for data processing content
        is_data_related = any(kp.lower() in content_lower for kp in data_keyphrases)
        
        # Check for location match if specified in query
        has_location_match = location_term and location_term in content_lower
        
        # Accept document if it's relevant to the query
        if (is_procedure and metadata.get('content_type') == 'procedure') or \
           (is_data_related and has_location_match) or \
           (is_procedure and has_location_match):
            filtered.append(doc)
    
    return filtered

def enforce_procedure_format(response: str) -> str:
    """Enforce consistent command formatting"""
    try:
        # Format FOURC commands
        response = re.sub(r'(FOURC\s*>\s*\S+)', r'* \1 *', response)
        # Standardize step numbering
        response = re.sub(r'(\d+)(\.|\))', r'* Step \1 :', response)
        # Remove HTML tags
        return re.sub(r'<[^>]+>', '', response).strip()
    except Exception as e:
        logger.error(f"Formatting failed: {str(e)}")
        return "Response formatting error"

def validate_commands(response: str, context: str) -> bool:
    """Verify all context commands are present in response"""
    try:
        context_commands = set(re.findall(r'FOURC > \S+', context))
        response_commands = set(re.findall(r'FOURC > \S+', response))
        return response_commands.issuperset(context_commands)
    except Exception as e:
        logger.error(f"Command validation failed: {str(e)}")
        return False

def extract_location_from_query(query: str) -> Optional[str]:
    """Extract location identifier from query"""
    match = re.search(r'(lnx\d{3}|lab\d{1,3}|station\d{1,3})', query, re.IGNORECASE)
    return match.group(0) if match else None

def ask_question(
    splits: List[Document],
    question: str,
    model: str = "tiny",
    temperature: float = 0.1,
    k: int = 8
) -> Tuple[str, List[Document]]:
    """Main query handler with enhanced error handling"""
    try:
        model_name = validate_model(model)
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # Manage vector store
        if not os.path.exists("faiss_index"):
            logger.info("Initializing new FAISS index...")
            vectorstore = FAISS.from_documents(splits, embeddings)
            vectorstore.save_local("faiss_index")
        else:
            vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        # Extract location from query to improve search
        location = extract_location_from_query(question)
        search_query = question
        
        # Enhance search query with location context if available
        if location:
            search_query = f"{question} relevant to {location}"
            logger.info(f"Enhanced search query with location: {location}")
        
        # Configure retriever with relaxed filtering
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": min(k, 10),  # Increased to get more potential matches
                "lambda_mult": 0.7
                # Removed strict filter to get more results
            }
        )

        # Process documents
        raw_docs = retriever.invoke(search_query)
        filtered_docs = filter_relevant_docs(raw_docs, question)
        
        if not filtered_docs:
            # Fallback search with broader criteria
            logger.info("No direct matches found. Attempting broader search...")
            broader_query = re.sub(r'(how to|steps for|procedure for)', '', question, flags=re.IGNORECASE).strip()
            if location:
                broader_query = f"{broader_query} {location}"
                
            raw_docs = retriever.invoke(broader_query)
            filtered_docs = raw_docs[:3]  # Take top 3 results as fallback
            
            if not filtered_docs:
                return f"No matching procedures found for '{question}'. Try specifying a different location or procedure name.", []

        # Build context with length management
        context = []
        total_len = 0
        for doc in filtered_docs:
            content = safe_get_content(doc)
            if (total_len + len(content)) <= MAX_CONTEXT_LENGTH:
                context.append(content)
                total_len += len(content)
            else:
                break

        # Generate response
        llm = Ollama(
            model=model_name,
            temperature=temperature,
            repeat_penalty=1.6,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )
        
        prompt = get_prompt_template(question).format(
            context="\n\n".join(context),
            question=question
        )
        
        response = llm.invoke(prompt)
        processed_response = enforce_procedure_format(response)

        # Only validate commands if we have procedure content
        has_commands = any("FOURC >" in content for content in context)
        if has_commands and not validate_commands(processed_response, "\n".join(context)):
            processed_response = "⚠️ Procedure validation failed. Consult documentation."

        return processed_response, filtered_docs

    except Exception as e:
        logger.error(f"Query failure: {str(e)}")
        return f"System error: {str(e)}", []