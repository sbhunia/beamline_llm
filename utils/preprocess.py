import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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
    failed = []
    markdown_files = glob.glob(f"{docs_dir}/**/*.md", recursive=True)
    print(f"Found {len(markdown_files)} markdown files", end="\n[")

    for file_path in markdown_files:
        base_name = os.path.basename(file_path).lower()
        try:
            # Try UTF-8 encoding first
            loader = TextLoader(file_path, encoding="utf-8")
            file_docs = loader.load()

            docs.extend(file_docs)
            print(".", end="")
        except Exception as e:
            try:
                loader = TextLoader(file_path, encoding="latin-1") 
                file_docs = loader.load()

                docs.extend(file_docs)
                print(":", end="")
            except Exception as e2:
                print("e", end="")
                failed.append(file_path)
    print("]")


    if failed:
        print(f"\nFailed to load {len(failed)} files:\n{failed}")


    print(f"\nSuccessfully loaded {len(docs)} documents total")


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