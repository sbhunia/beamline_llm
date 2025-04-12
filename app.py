import os
import sys
import time
import re
from utils.preprocess import load_documents as load_docs
from utils.query_model import ask_question
from utils.config import MARKDOWN_DOCS_DIR

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def validate_documents():
    """Ensure documents are loaded properly before starting"""
    print("\U0001F504 Loading and processing documents...")
    try:
        splits = load_docs(MARKDOWN_DOCS_DIR)
        if not splits:
            raise ValueError("No documents found in specified directory")
        if len(splits) < 10:  # Minimum expected chunks
            raise ValueError(f"Only {len(splits)} chunks found - check document processing")
        print(f"✅ Loaded {len(splits)} document chunks")
        return splits
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {str(e)}")
        print("Possible fixes:")
        print("1. Verify MARKDOWN_DOCS_DIR in config.py points to docs/")
        print("2. Check file permissions for markdown files")
        print("3. Run 'python -m utils.preprocess' to test loading")
        sys.exit(1)

# Initialize document store with validation
splits = validate_documents()

def format_source_documents(docs):
    """Format source documents with deduplication and validation"""
    output = []
    seen = set()
    for doc in docs:
        if not hasattr(doc, 'metadata'):
            continue
        source = doc.metadata.get("source", "unknown")
        if isinstance(source, str) and source not in seen:
            seen.add(source)
            output.append(f"- {os.path.basename(source)}")
    return "\n".join(output) if output else "No verified sources"

def handle_response(answer: str) -> str:
    """Sanitize and format LLM response"""
    # Remove any XML/HTML tags
    cleaned = re.sub(r'<[^>]+>', '', answer)
    # Normalize FOURC command formatting
    cleaned = re.sub(r'(FOURC\s*>\s*\S+)', r'* \1 *', cleaned)
    return cleaned.strip()

def main_loop():
    print("\n🧪 CHESS ID4B-QM2 Terminal Assistant Ready!")
    print("Type a question (or 'exit' to quit):\n")

    while True:
        try:
            question = input("> ").strip()
            if question.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            start_time = time.time()
            print("\nProcessing your question...")

            # Get response with error containment
            try:
                answer, source_docs = ask_question(
                    splits=splits,
                    question=question,
                    model="tiny",
                    temperature=0.1,
                    k=8
                )
            except Exception as e:
                answer = f"Query failed: {str(e)}"
                source_docs = []

            # Process and display results
            print("\n✅ Answer:")
            print(handle_response(answer))

            if source_docs:
                print("\n📄 Source Documents:")
                print(format_source_documents(source_docs))

            elapsed = time.time() - start_time
            print(f"\n⏱️ Completed in {elapsed:.2f} seconds\n")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\n⚠️ SYSTEM ERROR: {str(e)}")
            print("Please report this to beamline staff")

if __name__ == "__main__":
    main_loop()