# QM2 Assistant – Dual-Index RAG (Markdown + PDF)

## Folder Structure

Place your project files like this:

```
your_project/
├── app.py                  # Streamlit frontend
├── rag_engine.py           # RAG backend (dual FAISS indexes)
├── requirements.txt
├── md_files/               # ← Put all .md files here
│   ├── about.md
│   ├── beamline_basics.md
│   ├── SPEC_commands.md
│   └── ... (all 39 markdown files)
├── pdf_files/              # ← Put all .pdf files here
│   ├── 336_lakeshore (1).pdf
│   ├── CRYOCOOL-LT_G2b_MANUAL2023 (1).pdf
│   ├── SPEC manual pymca.pdf
│   └── spec Manual.pdf
├── faiss_index_md/         # Auto-created on first run
└── faiss_index_pdf/        # Auto-created on first run
```

## Setup

```bash
pip install -r requirements.txt
```

Set your Gemini API key:
```bash
export GOOGLE_API_KEY="your-key-here"
```

Or add it to `.streamlit/secrets.toml`:
```toml
GOOGLE_API_KEY = "your-key-here"
```

## Run

```bash
streamlit run app.py
```

On the first run the FAISS indexes will be built automatically.
This takes a few minutes because of PDF parsing + embedding generation.

## How It Works

### Two Separate FAISS Indexes

| Index | Source | Chunk Size | Overlap | Why |
|-------|--------|-----------|---------|-----|
| `faiss_index_md` | 39 markdown files (~130 KB) | 300 | 150 | Small, precise chunks for command lookups and step-by-step procedures |
| `faiss_index_pdf` | 4 PDF manuals (~570 pages) | 1000 | 300 | Larger chunks to keep technical context intact (specs, tables, wiring diagrams) |

### Retrieval Flow

1. User query hits **both** indexes in parallel
2. Top 6 results from each index are collected
3. Results are **deduplicated** by content hash
4. Merged results are **sorted by similarity score**
5. Top 10 chunks are sent to Gemini as context

### Why Not One Big Index?

Markdown files are short, structured, and command-dense — they need small chunks
so that individual commands and steps stay isolated. PDFs are dense 100–300 page
manuals where a single procedure spans multiple paragraphs — small chunks would
fragment the context and produce incoherent retrieval results.

## Rebuilding Indexes

If you add/change documents, click **🔄 Rebuild indexes** in the sidebar,
or run from terminal:

```python
from rag_engine import rebuild_indexes
rebuild_indexes()
```

Or delete the `faiss_index_md/` and `faiss_index_pdf/` folders and restart the app.