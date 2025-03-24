from langchain_community.vectorstores import FAISS

ANSWER_TEMPLATE = """
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

def create_vectorstore(splits, embeddings):
    print("Creating vector store...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    print("Vector store created successfully")

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5, "fetch_k": 12}
    )

    vectorstore.save_local("faiss_index")

    return vectorstore, retriever
