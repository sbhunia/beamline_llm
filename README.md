# Beamline LLM

## Introduction

Beamline LLM is ...

This `README.MD` file will be expanded on later.


## Project Structure

```
beamline-llm/
├─ 🗄️docs/
├─ 📁models/
│  ├─ 📁llama/
│  │  ├─ 📄query.py
│  ├─ 📁openai/
│  │  ├─ 📄query.py
├─ 📁utils/
│  ├─ 📄preprocess.py
│  ├─ 📄query_model.py
│  ├─ 📄resources.py
├─ 📃.env
├─ 📜.gitignore
├─ 📄app.py
├─ 📜README.md
```

### Environment Variables

Two environment variables are necessary (in the `.env` file):

 - `OPENAI_API_KEY`: This should contain your OpenAI API key if  you intend on using the OpenAI model.
 - `MARKDOWN_DOCS_DIR`: This should specify the directory of the docs the model will use for RAG relative to the location of the `app.py` file.
   - By default it is recommended to set this equal to `./docs`

A properly formatted .env file will look like this:

```bash
OPENAI_API_KEY=sk-...7FeO
MARKDOWN_DOCS_DIR=./docs
```


