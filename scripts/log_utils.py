from __future__ import annotations
import os, csv, uuid, datetime as dt
from typing import Dict, Any, List

# ---------------- Paths + Session ----------------
LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_ID = os.getenv(
    "SESSION_ID",
    dt.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
)

# Telemetry log (high-level)
CSV_PATH = os.path.join(LOG_DIR, f"telemetry_{SESSION_ID}.csv")

# Pipeline log (deep traces: embeddings, prompt, outputs)
PIPELINE_PATH = os.path.join(LOG_DIR, f"pipeline_{SESSION_ID}.csv")

# ---------------- Telemetry Header ----------------
_HEADER = [
    "timestamp","session_id","event","query","route","confidence","method",
    "agent","grounded","parser_passed","inferred",
    "prompt_chars","sources","preview"
]

# ---------------- Pipeline Header ----------------
_PIPELINE_HEADER = [
    "timestamp","session_id","query","stage","route","agent",
    "source","score","vector_dim","vector_preview",
    "retrieved","prompt_chars","prompt_preview",
    "raw_output_preview","final_output_preview"
]

# ---------------- Functions ----------------
def log_event(event: str, payload: Dict[str, Any]):
    """
    Append a high-level event (summary per query) to telemetry_<session>.csv
    """
    row = [
        dt.datetime.now().isoformat(timespec="seconds"),
        SESSION_ID,
        event,
        payload.get("query",""),
        payload.get("route",""),
        payload.get("confidence",""),
        payload.get("method",""),
        payload.get("agent",""),
        payload.get("grounded",""),
        payload.get("parser_passed",""),
        payload.get("inferred",""),
        payload.get("prompt_chars",""),
        str(payload.get("sources","")),
        (payload.get("preview","") or "")[:300].replace("\n"," \\n ")
    ]
    header_needed = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header_needed:
            w.writerow(_HEADER)
        w.writerow(row)


def log_stage(query: str, stage: str, payload: Dict[str, Any]):
    """
    Append a pipeline stage row (deep trace) to pipeline_<session>.csv
    """
    row = [
        dt.datetime.now().isoformat(timespec="seconds"),
        SESSION_ID,
        query,
        stage,
        payload.get("route",""),
        payload.get("agent",""),
        payload.get("source",""),
        payload.get("score",""),
        payload.get("vector_dim",""),
        str(payload.get("vector_preview","")),
        str(payload.get("retrieved","")),
        payload.get("prompt_chars",""),
        (payload.get("prompt_preview","") or "")[:200].replace("\n"," "),
        (payload.get("raw_output_preview","") or "")[:200].replace("\n"," "),
        (payload.get("final_output_preview","") or "")[:200].replace("\n"," "),
    ]
    header_needed = not os.path.exists(PIPELINE_PATH)
    with open(PIPELINE_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header_needed:
            w.writerow(_PIPELINE_HEADER)
        w.writerow(row)
