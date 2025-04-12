import os
import glob
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

def get_improved_splitter(doc_content: str, file_path: str) -> RecursiveCharacterTextSplitter:
    """
    Create a splitter optimized for technical documentation with numbered steps.
    
    Args:
        doc_content: The content of the document to split
        file_path: The path to the document file
    
    Returns:
        A text splitter optimized for the document's content type
    """
    # Check if document contains procedural steps (likely to have asterisks and numbers)
    contains_steps = any(marker in doc_content for marker in ["* Step", "1.", "2.", "Step 1", "FOURC >"])
    
    if contains_steps:
        # For procedural documents, use larger chunks with more overlap
        # to ensure complete procedures stay together
        return RecursiveCharacterTextSplitter(
            chunk_size=8000,                # Large chunk size to keep procedures intact
            chunk_overlap=1000,             # Significant overlap for context
            separators=["\n\n\n", "\n\n", "\n", " ", ""],  # Split on larger paragraph breaks first
            keep_separator=True,
            add_start_index=True,
        )
    else:
        # For reference documents, use moderate chunking
        return RecursiveCharacterTextSplitter(
            chunk_size=4000, 
            chunk_overlap=400,
            separators=["\n\n\n", "\n\n", "\n", " ", ""],
            keep_separator=True,
            add_start_index=True,
        )

def load_docs(docs_dir: str) -> list:
    """
    Load and split documents with improved processing for technical documentation.
    
    Args:
        docs_dir: Directory containing markdown documentation
        
    Returns:
        List of document chunks optimized for retrieval
    """
    docs = []
    failed = []
    markdown_files = glob.glob(os.path.join(docs_dir, '**', '*.md'), recursive=True)
    print(f"Found {len(markdown_files)} markdown files", end="\n[")

    for file_path in markdown_files:
        try:
            # Try UnstructuredMarkdownLoader first which preserves markdown structure
            try:
                loader = UnstructuredMarkdownLoader(file_path)
                file_docs = loader.load()
                docs.extend(file_docs)
                print("u", end="")  # 'u' for unstructured loader
            except:
                # Fall back to TextLoader if UnstructuredMarkdownLoader fails
                loader = TextLoader(file_path, encoding="utf-8")
                file_docs = loader.load()
                docs.extend(file_docs)
                print(".", end="")
        except Exception:
            try:
                # Try with different encoding
                loader = TextLoader(file_path, encoding="latin-1")
                file_docs = loader.load()
                docs.extend(file_docs)
                print(":", end="")
            except Exception:
                print("e", end="")
                failed.append(file_path)
    print("]")

    if failed:
        print(f"\nFailed to load {len(failed)} files:\n{failed}")

    print(f"\nSuccessfully loaded {len(docs)} documents total")

    # First use header-based splitting to preserve document structure
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "header1"),
            ("##", "header2"),
            ("###", "header3"),
            ("####", "header4"),
        ]
    )
    
    splits = []
    for doc in docs:
        # Read document content to determine appropriate splitter
        content = doc.page_content
        file_path = doc.metadata.get('source', '')
        
        # Try header-based splitting first
        try:
            header_splits = header_splitter.split_text(content)
            # For each header section, apply content-aware splitting
            for header_doc in header_splits:
                splitter = get_improved_splitter(header_doc.page_content, file_path)
                # Preserve header information in metadata
                sub_splits = splitter.split_documents([header_doc])
                
                # Transfer header metadata to all sub_splits
                for split in sub_splits:
                    # Add header info to metadata
                    for key, value in header_doc.metadata.items():
                        if key.startswith('header'):
                            split.metadata[key] = value
                    # Add source file info
                    split.metadata['source'] = file_path
                
                splits.extend(sub_splits)
        except:
            # If header splitting fails, use content-aware splitting directly
            splitter = get_improved_splitter(content, file_path)
            doc_splits = splitter.split_documents([doc])
            splits.extend(doc_splits)

    print(f"Created {len(splits)} text chunks optimized for accurate retrieval")

    return splits

if __name__ == "__main__":
    from utils.config import MARKDOWN_DOCS_DIR
    splits = load_docs(MARKDOWN_DOCS_DIR)
    print(f"Received {len(splits)} text chunks for embedding")