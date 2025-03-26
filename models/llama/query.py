from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Import create_vectorstore and the ANSWER_TEMPLATE string 
#   from the utils.resources module
from utils.resources import create_vectorstore, ANSWER_TEMPLATE
from utils.config import TEMPERATURE


# Create the embeddings using the splits, create the 
#   retriever, return the retriever for later use
def create_embedding(splits: list) -> FAISS:
    # OLlama embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Create the vectorstore and retriever using the function
    #   defined in the resources module
    vectorstore, retriever = create_vectorstore(splits, embeddings)
    
    return retriever, vectorstore

# Create the model using the OLlama model and the RAG prompt
#   template, return the model for later use
def create_model():
    rag_prompt = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)
    print("\nCreating model...")
    llm = ChatOllama(model="deepseek-r1:1.5b", temperature=TEMPERATURE)  # Deepseek(?) model used 
    print("Model created successfully")

    return llm, rag_prompt

def ask_question(splits, question: str):
    # Call the previous functions in this file
    #   to get the retriever and model
    retriever, vectorstore = create_embedding(splits)
    llm, rag_prompt = create_model()
    
    # Doc formatting helper function
    def format_docs(docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    # Build the RAG chain
    print("\nBuilding RAG chain...")
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    # NOTE: Does this need to be saved here specifically?
    #   Otherwise we can remove this line.
    vectorstore.save_local("faiss_index")

    # Retrieve RAG docs for response
    print("\nRetrieving docs...")
    retrieved_docs = retriever.get_relevant_documents(question)

    # Get response
    print("\nGetting response...")
    response = rag_chain.invoke(question)
    print("Response received!")

    return response, retrieved_docs
