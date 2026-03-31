# QM2 Assistant

## Folder Structure

```
COLAB/
├── faiss_index_md/         # Auto-created on first run
└── faiss_index_pdf/        # Auto-created on first run
├── md_files/               # All markdown files
│   ├── about.md
│   ├── beamline_basics.md
│   ├── SPEC_commands.md
│   └── ... (all 39 markdown files)
├── pdf_files/              # All PDF manuals
│   ├── 336_lakeshore (1).pdf
│   ├── CRYOCOOL-LT_G2b_MANUAL2023 (1).pdf
│   ├── SPEC manual pymca.pdf
│   └── spec Manual.pdf
├── app.py                  # Streamlit frontend
├── benchmark.json          # file used for metrics (irrelevant for the user -- please ignore)
├── rag_engine.py           # RAG backend
├── requirements.txt        # requirements and versions 
├── SETUP_gemini.ipynb      # clear instructions on setting up the code


```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your API key (mandatory)

A Gemini API key is required. Create one at [Google AI Studio](https://aistudio.google.com/app/apikey) and make sure billing is enabled for the associated project.

Add the key to `.streamlit/secrets.toml`: When you have access to the app, click on manage app ( Down right corner) then click on settings and go to Secrets. It currently has Aneesha's API key, but it can always be changed.

```toml
GOOGLE_API_KEY = "your-key-here"
```

### 3. Build the indexes

On first run, FAISS indexes are built automatically. If you add or change any files in `md_files/` or `pdf_files/`, the indexes must be rebuilt. There are three ways to do this:

**Option A — Streamlit UI:** Click the "Rebuild Indexes" button in the left sidebar. This will take at least 3–5 minutes due to PDF parsing and embedding generation.

**Option B — Terminal:**
```bash
export GOOGLE_API_KEY="your-key-here"
python rag_engine.py
```

**Option C — Delete and restart:** Delete the `faiss_index_md/` and `faiss_index_pdf/` folders and restart the app. The indexes will be rebuilt automatically on startup.

---

## How It Works

### Two Separate FAISS Indexes

**Markdown index** (`faiss_index_md`) covers 39 markdown files (~130 KB) and uses a chunk size of 300 with an overlap of 150. The smaller chunks keep individual commands and step-by-step procedures isolated for precise lookups.

**PDF index** (`faiss_index_pdf`) covers 4 PDF manuals (~570 pages) and uses a chunk size of 1000 with an overlap of 300. The larger chunks preserve technical context across specs, tables, and wiring diagrams that span multiple paragraphs.

### Retrieval Flow

1. User query hits **both** indexes in parallel
2. Top 6 results from each index are collected
3. Results are deduplicated by content hash
4. Merged results are sorted by similarity score
5. Top 10 chunks are sent to Gemini as context

### Why Not One Big Index?

Markdown files are short, structured, and command-dense — they need small chunks so that individual commands and steps stay isolated. PDFs are dense 100–300 page manuals where a single procedure spans multiple paragraphs — small chunks would fragment the context and produce incoherent retrieval results.

---

## Git Workflow: Keeping Both Repos in Sync

This project uses two remotes:
- `origin` → fork: `sai-aneesha-valluru/beamline_llm` (branch: `Aneesha`) — connected to the Streamlit app
- `upstream` → main repo: `sbhunia/beamline_llm` (branch: `Aneesha`) — source of truth

### One-time setup

After cloning, add the fork as `origin`:

```bash
git remote add origin https://github.com/sai-aneesha-valluru/beamline_llm.git
git remote -v  # verify both remotes appear
```

You should see:

```
origin    https://github.com/sai-aneesha-valluru/beamline_llm.git (fetch)
origin    https://github.com/sai-aneesha-valluru/beamline_llm.git (push)
upstream  https://github.com/sbhunia/beamline_llm.git (fetch)
upstream  https://github.com/sbhunia/beamline_llm.git (push)
```

### Every time you make changes

Push to both remotes to keep everything in sync:

```bash
git add .
git commit -m "describe your change here"
git push origin Aneesha      # updates fork → triggers Streamlit redeploy
git push upstream Aneesha    # keeps main repo in sync
```

>  Always push to both remotes. If you only push to `origin`, the main repo falls behind. If you only push to `upstream`, the Streamlit app won't pick up the changes.
