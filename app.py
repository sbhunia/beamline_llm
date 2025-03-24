### START IMPORTS ###
# OS Imports
from dotenv import load_dotenv, find_dotenv
import os

# Workspace Imports
from utils.preprocess import load_docs
from utils.query_model import ask_question

### END IMPORTS ###


### LOAD ENVIRONMENT VARIABLES ###
load_dotenv(find_dotenv())

### LOAD DIRECTORY FOR MARKDOWN FILES ###
docs_dir = os.getenv("MARKDOWN_DOCS_DIR")
### END ###

# Call utils.preprocess.load_docs
#   This loads in the MD documents and chunks them to prepare for embedding
splits = load_docs(docs_dir)
print(f"Received {len(splits)} text chunks for embedding")


if __name__ == "__main__":
    ### LOAD OPENAI KEY ###
    openai_api_key = os.getenv("OPENAI_API_KEY")
    ### END ###

    # Specify sample question
    Q = "How to change temperature from 300K to 13K?"

    # Call utils.query_model.ask_question
    #   This performs all of the fancy LLM stuff
    # NOTE: Specify model= as 'openai' or 'llama' depending on which model you want to use
    A, source_documents = ask_question(splits=splits, question=Q, model="llama")

    # View for debugging
    # NOTE: The below commented out code has excessive output IMO
    # for i, doc in enumerate(source_documents):
    #     print(f"Document {i} content:\n{doc.page_content}\n")
    #     print(f"Source: {doc.metadata}\n")
    
    doc_sources = [doc.metadata['source'].split('/')[-1] for doc in source_documents]
    print(f"\n\nA total of {len(source_documents)} were retrieved for the response.")
    print(f"These documents were:\n{doc_sources}")

    # Print Question and Answer
    print(f"\n\nQuestion: {Q}")
    print(f"Answer: {A}")
