import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# STEP 1: Load each markdown file individually with error handling and special treatment
docs = []
large_docs = []  # For storing temp.md and other large documents
markdown_files = glob.glob("./docs/**/*.md", recursive=True)
print(f"Found {len(markdown_files)} markdown files")

for file_path in markdown_files:
    base_name = os.path.basename(file_path).lower()
    try:
        # Try UTF-8 encoding first
        loader = TextLoader(file_path, encoding="utf-8", encoding_errors="replace")
        file_docs = loader.load()
        
        # Special handling for temperature-related files
        if base_name == "temp.md" or "temperature" in base_name or "cryo" in base_name:
            large_docs.extend(file_docs)
            print(f"✓ Loaded {file_path} as large document for special handling")
        else:
            docs.extend(file_docs)
            print(f"✓ Loaded {file_path}")
    except Exception as e:
        print(f"! Error with {file_path}: {str(e)}")
        try:
            loader = TextLoader(file_path, encoding="latin-1") 
            file_docs = loader.load()
            
            # Special handling for temperature-related files
            if base_name == "temp.md" or "temperature" in base_name or "cryo" in base_name:
                large_docs.extend(file_docs)
                print(f"✓ Loaded {file_path} as large document with fallback encoding")
            else:
                docs.extend(file_docs)
                print(f"✓ Loaded {file_path} with fallback encoding")
        except Exception as e2:
            print(f"✕ Could not load {file_path}: {str(e2)}")

print(f"\nSuccessfully loaded {len(docs) + len(large_docs)} documents total")
print(f"Standard documents: {len(docs)}")
print(f"Large special documents: {len(large_docs)}")

# STEP 2: Split documents with different strategies
# Standard docs - moderate chunks
standard_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
standard_splits = standard_splitter.split_documents(docs)

# Large docs - much larger chunks to preserve instructions
large_splitter = MarkdownTextSplitter(chunk_size=6000, chunk_overlap=500)  # Much larger chunks for temp.md
large_splits = large_splitter.split_documents(large_docs)

# Combine all splits
all_splits = standard_splits + large_splits
print(f"Created {len(all_splits)} text chunks for embedding")
print(f"- {len(standard_splits)} standard chunks")
print(f"- {len(large_splits)} large document chunks")

# STEP 3: Initialize Ollama embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# STEP 4: Create FAISS vector store
print("Creating vector store...")
vectorstore = FAISS.from_documents(all_splits, embeddings)
print("Vector store created successfully")

# STEP 5: Create retriever and initialize local LLM
# Use search_type="mmr" for Maximum Marginal Relevance to get diverse but relevant results
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 12}
)

llm = ChatOllama(model="deepseek-r1:1.5b", temperature=0.1)

# STEP 6: Define improved RAG prompt template
answer_template = """
### Role:
You are a highly accurate technical assistant for beamline cryo systems.

### Goal:
Provide crystal-clear and strictly step-by-step instructions extracted only from the reference materials. The output should:
- Mirror the structure from the research content
- Include all command lines (e.g., `FOURC > prepN2_low`)
- Mention physical actions (e.g., open/close valves)
- Emphasize timing/waiting/stabilization periods
- Include diagrams only if explicitly mentioned
- NEVER infer or add steps not included in the research

If the content is unclear or incomplete, say: "The research did not contain enough details to answer this question reliably."

### Reference:
{context}

### Question:
{question}

### Output Format:
Respond using a numbered list of steps, as shown in the original instructions.
Use Markdown for bold commands, italics for descriptions, and include warnings when appropriate.
"""


rag_prompt = ChatPromptTemplate.from_template(answer_template)

# Helper function to format retrieved documents with better separation
def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

# STEP 7: Build the RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Save the vector store for future use
vectorstore.save_local("faiss_index")
print("Vector store saved to 'faiss_index' directory")

# Function to query the RAG system with debug info
def ask_rag(question):
    print(f"\nQuestion: {question}")
    
    # Debug: Print retrieved documents before sending to LLM
    retrieved_docs = retriever.get_relevant_documents(question)
    print(f"Retrieved {len(retrieved_docs)} relevant documents")
    
    # Print first 200 characters of each retrieved document to verify content
    for i, doc in enumerate(retrieved_docs):
        print(f"Doc {i+1} snippet: {doc.page_content[:200]}...")
    
    response = rag_chain.invoke(question)
    print(f"Answer: {response}")
    return response

# Example question
if __name__ == "__main__":
    ask_rag("How to change temperature from 300K to 13K?.")