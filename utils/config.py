import os
from dotenv import load_dotenv, find_dotenv

### LOAD ENVIRONMENT VARIABLES ###
load_dotenv(find_dotenv())

### LOAD DIRECTORY FOR MARKDOWN FILES ###
MARKDOWN_DOCS_DIR = os.getenv("MARKDOWN_DOCS_DIR")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_OPTIONS = ["llama", "openai"]
MODEL_NAMES = {"llama": "Meta's OLlama", "openai": "OpenAI's GPT-4"}
DEFAULT_MODEL = "llama"  # OR = MODEL_OPTIONS[0]
TEMPERATURE = 0.4