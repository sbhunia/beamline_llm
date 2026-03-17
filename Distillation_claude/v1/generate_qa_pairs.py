"""
Q&A Pair Generator for SPEC Beamline Fine-Tuning
=================================================
This script processes your PDFs, markdown files, and .mac files to generate
high-quality instruction/answer pairs for fine-tuning.

It generates THREE types of pairs:
1. TEXTUAL Q&A - from PDFs and markdown (factual knowledge)
2. CODE EXPLANATION - "What does this macro do?" -> explanation
3. CODE GENERATION - "Write a SPEC macro that..." -> code

USAGE:
------
Option A: Use a local LLM or API to generate Q&A pairs (recommended)
    - Set your API key and uncomment the API section
    - Run: python generate_qa_pairs.py

Option B: Use template-based generation (no API needed, lower quality)
    - Run: python generate_qa_pairs.py --no-api

The output is a JSONL file ready for fine-tuning.
"""

import json
import os
import re
import sys
from pathlib import Path
from pypdf import PdfReader

# ============================================================
# CONFIGURATION - EDIT THESE PATHS
# ============================================================

PDF_FILES = [
    "/home/vallurs/research/data/PDFs/336_lakeshore__1_.pdf",
    "/home/vallurs/research/data/PDFs/CRYOCOOL-LT_G2b_MANUAL2023__1_.pdf",
    "/home/vallurs/research/data/PDFs/spec_Manual.pdf",
    "/home/vallurs/research/data/PDFs/SPEC_manual_pymca.pdf",
]

MD_FOLDER = "/home/vallurs/research/data/md_files"
MAC_FOLDER = "/home/vallurs/research/data/mac_files"  # folder with .mac files

OUTPUT_FILE = "/home/vallurs/research/data/spec_qa_pairs.jsonl"

# ============================================================
# STEP 1: Extract text from all sources
# ============================================================

def extract_pdf_text(pdf_path, max_pages=None):
    """Extract text from a PDF, page by page."""
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        if max_pages and i >= max_pages:
            break
        text = page.extract_text()
        if text and len(text.strip()) > 50:
            pages.append(text.strip())
    return pages


def extract_md_text(md_folder):
    """Extract text from all markdown files."""
    chunks = []
    for f in sorted(Path(md_folder).glob("*.md")):
        with open(f, "r", encoding="utf-8") as fh:
            text = fh.read().strip()
            if text:
                chunks.append({"source": f.name, "text": text})
    return chunks


def extract_mac_files(mac_folder):
    """Extract .mac files as individual code blocks with metadata."""
    mac_files = []
    extensions = ["*.mac", "*.macro"]
    # Also grab files without extensions that are SPEC scripts
    for ext in extensions:
        for f in sorted(Path(mac_folder).glob(ext)):
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                code = fh.read().strip()
                if code and len(code) > 20:
                    mac_files.append({
                        "filename": f.name,
                        "code": code,
                    })
    # Also check for extensionless files that look like SPEC code
    for f in sorted(Path(mac_folder).iterdir()):
        if f.is_file() and f.suffix == "" and f.name not in ["README"]:
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                code = fh.read().strip()
                if code and ("def " in code or "umv " in code or "ascan " in code):
                    mac_files.append({
                        "filename": f.name,
                        "code": code,
                    })
    return mac_files


def extract_functions_from_mac(code):
    """Parse a .mac file and extract individual function definitions."""
    functions = []
    # SPEC functions are defined with: def function_name '{ ... }'
    # or: def function_name ' ... '
    pattern = r"def\s+(\w+)\s*'(.*?)'"
    matches = re.findall(pattern, code, re.DOTALL)
    for name, body in matches:
        body = body.strip()
        if len(body) > 10:
            functions.append({"name": name, "body": f"def {name} '{body}'"})
    return functions


# ============================================================
# STEP 2: Generate Q&A pairs (template-based, no API needed)
# ============================================================

