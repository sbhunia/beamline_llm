from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral:instruct")
print(llm.invoke("Explain what a beamline is in one sentence.").content)