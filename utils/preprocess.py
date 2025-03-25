import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Provides the appropriate splitter based on the length of the document
#   This is to ensure that the document is split into chunks that are not too large
def get_dynamic_splitter(doc_length: int) -> RecursiveCharacterTextSplitter:
    if doc_length <= 1000:
        return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    elif doc_length <= 2000:
        return RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    elif doc_length <= 4000:
        return RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400)
    else:
        return RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=500)

def load_docs(docs_dir: str) -> list:
    docs = []
    failed = []  # Keep track of failed files to print for debugging later
    markdown_files = glob.glob(f"{docs_dir}/**/*.md", recursive=True)
    print(f"Found {len(markdown_files)} markdown files", end="\n[")

    for file_path in markdown_files:
        try:
            # Try UTF-8 encoding first
            loader = TextLoader(file_path, encoding="utf-8")
            file_docs = loader.load()

            docs.extend(file_docs)
            print(".", end="")  # Print '.' for successful load
        except Exception as e:
            try:
                # Try Latin-1 if UTF-8 fails
                loader = TextLoader(file_path, encoding="latin-1") 
                file_docs = loader.load()

                docs.extend(file_docs)
                print(":", end="")  # Print ':' for Latin-1 successful load
            except Exception as e2:
                print("e", end="")  # Print 'e' for failed load
                failed.append(file_path)  # Add file name to failed list for debugging later
    print("]")


    if failed:  # If failed files exist, print them for debugging
        print(f"\nFailed to load {len(failed)} files:\n{failed}")


    print(f"\nSuccessfully loaded {len(docs)} documents total")


    # Get split documents with dynamic splitting
    splits = []
    for doc in docs:
        splitter = get_dynamic_splitter(len(doc.page_content))
        splits.extend(splitter.split_documents([doc]))


    print(f"Created {len(splits)} text chunks for embedding")

    return splits

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    docs_dir = os.getenv("MARKDOWN_DOCS_DIR")
    splits = load_docs(docs_dir)
    print(f"Received {len(splits)} text chunks for embedding")