def generate_text_qa_from_faq(md_text):
    """Extract Q&A pairs from FAQ-style markdown."""
    pairs = []
    lines = md_text.split("\n")
    current_q = None
    current_a = []

    for line in lines:
        line = line.strip()
        # Match question patterns
        if re.match(r"^#{1,6}\s*Q[\.:]\s*", line) or re.match(r"^#{1,6}\s*Q\s", line):
            if current_q and current_a:
                answer = " ".join(current_a).strip()
                if len(answer) > 20:
                    pairs.append({
                        "instruction": current_q,
                        "output": answer,
                        "type": "text_qa"
                    })
            current_q = re.sub(r"^#{1,6}\s*Q[\.:]*\s*", "", line).strip()
            current_a = []
        elif current_q is not None:
            # Skip image/figure markdown
            if line.startswith("![") or line.startswith("<figure") or line.startswith("</figure"):
                continue
            if line.startswith("#"):
                # New section, save current Q&A
                if current_q and current_a:
                    answer = " ".join(current_a).strip()
                    if len(answer) > 20:
                        pairs.append({
                            "instruction": current_q,
                            "output": answer,
                            "type": "text_qa"
                        })
                current_q = None
                current_a = []
            elif line:
                current_a.append(line)

    # Don't forget the last one
    if current_q and current_a:
        answer = " ".join(current_a).strip()
        if len(answer) > 20:
            pairs.append({
                "instruction": current_q,
                "output": answer,
                "type": "text_qa"
            })
    return pairs


def generate_procedural_qa(md_text, source_name):
    """Generate Q&A pairs from step-by-step procedures in markdown."""
    pairs = []
    sections = re.split(r"\n#{1,4}\s+", md_text)

    for section in sections:
        lines = section.strip().split("\n")
        if not lines:
            continue
        title = lines[0].strip()
        body_lines = [l.strip() for l in lines[1:] if l.strip()
                       and not l.strip().startswith("![")
                       and not l.strip().startswith("<figure")]
        body = "\n".join(body_lines)

        if len(body) > 50 and ("step" in body.lower() or "* " in body):
            pairs.append({
                "instruction": f"What are the steps for {title}?",
                "output": body,
                "type": "procedural_qa"
            })
    return pairs


def generate_code_explanation_pairs(mac_files):
    """Generate 'explain this code' pairs from .mac files."""
    pairs = []
    for mac in mac_files:
        functions = extract_functions_from_mac(mac["code"])
        for func in functions:
            # "What does X do?" -> code
            pairs.append({
                "instruction": f"What does the SPEC macro function '{func['name']}' do in {mac['filename']}? Show its code.",
                "output": func["body"],
                "type": "code_explanation"
            })
            # "Write a SPEC macro like X" -> code
            # Infer purpose from name
            purpose = func["name"].replace("_", " ").replace("-", " ")
            pairs.append({
                "instruction": f"Write a SPEC macro for {purpose}.",
                "output": func["body"],
                "type": "code_generation"
            })
    return pairs


def generate_full_file_pairs(mac_files):
    """Generate pairs for complete .mac files."""
    pairs = []
    for mac in mac_files:
        if len(mac["code"]) < 5000:  # Only for reasonably sized files
            # Extract first comment block as description
            desc_lines = []
            for line in mac["code"].split("\n"):
                if line.startswith("#"):
                    desc_lines.append(line.lstrip("#").strip())
                elif desc_lines:
                    break
            desc = " ".join(desc_lines).strip() if desc_lines else mac["filename"]

            pairs.append({
                "instruction": f"Show me the complete SPEC macro file '{mac['filename']}'. What does it do?",
                "output": f"The file '{mac['filename']}' contains macros for {desc}.\n\nHere is the complete code:\n\n```\n{mac['code']}\n```",
                "type": "code_full_file"
            })
    return pairs


