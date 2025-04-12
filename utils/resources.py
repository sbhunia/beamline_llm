from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

# Strict technical template
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

# Casual/general prompt
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

# Simple classifier using keyword rules
def is_technical_question(q: str) -> bool:
    TECHNICAL_KEYWORDS = [
        "how to", "change temperature", "process", "run", "open", "spec", "import", "beam dump"
    ]
    return any(keyword in q.lower() for keyword in TECHNICAL_KEYWORDS)

# Create FAISS vectorstore and retriever
def create_vectorstore(splits, embeddings, save_path="faiss_index"):
    print("Creating vector store...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    print("Vector store created successfully")

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 8,
            "fetch_k": 15,
            "lambda_mult": 0.7
        }
    )

    vectorstore.save_local(save_path)
    print(f"Vector store saved to '{save_path}'")
    return vectorstore, retriever

# Create dynamic prompt template
def get_prompt_template(question: str) -> PromptTemplate:
    if is_technical_question(question):
        return PromptTemplate(template=ANSWER_TEMPLATE, input_variables=["context", "question"])
    else:
        return PromptTemplate(template=ROUTING_PROMPT, input_variables=["context", "question"])
