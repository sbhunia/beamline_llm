# from models.openai.query import ask_question as ask

# Routes the ask_question function to the appropriate model
def ask_question(splits, question: str, model="openai") -> str:
    if model.lower() == "openai":
        from models.openai.query import ask_question as ask
    elif model.lower() == "llama":
        from models.llama.query import ask_question as ask

    return ask(splits=splits, question=question)
