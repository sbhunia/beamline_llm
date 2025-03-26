### IMPORTS ###
import os
import sys

# Custom modules
from utils.preprocess import load_docs
from utils.query_model import ask_question
from utils.config import MARKDOWN_DOCS_DIR, DEFAULT_MODEL

# From Chainlit
import chainlit as cl
from chainlit.message import Message
from chainlit.input_widget  import Select
### END IMPORTS ###


sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Call utils.preprocess.load_docs
splits = load_docs(MARKDOWN_DOCS_DIR)

@cl.on_chat_start
async def start():
    await Message("Welcome! The default model is OpenAI's GPT-4").send()

    selected = await cl.ChatSettings(
        [
            Select(id="model", label="Model", values=["openai", "llama"], initial_index=0)
        ]
    ).send()

    cl.user_session.set("model", DEFAULT_MODEL)

@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("model", settings["model"])
    print("on_settings_update", settings)
    print("user_model:", cl.user_session.get("model"))


@cl.on_message
async def main(message):
    # Specify the question from the user
    Q = message.content

    # Get user selected model from UI
    M = cl.user_session.get("model")

    # Call utils.query_model.ask_question
    #   This performs all of the fancy LLM stuff
    # NOTE: Specify model= as 'openai' or 'llama'
    A, source_documents = ask_question(splits=splits, question=Q, model=M)

    # Prepare the response
    doc_sources = [doc.metadata['source'].split('/')[-1] for doc in source_documents]
    response = f"{A}\n\nSource Documents: "

    for i, doc in enumerate(doc_sources):
        url = f"https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/docs/{doc}"
        response += f"[{doc}]({url})"
        if i != len(doc_sources) - 1:
            response += ", "

    # Send the response back to the user and wait for the next message
    await cl.Message(content=response).send()

if __name__ == "__main__":
    cl.run()