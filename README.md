# Beamline LLM Web Application

This project is a web application that (currently, subject to change) utilizes Chainlit to provide an interactive interface for querying a RAG LLM that specifically only uses documentation from the [CHESS ID4B - QM2 Beamline Documentation](https://suchismitasarker.github.io/CHESS-ID4B-QM2/). The application processes user questions and retrieves relevant information using the language model.

## TODO List

[ ] Allow OpenAI implementation to use prompt template (`models/openai/query.py`)
[X] Fix bug where 'models' module not found (`utils/query_model.py`)

[X] Print links to source files used with nice formatting (`app.py`)
[ ] Fix bug where Chainlit text box pastes double (`app.py`?)
[ ] Change intro message depending on what model is default (`app.py`)
[X] Add a list of models available (`utils/config.py`)



## Project Structure

```
beamline-llm/
├─ 🗄️docs/
├─ 📁models/
│  ├─ 📁llama/
│  │  ├─ 📄query.py
│  └─ 📁openai/
│     └─ 📄query.py
├─ 📁utils/
│  ├─ 📄preprocess.py
│  ├─ 📄query_model.py
│  └─ 📄resources.py
├─ 📃.env
├─ 📜.gitignore
├─ 📄app.py
└─ 📜README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd beamline_llm
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   Ensure that `requirements.txt` includes Chainlit and other necessary libraries. Install them using:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root and add the necessary environment variables, such as:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   MARKDOWN_DOCS_DIR=<path_to_markdown_files>
   ```

## Usage

1. **Run the Application**
   Start the Chainlit server to launch the web application:
   ```bash
   chainlit run app.py
   ```

2. **Access the Web Interface**
   Open your web browser and navigate to `http://localhost:8000` to interact with the application.

## Features

- Load and process markdown documents for embedding.
- Query a language model with user-defined questions.
- Display relevant answers and source documents in the web interface.