def generate_cryocool_qa_from_pdf(pdf_pages):
    """Generate Q&A pairs from the CRYOCOOL manual."""
    full_text = "\n".join(pdf_pages)
    pairs = []

    # Manually crafted Q&A from the CRYOCOOL manual content
    qa_templates = [
        {
            "q": "What are the main component parts of the CRYOCOOL-LT system?",
            "search": "Main Component Parts",
        },
        {
            "q": "What type of refrigerator is used in the CRYOCOOL system?",
            "search": "Gifford McMahon",
        },
        {
            "q": "What are the four temperature sensor channels on the CRYOCOOL-LT?",
            "search": "Channel A",
        },
        {
            "q": "How does the tip heater prevent ice formation in the CRYOCOOL system?",
            "search": "Tip Heater",
        },
        {
            "q": "What is the maximum pressure relief setting for the CRYOCOOL gas supply?",
            "search": "Pressure relief",
        },
        {
            "q": "What are the typical PID settings for the CRYOCOOL gas stream temperature control?",
            "search": "PID",
        },
        {
            "q": "What are the steps for operating the CRYOCOOL with helium gas?",
            "search": "Operation - Helium",
        },
        {
            "q": "What are the steps for operating the CRYOCOOL with nitrogen gas?",
            "search": "Operation - Nitrogen",
        },
        {
            "q": "How do you shut down the CRYOCOOL system?",
            "search": "Shutdown",
        },
        {
            "q": "What is the normal flow rate for helium gas in the CRYOCOOL?",
            "search": "flow rate",
        },
    ]

    for template in qa_templates:
        # Find relevant text around the search term
        search = template["search"].lower()
        for i, page in enumerate(pdf_pages):
            if search in page.lower():
                # Take this page and maybe the next
                answer_text = page
                if i + 1 < len(pdf_pages):
                    answer_text += "\n" + pdf_pages[i + 1]
                # Truncate to reasonable length
                answer_text = answer_text[:2000].strip()
                if len(answer_text) > 50:
                    pairs.append({
                        "instruction": template["q"],
                        "output": answer_text,
                        "type": "text_qa"
                    })
                break
    return pairs


def generate_lakeshore_qa_from_pdf(pdf_pages):
    """Generate Q&A pairs from the Lakeshore 336 manual."""
    pairs = []
    qa_templates = [
        {"q": "What are the input types supported by the Lakeshore 336 temperature controller?", "search": "input type"},
        {"q": "How do you configure the heater output on the Lakeshore 336?", "search": "heater output"},
        {"q": "What temperature sensor curves are available on the Lakeshore 336?", "search": "sensor curve"},
        {"q": "How do you set up PID control on the Lakeshore 336?", "search": "PID"},
        {"q": "What are the remote interface commands for the Lakeshore 336?", "search": "remote interface"},
        {"q": "How do you configure zones on the Lakeshore 336?", "search": "zone"},
    ]

    for template in qa_templates:
        search = template["search"].lower()
        for i, page in enumerate(pdf_pages):
            if search in page.lower():
                answer_text = page[:2000].strip()
                if len(answer_text) > 50:
                    pairs.append({
                        "instruction": template["q"],
                        "output": answer_text,
                        "type": "text_qa"
                    })
                break
    return pairs


def generate_spec_manual_qa(pdf_pages):
    """Generate Q&A pairs from the SPEC manual."""
    pairs = []
    # SPEC manual is huge (317 pages), extract key sections
    qa_templates = [
        {"q": "What is the SPEC command 'ascan' and how do you use it?", "search": "ascan"},
        {"q": "How do you move a motor in SPEC?", "search": "mv "},
        {"q": "How do you define a macro in SPEC?", "search": "def "},
        {"q": "How do you set motor limits in SPEC?", "search": "set_lm"},
        {"q": "What is the 'ct' command in SPEC?", "search": "counting"},
        {"q": "How do you use the SPEC dscan command?", "search": "dscan"},
        {"q": "How do you open and close shutters in SPEC?", "search": "shopen"},
        {"q": "What is a mesh scan in SPEC?", "search": "mesh"},
        {"q": "How do you save motor positions in SPEC?", "search": "usersave"},
        {"q": "How do you use the MCA (multichannel analyzer) in SPEC?", "search": "mcasetup"},
    ]

    for template in qa_templates:
        search = template["search"].lower()
        for i, page in enumerate(pdf_pages):
            if search in page.lower() and len(page) > 100:
                answer_text = page[:2000].strip()
                if len(answer_text) > 80:
                    pairs.append({
                        "instruction": template["q"],
                        "output": answer_text,
                        "type": "text_qa"
                    })
                break
    return pairs


# ============================================================
# STEP 3: LLM-POWERED Q&A Generation (RECOMMENDED)
# ============================================================

# If you have access to an API (OpenAI, Anthropic, etc.), you can
# generate much higher quality Q&A pairs.
# Uncomment and configure the section below.

