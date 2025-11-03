from __future__ import annotations
import os, csv, uuid, datetime as dt, requests
from typing import Dict, Any

LOG_DIR = os.getenv("LOG_DIR", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

SESSION_ID = os.getenv(
    "SESSION_ID",
    dt.datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
)

CSV_PATH = os.path.join(LOG_DIR, f"session_{SESSION_ID}.csv")

CSV_HEADER = [
    
    "timestamp","session_id","request_id",
    
    "event_or_stage","event_name","agent","route","method",
    
    "original_query","normalized_query","rewritten_query",
    
    "source","retrieved","retrieved_full","vector_dim","vector_preview",
    "best_score","avg_score","spread","confidence",
    
    "prompt_chars","prompt_tokens_est","prompt_full",
   
    "model","latency_ms","llm_output_full",

    "parser_passed","parser_result","parser_input",
    
    "final_output_full","preview"
]

def _sanitize(val: Any) -> str:
    if val is None: return ""
    return str(val).replace("\r","\\r").replace("\n","\\n").replace("\t","\\t")

def _write_row(row: Dict[str, Any]):
    header_needed = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER, quoting=csv.QUOTE_ALL)
        if header_needed:
            w.writeheader()
        w.writerow({k: _sanitize(row.get(k, "")) for k in CSV_HEADER})

def _base_row(payload: Dict[str, Any], kind: str, name: str) -> Dict[str, Any]:
    return {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "session_id": SESSION_ID,
        "request_id": payload.get("request_id",""),
        "event_or_stage": kind,
        "event_name": name,
        "agent": payload.get("agent",""),
        "route": payload.get("route",""),
        "method": payload.get("method",""),
        "original_query": payload.get("original_query",""),
        "normalized_query": payload.get("normalized_query",""),
        "rewritten_query": payload.get("rewritten_query",""),
        "source": payload.get("source",""),
        "retrieved": payload.get("retrieved",""),
        "retrieved_full": payload.get("retrieved_full",""),
        "vector_dim": payload.get("vector_dim",""),
        "vector_preview": payload.get("vector_preview",""),
        "best_score": payload.get("best_score",""),
        "avg_score": payload.get("avg_score",""),
        "spread": payload.get("spread",""),
        "confidence": payload.get("confidence",""),
        "prompt_chars": payload.get("prompt_chars",""),
        "prompt_tokens_est": payload.get("prompt_tokens_est",""),
        "prompt_full": payload.get("prompt_full",""),
        "model": payload.get("model",""),
        "latency_ms": payload.get("latency_ms",""),
        "llm_output_full": payload.get("llm_output_full",""),
        "parser_passed": payload.get("parser_passed",""),
        "parser_result": payload.get("parser_result",""),
        "parser_input": payload.get("parser_input",""),
        "final_output_full": payload.get("final_output_full",""),
        "preview": payload.get("preview","")
    }

def log_event(event: str, payload: Dict[str, Any]):
    _write_row(_base_row(payload, "event", event))

def log_stage(stage: str, payload: Dict[str, Any]):
    _write_row(_base_row(payload, "stage", stage))

def check_ollama_health(base_url="http://127.0.0.1:11434"):
    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            return {"status": "ok", "models": models}
        return {"status": f"bad_status_{resp.status_code}", "models": []}
    except Exception as e:
        return {"status": f"error: {e}", "models": []}
