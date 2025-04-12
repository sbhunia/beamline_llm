from langchain_community.vectorstores import FAISS

# Improved prompt template to ensure exact reproduction of document content
ANSWER_TEMPLATE = """
### Role:
You are a highly accurate technical assistant for beamline cryo systems. You MUST reproduce the exact steps from the reference documents without any creative additions or simplifications.

### Goal:
Provide crystal-clear and strictly step-by-step instructions extracted VERBATIM from the reference materials. The output must:
- Copy the exact numbered steps, format, and structure from the source material
- Include all command lines exactly as written (e.g., `FOURC > prepN2_low`)
- Copy all physical actions (e.g., open/close valves) exactly as described
- Preserve all timing/waiting/stabilization periods mentions
- Maintain the exact markdown formatting, including asterisks, bullet points, and numbering
- **NEVER infer, summarize, abbreviate, or add steps not explicitly in the research**
- **NEVER change temperature values or other numerical parameters**

If the content is unclear or incomplete, respond with: "The research did not contain enough details to answer this question reliably."

### Reference:
{context}

### Question:
{question}

### Think Step-by-Step:
1. Identify which section in the reference materials answers the question directly
2. Copy that section's formatting and structure exactly, preserving all numbering/bullets
3. Double-check that you've included ALL commands prefixed with FOURC >
4. Verify you've maintained all temperature values and numerical parameters exactly
5. Ensure all waiting periods and stabilization steps are preserved

### Output Format:
Respond using the EXACT same formatting as shown in the original instructions.
If the original uses a numbered list with asterisks like:
* Step 1 : *FOURC > *`command`
* Step 2 : *description*

Then your response MUST follow this EXACT pattern.
"""

def create_vectorstore(splits, embeddings, save_path="faiss_index"):
    """
    Create a FAISS vector store from a list of split documents and return a retriever for querying.

    Args:
        splits (List[Document]): The text chunks created from the documentation.
        embeddings (Embeddings): Embedding model to use for vectorizing documents.
        save_path (str): Directory path to save the FAISS index locally.

    Returns:
        vectorstore (FAISS): The FAISS vector store object.
        retriever (BaseRetriever): A retriever object to use for semantic search.
    """
    print("Creating vector store...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    print("Vector store created successfully")

    # Improve retrieval with more relevant documents and lower diversity
    # to prioritize finding the exact procedure
    retriever = vectorstore.as_retriever(
        search_type="mmr",  # Maximal Marginal Relevance
        search_kwargs={
            "k": 8,         # Increased from 5 to get more context
            "fetch_k": 15,  # Increased from 12
            "lambda_mult": 0.7  # Higher value (0-1) means more relevance, less diversity
        }
    )

    vectorstore.save_local(save_path)
    print(f"Vector store saved to '{save_path}'")

    return vectorstore, retriever