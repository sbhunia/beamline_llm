### IMPORTS ###
import os
import sys
import time
import re
from typing import List, Dict, Any, Tuple

# Custom modules
from utils.preprocess import load_docs
from utils.query_model import ask_question
from utils.config import MARKDOWN_DOCS_DIR, DEFAULT_MODEL, MODEL_OPTIONS, MODEL_NAMES

# From Chainlit
import chainlit as cl
from chainlit.message import Message
from chainlit.input_widget import Select, Slider, Switch
from chainlit.element import Element
### END IMPORTS ###


sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Load documents at startup
print("🔄 Loading and processing documents...")
splits = load_docs(MARKDOWN_DOCS_DIR)
print(f"✅ Loaded {len(splits)} document chunks")

def format_source_content(source_docs: List[Any]) -> str:
    """Format source document content for debug view."""
    if not source_docs:
        return "No source documents retrieved."
    
    formatted = ""
    for i, doc in enumerate(source_docs):
        source = doc.metadata.get('source', 'unknown').split('/')[-1]
        headers = []
        for key in doc.metadata:
            if key.startswith('header') and doc.metadata[key]:
                headers.append(f"{key}: {doc.metadata[key]}")
        
        header_info = " | ".join(headers) if headers else "No header metadata"
        
        formatted += f"📄 **Source {i+1}**: {source}\n"
        formatted += f"**Context**: {header_info}\n"
        formatted += f"**Content**:\n```markdown\n{doc.page_content[:400]}...\n```\n\n"
    
    return formatted

@cl.on_chat_start
async def start():
    # Welcome message
    welcome_msg = f"""# 🧪 CHESS ID4B-QM2 Beamline Assistant

Welcome! This assistant helps you with beamline operation procedures by retrieving information from technical documentation.

- Ask about step-by-step procedures
- Get command syntax for the beamline interface
- Find temperature control information

Default model: **{MODEL_NAMES[DEFAULT_MODEL]}**
"""
    await Message(content=welcome_msg).send()

    # Initialize settings
    selected = await cl.ChatSettings(
        [
            Select(
                id="model", 
                label="LLM Model", 
                values=MODEL_OPTIONS, 
                initial_index=0
            ),
            Slider(
                id="temperature",
                label="Temperature",
                initial=0.1,
                min=0,
                max=1,
                step=0.1,
                tooltip="Lower values = more deterministic responses"
            ),
            Slider(
                id="k_docs",
                label="Retrieved Documents",
                initial=8,
                min=3,
                max=15,
                step=1,
                tooltip="Number of documents to retrieve"
            ),
            Switch(
                id="show_debug",
                label="Show Debug Info",
                initial=False
            )
        ]
    ).send()

    cl.user_session.set("model", DEFAULT_MODEL)
    cl.user_session.set("temperature", 0.1)
    cl.user_session.set("k_docs", 8)
    cl.user_session.set("show_debug", False)

@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("model", settings["model"])
    cl.user_session.set("temperature", float(settings["temperature"]))
    cl.user_session.set("k_docs", int(settings["k_docs"]))
    cl.user_session.set("show_debug", settings["show_debug"])
    print(f"🔄 Settings updated: {settings}")


@cl.on_message
async def main(message):
    try:
        # Start processing indicator
        processing_msg = cl.Message(content="🔄 Processing your request...")
        await processing_msg.send()
        
        start_time = time.time()
        
        print(f"▶️ User input: {message.content}")
        
        # Get session settings
        question = message.content
        model = cl.user_session.get("model")
        temperature = cl.user_session.get("temperature")
        k_docs = cl.user_session.get("k_docs")
        show_debug = cl.user_session.get("show_debug")
        
        print(f"🤖 Using model: {model}, temp: {temperature}, k: {k_docs}")

        # Call the query function with parameters
        answer, source_documents = ask_question(
            splits=splits, 
            question=question, 
            model=model,
            temperature=temperature,
            k=k_docs
        )

        # Process response
        if "</think>" in answer:
            thinking = re.search(r"<think>(.*?)</think>", answer, re.DOTALL)
            thinking_content = thinking.group(1).strip() if thinking else ""
            answer = answer.split("</think>")[-1].strip()
        else:
            thinking_content = ""

        print(f"✅ Response received in {time.time() - start_time:.2f}s")
        
        # Prepare source document links
        doc_sources = []
        seen_sources = set()
        for doc in source_documents:
            source = doc.metadata.get('source', '').split('/')[-1]
            if source and source not in seen_sources:
                doc_sources.append(source)
                seen_sources.add(source)

        # Format response
        response = f"{answer}\n\n"
        
        # Add source documents
        if doc_sources:
            response += f"📄 **Source Documents:**\n"
            for doc in doc_sources:
                url = f"https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/docs/{doc}"
                response += f"- [{doc}]({url})\n"

        # Update the processing message with the final response
        await processing_msg.update(content=response)
        
        # Add debug information if enabled
        if show_debug:
            debug_response = f"### 🔍 Debug Information\n\n"
            debug_response += f"**Query Time**: {time.time() - start_time:.2f}s\n"
            debug_response += f"**Model**: {model}\n"
            debug_response += f"**Temperature**: {temperature}\n"
            debug_response += f"**Retrieved Documents**: {len(source_documents)}/{k_docs}\n\n"
            
            if thinking_content:
                debug_response += f"**LLM Thinking Process**:\n```\n{thinking_content}\n```\n\n"
            
            debug_response += f"**Retrieved Source Content**:\n{format_source_content(source_documents)}"
            
            await cl.Message(content=debug_response).send()

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {str(e)}\n{error_details}")
        await cl.Message(content=f"⚠️ Error: {str(e)}").send()


if __name__ == "__main__":
    cl.run()