"""
import openai  # or anthropic

client = openai.OpenAI(api_key="YOUR_KEY")  # or use anthropic

def generate_qa_with_llm(text_chunk, source_type="document"):
    prompt = f'''You are helping create training data for a SPEC beamline assistant.
Given the following {source_type} content, generate 5-10 question-answer pairs.

For text content: Generate factual Q&A about the procedures, settings, and equipment.
For code content: Generate "What does this do?", "How would you write...", and 
"Explain..." style questions.

Output as JSON array: [{{"question": "...", "answer": "..."}}]

Content:
{text_chunk[:4000]}
'''
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or claude-sonnet-4-20250514 via Anthropic
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    
    try:
        pairs = json.loads(response.choices[0].message.content)
        return pairs
    except:
        return []
"""


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():
    use_api = "--no-api" not in sys.argv
    all_pairs = []

    print("=" * 60)
    print("SPEC Beamline Q&A Pair Generator")
    print("=" * 60)

    # --- Process PDFs ---
    for pdf_path in PDF_FILES:
        if not os.path.exists(pdf_path):
            print(f"  [SKIP] PDF not found: {pdf_path}")
            continue
        print(f"\n  Processing PDF: {os.path.basename(pdf_path)}")
        pages = extract_pdf_text(pdf_path)
        print(f"    Extracted {len(pages)} pages")

        basename = os.path.basename(pdf_path).lower()
        if "cryocool" in basename:
            pairs = generate_cryocool_qa_from_pdf(pages)
        elif "lakeshore" in basename or "336" in basename:
            pairs = generate_lakeshore_qa_from_pdf(pages)
        elif "spec" in basename:
            pairs = generate_spec_manual_qa(pages)
        else:
            pairs = []

        all_pairs.extend(pairs)
        print(f"    Generated {len(pairs)} Q&A pairs")

    # --- Process Markdown ---
    if os.path.isdir(MD_FOLDER):
        print(f"\n  Processing Markdown files from: {MD_FOLDER}")
        md_chunks = extract_md_text(MD_FOLDER)
        for chunk in md_chunks:
            faq_pairs = generate_text_qa_from_faq(chunk["text"])
            proc_pairs = generate_procedural_qa(chunk["text"], chunk["source"])
            all_pairs.extend(faq_pairs)
            all_pairs.extend(proc_pairs)
            print(f"    {chunk['source']}: {len(faq_pairs)} FAQ + {len(proc_pairs)} procedural pairs")
    elif os.path.isfile(MD_FOLDER):
        # Single MD file
        with open(MD_FOLDER, "r", encoding="utf-8") as f:
            text = f.read()
        faq_pairs = generate_text_qa_from_faq(text)
        proc_pairs = generate_procedural_qa(text, "combined_output.md")
        all_pairs.extend(faq_pairs)
        all_pairs.extend(proc_pairs)
        print(f"    combined_output.md: {len(faq_pairs)} FAQ + {len(proc_pairs)} procedural pairs")

    # --- Process .mac files ---
    if os.path.isdir(MAC_FOLDER):
        print(f"\n  Processing .mac files from: {MAC_FOLDER}")
        mac_files = extract_mac_files(MAC_FOLDER)
        print(f"    Found {len(mac_files)} macro files")

        code_pairs = generate_code_explanation_pairs(mac_files)
        file_pairs = generate_full_file_pairs(mac_files)
        all_pairs.extend(code_pairs)
        all_pairs.extend(file_pairs)
        print(f"    Generated {len(code_pairs)} code Q&A + {len(file_pairs)} full-file pairs")

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print(f"TOTAL Q&A PAIRS: {len(all_pairs)}")

    type_counts = {}
    for p in all_pairs:
        t = p.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")

    # --- Save ---
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for pair in all_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")

    print(f"\nSaved to: {OUTPUT_FILE}")
    print(f"{'=' * 60}")
    print("\nNEXT STEPS:")
    print("1. Review the generated pairs and fix any incorrect answers")
    print("2. Add more pairs manually for critical domain knowledge")
    print("3. Run the training script: python train_spec_lora.py")
    print("\nTO GET MORE PAIRS (RECOMMENDED):")
    print("  Use Claude/GPT-4 to generate additional Q&A pairs from your PDFs.")
    print("  Feed each PDF page to the LLM and ask it to generate 5-10 Q&A pairs.")
    print("  This can easily get you to 500-1000+ high-quality pairs.")


if __name__ == "__main__":
    main()
