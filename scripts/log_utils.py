import os, json, datetime as dt

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "session.jsonl")

def log_event(event: dict):
    """Write events to logs/session.jsonl + console."""
    event = {"time": dt.datetime.now().isoformat(), **event}
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print("LOG:", event)
