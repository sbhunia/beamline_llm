import os
from dotenv import load_dotenv, find_dotenv

### LOAD ENVIRONMENT VARIABLES ###
load_dotenv(find_dotenv())

### LOAD DIRECTORY FOR MARKDOWN FILES ###
MARKDOWN_DOCS_DIR = os.getenv("MARKDOWN_DOCS_DIR")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "llama"
TEMPERATURE = 0.4