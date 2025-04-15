import os
import glob
import logging
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants for document processing
PROCEDURAL_MARKERS = [
    "* Step", "FOURC >", "Procedure:", "Step 1", "1.", "2.", "Command:",
    "Verification:", "Sample:", "!!! danger", "<b><i><u>", 
    "FOURC", "command", "execute", "WARNING", "CAUTION"
]

COMMAND_PATTERNS = [
    r'FOURC\s*>\s*`?([^`\n]+)`?',  # FOURC > command
    r'```bash\n([^`]+)```',         # bash code blocks
    r'```\n([^`]+)```',             # generic code blocks
    r'\*\s*Step\s+\d+\s*:\s*(.+)'   # * Step 1: content
]

ENCODINGS_TO_TRY = ['utf-8', 'latin-1', 'utf-16', 'iso-8859-1']

@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    chunk_size_procedural: int = 6000
    chunk_size_reference: int = 3000
    chunk_overlap_procedural: int = 800
    chunk_overlap_reference: int = 500
    min_chunk_size: int = 200
    extract_commands: bool = True
    include_headers: bool = True

def detect_document_type(content: str) -> str:
    """
    Analyzes content to determine document type - procedure, reference, or general.
    
    Returns: 
        str: "procedure", "reference", or "general"
    """
    # Count procedural markers
    marker_count = sum(1 for marker in PROCEDURAL_MARKERS if marker in content)
    
    # Detect command presence
    has_commands = any(re.search(pattern, content) for pattern in COMMAND_PATTERNS)
    
    # Determine document type
    if marker_count >= 2 or has_commands:
        return "procedure"
    elif "## " in content or "### " in content:
        return "reference"
    else:
        return "general"

def extract_commands(content: str) -> List[str]:
    """
    Extracts FOURC commands and other executable instructions from content.
    
    Returns:
        List[str]: Extracted commands
    """
    commands = []
    for pattern in COMMAND_PATTERNS:
        for match in re.finditer(pattern, content):
            cmd = match.group(1).strip()
            if cmd and len(cmd) < 200:  # Avoid capturing large blocks
                commands.append(cmd)
    return commands

def get_optimized_splitter(content: str, config: ProcessingConfig) -> RecursiveCharacterTextSplitter:
    """
    Creates a context-aware text splitter optimized for the document type.
    
    Args:
        content: Document content
        config: Processing configuration
        
    Returns:
        RecursiveCharacterTextSplitter: Configured text splitter
    """
    doc_type = detect_document_type(content)
    
    return RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size_procedural if doc_type == "procedure" else config.chunk_size_reference,
        chunk_overlap=config.chunk_overlap_procedural if doc_type == "procedure" else config.chunk_overlap_reference,
        separators=["\n\n## ", "\n\n### ", "\n\n#### ", "\n\n", "\n", " "],
        keep_separator=True,
        add_start_index=True,
        length_function=len,
        is_separator_regex=False
    )

def enhance_metadata(doc: Document, file_path: str, doc_type: str, 
                     headers: Dict[str, str], commands: List[str]) -> Document:
    """
    Enhances document metadata with rich context information.
    
    Args:
        doc: The document to enhance
        file_path: Source file path
        doc_type: Detected document type
        headers: Extracted headers
        commands: Extracted commands
        
    Returns:
        Document: Enhanced document
    """
    # Base metadata
    doc.metadata.update({
        "source": os.path.basename(file_path),
        "file_path": file_path,
        "content_type": doc_type,
        "doc_length": len(doc.page_content)
    })
    
    # Add header information if available
    if headers:
        doc.metadata.update(headers)
        
    # Add commands for procedural documents
    if commands and doc_type == "procedure":
        doc.metadata["commands"] = commands
        doc.metadata["command_count"] = len(commands)
    
    return doc

def process_file(file_path: str, config: ProcessingConfig) -> List[Document]:
    """
    Processes a single file into optimized document chunks.
    
    Args:
        file_path: Path to file
        config: Processing configuration
        
    Returns:
        List[Document]: Processed document chunks
    """
    # Try multiple encodings
    content = None
    for encoding in ENCODINGS_TO_TRY:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if not content:
        logger.error(f"Failed to load {file_path} with all encodings")
        return []

    # Detect document type
    doc_type = detect_document_type(content)
    logger.info(f"Processing {file_path} as {doc_type} document")
    
    # Extract commands if needed
    commands = extract_commands(content) if config.extract_commands else []
    
    # Process with header splitting if document has headers
    documents = []
    
    # Use header splitter for structured documents
    if config.include_headers and ("# " in content or "## " in content):
        header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"), ("##", "Header 2"), 
                ("###", "Header 3"), ("####", "Header 4")
            ]
        )
        
        # Split by markdown headers first
        header_chunks = header_splitter.split_text(content)
        
        for chunk in header_chunks:
            # Create header metadata
            headers = {k: v for k, v in chunk.metadata.items() if k.startswith("Header")}
            
            # Skip tiny chunks
            if len(chunk.page_content) < config.min_chunk_size:
                continue
                
            # Further split long chunks
            splitter = get_optimized_splitter(chunk.page_content, config)
            sub_chunks = splitter.split_documents([chunk])
            
            # Enhance each chunk with metadata
            for sub_chunk in sub_chunks:
                enhanced_doc = enhance_metadata(
                    sub_chunk, file_path, doc_type, headers, 
                    extract_commands(sub_chunk.page_content)
                )
                documents.append(enhanced_doc)
    else:
        # Direct splitting for unstructured documents
        splitter = get_optimized_splitter(content, config)
        chunks = splitter.split_text(content)
        
        for chunk in chunks:
            if len(chunk) < config.min_chunk_size:
                continue
                
            doc = Document(page_content=chunk)
            enhanced_doc = enhance_metadata(
                doc, file_path, doc_type, {}, 
                extract_commands(chunk)
            )
            documents.append(enhanced_doc)
    
    logger.info(f"Created {len(documents)} chunks from {file_path}")
    return documents

def load_documents(docs_dir: str, config: Optional[ProcessingConfig] = None) -> List[Document]:
    """
    Loads and processes technical documentation with enhanced context handling.
    
    Args:
        docs_dir: Directory containing documentation
        config: Processing configuration
        
    Returns:
        List[Document]: Processed document chunks
    """
    if config is None:
        config = ProcessingConfig()
        
    documents = []
    file_patterns = ["**/*.md", "**/*.txt", "**/*.rst"]
    
    for pattern in file_patterns:
        files = glob.glob(os.path.join(docs_dir, pattern), recursive=True)
        logger.info(f"Found {len(files)} files matching pattern {pattern}")
        
        for file_path in files:
            try:
                file_documents = process_file(file_path, config)
                documents.extend(file_documents)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {str(e)}")
                continue

    logger.info(f"Processed {len(documents)} total document chunks")
    return documents

# Main function to run processing directly
def process_directory(input_dir: str, config: Optional[ProcessingConfig] = None) -> List[Document]:
    """
    Process all documents in a directory with enhanced contextualization.
    
    Args:
        input_dir: Directory containing documentation
        config: Processing configuration
        
    Returns:
        List[Document]: All processed documents
    """
    if not os.path.exists(input_dir):
        logger.error(f"Directory {input_dir} does not exist")
        return []
        
    logger.info(f"Starting document processing from {input_dir}")
    documents = load_documents(input_dir, config)
    logger.info(f"Completed processing with {len(documents)} total chunks")
    return documents