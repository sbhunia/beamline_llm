import os
import glob
import logging
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROCEDURAL_MARKERS = [
    "* Step", "FOURC >", "Procedure:", "Step 1", "1.", "2.", "Command:",
    "Verification:", "Sample:", "!!! danger", "<b><i><u>"
]
ENCODINGS_TO_TRY = ['utf-8', 'latin-1', 'utf-16', 'iso-8859-1']

def get_optimized_splitter(content: str) -> RecursiveCharacterTextSplitter:
    """Create context-aware text splitter based on document content"""
    is_procedural = any(marker in content for marker in PROCEDURAL_MARKERS)
    
    return RecursiveCharacterTextSplitter(
        chunk_size=6000 if is_procedural else 3000,
        chunk_overlap=800 if is_procedural else 500,
        separators=["\n\n## ", "\n\n### ", "\n\n#### ", "\n\n", "\n", " "],
        keep_separator=True,
        add_start_index=True,
        is_separator_regex=False
    )

def load_documents(docs_dir: str) -> List[Document]:
    """Load and process technical documentation with enhanced metadata handling"""
    documents = []
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header 1"), ("##", "Header 2"), 
            ("###", "Header 3"), ("####", "Header 4")
        ]
    )

    for file_path in glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True):
        try:
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
                continue

            # Split by markdown headers first
            header_chunks = header_splitter.split_text(content)
            
            for chunk in header_chunks:
                # Determine content type
                is_procedure = any(marker in chunk.page_content for marker in PROCEDURAL_MARKERS)
                
                # Split using optimized splitter
                splitter = get_optimized_splitter(chunk.page_content)
                sub_chunks = splitter.split_documents([chunk])
                
                # Add metadata
                for sub_chunk in sub_chunks:
                    sub_chunk.metadata.update({
                        "source": os.path.basename(file_path),
                        "file_path": file_path,
                        "content_type": "procedure" if is_procedure else "reference",
                        **chunk.metadata
                    })
                    
                documents.extend(sub_chunks)

        except Exception as e:
            logger.error(f"Failed to process {file_path}: {str(e)}")
            continue

    logger.info(f"Processed {len(documents)} document chunks")
    return documents  # Ensure this return statement exists