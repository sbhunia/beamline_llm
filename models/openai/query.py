from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# Import create_vectorstore and the ANSWER_TEMPLATE string 
#   from the utils.resources module
from utils.resources import create_vectorstore, ANSWER_TEMPLATE


# Create the embeddings using the splits, create the 
#   retriever, return the retriever for later use
def create_embedding(splits: list):
    # OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    # Create the vectorstore and retriever using the function
    #   defined in the resources module
    _, retriever = create_vectorstore(splits, embeddings)
    
    return retriever

# Create the model using the OpenAI model and the RAG prompt
#   template, return the model for later use
def create_model():
    # TODO: 'rag_prompt' is currently not used!!! implement this !!!
    rag_prompt = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)
    print("\nCreating model...")
    llm = ChatOpenAI(model="gpt-4", temperature=0.1)  # GPT-4 model used
    print("Model created successfully")

    return llm, rag_prompt

def ask_question(splits, question: str):
    # Call the previous functions in this file
    #   to get the retriever and model
    retriever = create_embedding(splits)
    llm, rag_prompt = create_model()

    print("\nRetrieving docs...")
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm, retriever, return_source_documents=True
    )

    # Get the response given the question
    print("\nGetting response...")
    response = rag_chain({"question": question, "chat_history": []})
    print("Response received!")

    # Return the answer and source documents
    return response['answer'], response['source_documents']
