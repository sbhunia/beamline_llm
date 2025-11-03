from __future__ import annotations
import os, csv, uuid, datetime as dt, requests
from typing import Dict, Any

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_ID = os.getenv(
    "SESSION_ID",
    dt.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
)

CSV_PATH = os.path.join(LOG_DIR, f"telemetry_{SESSION_ID}.csv")
PIPELINE_PATH = os.path.join(LOG_DIR, f"pipeline_{SESSION_ID}.csv")

_HEADER = [
    "timestamp","session_id","request_id","event",
    "original_query","rewritten_query",
    "route","confidence","method",
    "agent","grounded","parser_passed","inferred",
    "prompt_chars","sources","preview"
]

_PIPELINE_HEADER = [
    "timestamp","session_id","request_id","query","stage","route","agent",
    "source","score","vector_dim","vector_preview",
    "retrieved","prompt_chars","prompt_preview",
    "raw_output_preview","final_output_preview"
]

def check_ollama_health(base_url="http://127.0.0.1:11434"):
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            return {"status": "ok", "models": models}
        return {"status": f"bad_status_{resp.status_code}", "models": []}
    except Exception as e:
        return {"status": f"error: {e}", "models": []}

def _write_row(path, header, row):
    header_needed = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header_needed:
            w.writerow(header)
        w.writerow(row)

def log_event(event: str, payload: Dict[str, Any]):
    """High-level telemetry per query."""
    row = [
        dt.datetime.now().isoformat(timespec="seconds"),
        SESSION_ID,
        payload.get("request_id", ""),
        event,
        payload.get("original_query", ""),
        payload.get("rewritten_query", ""),
        payload.get("route", ""),
        payload.get("confidence", ""),
        payload.get("method", ""),
        payload.get("agent", ""),
        payload.get("grounded", ""),
        payload.get("parser_passed", ""),
        payload.get("inferred", ""),
        payload.get("prompt_chars", ""),
        str(payload.get("sources", "")),
        (payload.get("preview", "") or "")[:300].replace("\n", " \\n "),
    ]
    _write_row(CSV_PATH, _HEADER, row)

def log_stage(query: str, stage: str, payload: Dict[str, Any]):
    """Deep trace: detailed pipeline steps."""
    row = [
        dt.datetime.now().isoformat(timespec="seconds"),
        SESSION_ID,
        payload.get("request_id", ""),
        query,
        stage,
        payload.get("route", ""),
        payload.get("agent", ""),
        payload.get("source", ""),
        payload.get("score", ""),
        payload.get("vector_dim", ""),
        str(payload.get("vector_preview", "")),
        str(payload.get("retrieved", "")),
        payload.get("prompt_chars", ""),
        (payload.get("prompt_preview", "") or "")[:200].replace("\n", " "),
        (payload.get("raw_output_preview", "") or "")[:200].replace("\n", " "),
        (payload.get("final_output_preview", "") or "")[:200].replace("\n", " "),
    ]
    _write_row(PIPELINE_PATH, _PIPELINE_HEADER, row)
