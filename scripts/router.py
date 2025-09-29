from __future__ import annotations
import os, re, json, time
from typing import Literal, Tuple
from langchain_ollama import ChatOllama

Route = Literal["code", "text"]

# Simple keyword rules
_CODE_TOKENS = {
    "umv","umvr","ascan","dscan","mesh","mv","mvr","waitmove",
    "getangles","ct","for (","while (","phi","spec","macro","def "
}
_CODE_TRIGGERS = (
    "generate","write","macro","code","script","implement","create","rotate","scan","move"
)

def _rule_score(q: str) -> float:
    ql = (q or "").lower()
    score = 0.0
    if any(t in ql for t in _CODE_TRIGGERS): score += 0.6
    if any(t in ql for t in _CODE_TOKENS):   score += 0.6
    if re.search(r"\bdef\s+[A-Za-z_]\w*\b", ql): score += 0.6
    return min(score, 1.0)

def _llm_router(q: str) -> Tuple[Route, float]:
    model = ChatOllama(
        model=os.getenv("ROUTER_MODEL","mistral:latest"),
        base_url=os.getenv("OLLAMA_BASE_URL","http://127.0.0.1:11434"),
        temperature=0.0
    )
    prompt = (
        "Classify the user query as either SPEC CODE or TEXT.\n"
        "Return ONLY JSON as {\"route\":\"code|text\",\"confidence\":0..1}.\n"
        f"Query: {q}\n"
    )
    start = time.time()
    r = model.invoke([{"role":"user","content":prompt}])
    _ = time.time()-start
    try:
        data = json.loads(getattr(r,"content","{}"))
        route = "code" if str(data.get("route","text")).lower().startswith("code") else "text"
        conf  = float(data.get("confidence",0.5))
    except Exception:
        route, conf = "text", 0.5
    return route, max(0.0, min(conf, 1.0))

def route(query: str) -> Tuple[Route, float, dict]:
    rs = _rule_score(query)
    meta = {"rule_score": rs}
    if rs >= 0.95:
        return "code", 0.98, meta
    if rs <= 0.25:
        return "text", 0.9, meta
    llm_route, llm_conf = _llm_router(query)
    meta.update({"llm_route": llm_route, "llm_confidence": llm_conf})
    if llm_conf < 0.6:
        return "text", 0.6, meta
    return llm_route, llm_conf, meta
