from __future__ import annotations
import os, csv, uuid, datetime as dt, sys
from typing import List, Dict, Any
import yaml

from scripts.router import route
from scripts.codegen_agent import run_codegen_ui
from scripts.text_agent import answer

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def _timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")

def _new_run_path() -> str:
    return os.path.join(LOG_DIR, f"eval_run_{_timestamp()}_{uuid.uuid4().hex[:6]}.csv")

def run_eval(yaml_path: str) -> str:
    """
    YAML format:
    - query: "..."
      expected: "..."   # optional (you'll compute ROUGE manually in Excel)
    """
    with open(yaml_path, "r") as f:
        items = yaml.safe_load(f) or []

    out_path = _new_run_path()
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "idx","query","route","confidence","answer_or_code",
            "grounded","parser_passed","sources","prompt_chars","expected"
        ])
        for i, row in enumerate(items):
            q = row.get("query","")
            expected = row.get("expected","")
            r = route(q)
            if r["route"] == "code":
                res = run_codegen_ui(q)
                answer_or_code = res["code"]
                grounded = res.get("grounded", False)
                parser_passed = res.get("parser_passed", False)
                sources = res.get("sources", [])
                prompt_chars = res.get("prompt_chars", 0)
            else:
                res = answer(q)
                answer_or_code = res["answer"]
                grounded = res.get("grounded", False) or res.get("inferred", False)
                parser_passed = ""  # N/A for text
                sources = res.get("sources", [])
                prompt_chars = res.get("prompt_chars", 0)

            w.writerow([
                i, q, r["route"], r["confidence"],
                answer_or_code.replace("\n"," \\n ")[:1500],
                grounded, parser_passed, str(sources), prompt_chars, expected
            ])
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.eval_runner path/to/tests.yaml")
        sys.exit(1)
    out_csv = run_eval(sys.argv[1])
    print("Wrote:", out_csv)
