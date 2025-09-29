from __future__ import annotations
from typing import Dict, Any
from langchain_ollama import ChatOllama
import os
import json

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
ROUTER_MODEL = os.getenv("ROUTER_MODEL", os.getenv("TEXT_MODEL", "mistral:instruct"))

ROUTER_PROMPT = """
You are a routing agent. There are two specialists:

- CODE AGENT: for SPEC macros/commands, writing or generating code, or performing calculations.
- TEXT AGENT: for explanations, definitions, descriptions, and conceptual answers.
- BOTH: when the request needs both explanation and code.

RULES:
- If the user says "write", "generate", "show code", "give me a macro", or similar → always CODE.
- If the query mixes explanation and code → BOTH.
- If the user just asks "what is", "explain", "define", or "describe" → TEXT.

Return the result as JSON:
{"route": "CODE" | "TEXT" | "BOTH", "confidence": float between 0 and 1}

Examples:
Q: "Write a spec code to rotate a sample 10 times"
A: {"route": "CODE", "confidence": 0.95}

Q: "Explain what ascan does"
A: {"route": "TEXT", "confidence": 0.9}

Q: "Explain what ascan does and show me code"
A: {"route": "BOTH", "confidence": 0.95}

Now classify this request:
"""

def route(query: str) -> Dict[str, Any]:
    try:
        llm = ChatOllama(model=ROUTER_MODEL, base_url=OLLAMA_BASE, temperature=0.0)
        response = llm.invoke([{"role": "user", "content": ROUTER_PROMPT + query}])
        raw = getattr(response, "content", str(response)) or ""
        data = json.loads(raw)
        label = data.get("route", "TEXT").lower()
        conf = float(data.get("confidence", 0.7))
        return {"route": label, "confidence": conf, "method": "llm"}
    except Exception as e:
        return {"route": "text", "confidence": 0.5, "method": f"error: {e}"}
