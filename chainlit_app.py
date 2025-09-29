from __future__ import annotations

import os, datetime as dt, re
import streamlit as st
from scripts.router import route as route_query
from scripts.codegen_agent import run_codegen_ui
from scripts.text_agent import answer as text_answer
from scripts.log_utils import log_event

# Timeout helper
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError
def run_with_timeout(func, *args, timeout_s: int = 30, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func, *args, **kwargs)
        try:
            return fut.result(timeout=timeout_s), None
        except _TOError:
            return None, "timeout"
        except Exception as e:
            return None, f"error: {e}"

# ---------------- UI config + styles ----------------
st.set_page_config(page_title="QM2 Assistant", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
<style>
.topbar { background:#b50f2b; height:52px; width:100%; position:fixed; top:0; left:0; right:0; z-index:9999;
          display:flex; align-items:center; padding:0 18px; box-shadow:0 1px 0 rgba(0,0,0,0.08); }
.topbar-title { color:#fff; font-weight:700; font-size:24px; letter-spacing:.2px; }
.topbar-logo { margin-left:auto; color:#fff; font-weight:800; font-size:28px; }
.block-container { padding-top:80px; }
section[data-testid="stSidebar"] { width:260px !important; }
.plaque { background:#d5d1bf; display:inline-block; padding:12px 22px; border-radius:3px; font-weight:800; letter-spacing:.5px; color:#1a1a1a; }
.result-card { background:#fff; border:1px solid #e5e5e5; border-radius:6px; padding:10px 12px; margin-bottom:8px; }
code.path { background:#f7f7f7; padding:2px 6px; border-radius:4px; }
.agent-badge { display:inline-block; padding:4px 8px; border-radius:6px; font-weight:700; font-size:12px; margin-bottom:8px; }
.agent-code { background:#fff1f2; color:#9f1239; border:1px solid #fecdd3; }
.agent-text { background:#eef2ff; color:#1e3a8a; border:1px solid #c7d2fe; }
html, body, .block-container { font-size: 1.05rem; }
code, pre { font-size: 0.95rem !important; }
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="topbar">
    <div class="topbar-title">User Interface (Front-end)</div>
    <div class="topbar-logo">M</div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------- Session state ----------------
if "view" not in st.session_state: st.session_state.view="home"
if "messages" not in st.session_state: st.session_state.messages=[]
if "history" not in st.session_state: st.session_state.history=[]
if "last_generated_code" not in st.session_state: st.session_state.last_generated_code=""
if "last_task" not in st.session_state: st.session_state.last_task=""
if "debug_last" not in st.session_state: st.session_state.debug_last=None
if "beamline_mode" not in st.session_state: st.session_state.beamline_mode=True  # ON = no website
if "last_intent" not in st.session_state: st.session_state.last_intent=None
if "last_topic" not in st.session_state: st.session_state.last_topic=None

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("<div class='sb-label'>🆕 <span>New chat</span> <span class='badge-new'>NEW</span></div>", unsafe_allow_html=True)
    new_chat=st.button("New chat",key="btn_new")

    st.markdown("<div class='sb-label'>🧪 <span>Beamline Mode</span></div>", unsafe_allow_html=True)
    st.session_state.beamline_mode = st.toggle(
        "Beamline Mode (Drive+Markdown only; no website)",
        value=st.session_state.beamline_mode,
        help="ON = faster, local docs only. OFF = also include Website.",
        key="toggle_beamline",
    )

    st.markdown("<div class='sb-label'>📜 <span>History</span></div>", unsafe_allow_html=True)
    _ = st.button("History",key="btn_history")

    st.markdown("<div class='sb-label'>⚙️ <span>Settings</span></div>", unsafe_allow_html=True)
    st.session_state.show_debug=st.toggle(
        "Show debug panel",
        value=st.session_state.get("show_debug",False),
        help="Show retrieved chunks, router decision, and scores.",
        key="toggle_debug",
    )

if new_chat:
    if st.session_state.messages:
        st.session_state.history.append(
            {"when":dt.datetime.now().isoformat(timespec="seconds"), "transcript":list(st.session_state.messages)}
        )
    st.session_state.messages=[]; st.session_state.view="home"
    st.session_state.last_generated_code=""; st.session_state.last_task=""
    st.session_state.last_intent=None; st.session_state.last_topic=None

# ---------------- Header plaque ----------------
cc1,cc2,cc3=st.columns([1,2,1])
with cc2:
    st.markdown(
        f"<div class='plaque' style='display:block; text-align:center;'>"
        f"QM2 ASSISTANT • Beamline Mode: {'ON' if st.session_state.beamline_mode else 'OFF'}</div>",
        unsafe_allow_html=True,
    )

# ---------------- Chat history render ----------------
if not st.session_state.messages and st.session_state.view=="home":
    st.markdown(
        """<div style="display:flex; justify-content:center; align-items:center; height:280px;">
           <div style="font-size:28px; font-weight:700; color:#1a1a1a;">Hi! How can I help you today?</div></div>""",
        unsafe_allow_html=True,
    )
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- Smalltalk + followups ----------------
_SMALLTALK_RE = re.compile(
    r"^\s*(hi|hello|hey|yo|hola|namaste|sup|how\s+are\s+you\??|how'?s\s+it\s+going\??|what'?s\s*up\??|whats\s*up\??)\s*$",
    re.I
)

def _resolve_followup(uq: str) -> str:
    q = uq.strip().lower()
    li = st.session_state.last_intent or {}
    if not li: return uq
    if re.search(r"\b(once|one time|write\s+for\s+once|write\s+once)\b", q) and li.get("type")=="rotate":
        return "write a spec code to spin the crystal 1 time"
    if re.search(r"\b(also\s+)?add\s+comment\b", q) and li.get("type")=="move_motor":
        return "write a spec code to move a single motor, and also add a printer comment that it was moved"
    return uq

def _record_intent_from_task(task_text: str) -> None:
    t = task_text or ""
    m = re.search(r"rotate\s+(?:the\s+)?(?:sample|crystal)\s+(\d+)\s+times", t, re.I)
    if m:
        st.session_state.last_intent={"type":"rotate","n":int(m.group(1))}
        st.session_state.last_topic="rotate"; return
    if re.search(r"\bspin\s+(?:the\s+)?(?:sample|crystal)\s+(?:one|1)\s+time\b", t, re.I):
        st.session_state.last_intent={"type":"rotate","n":1}
        st.session_state.last_topic="rotate"; return
    if re.search(r"\bmove\s+(?:a|one|single)\s+motor\b", t, re.I):
        st.session_state.last_intent={"type":"move_motor","comment":bool(re.search(r"\b(comment|printer)\b", t, re.I))}
        st.session_state.last_topic="move_motor"

# ---------------- Chat input ----------------
user_query = st.chat_input("Type your query here…")
if user_query:
    uq = user_query.strip()
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role":"user","content":user_query})

    if _SMALLTALK_RE.match(uq):
        reply = " Ready to crunch macros and answer beamline questions. What should we tackle?"
        with st.chat_message("assistant"):
            st.markdown("<span class='agent-badge agent-text'>📚 TEXT AGENT</span><br/>"+reply, unsafe_allow_html=True)
        st.session_state.messages.append({"role":"assistant","content":reply})
    else:
        effective_query = _resolve_followup(uq)
        with st.chat_message("assistant"):
            try:
                route, conf, meta = route_query(effective_query)
            except Exception as e:
                route, conf, meta = "text", 0.0, {"error": str(e)}

            # ---------------- CODE route ----------------
            # ---------------- CODE route ----------------
            if route == "code":
                result, err = run_with_timeout(run_codegen_ui, effective_query, timeout_s=30)
                if err == "timeout":
                    answer = (
                        "<span class='agent-badge agent-code'>🛠️ CODE AGENT</span><br/>"
                        "Timed out while generating code. Showing a minimal SPEC stub you can run, "
                        "and logging this timeout to help debug."
                        "\n\n```spec\nprint \"timeout while generating code\"\n```"
                    )
                    st.markdown(answer, unsafe_allow_html=True)
                    log_event({"type":"timeout","agent":"code","query":effective_query})
                    st.session_state.debug_last={"router":{"route":route,"conf":conf,**meta},"agent":"code","error":"timeout"}
                    st.session_state.messages.append({"role":"assistant","content":answer})
                    st.stop()

                elif err and err.startswith("error:"):
                    msg = err.split("error:",1)[-1].strip()
                    answer = (
                        "<span class='agent-badge agent-code'>🛠️ CODE AGENT</span><br/>"
                        f"Error while generating code: {msg}\n\n"
                        "```spec\nprint \"codegen error\"\n```"
                    )
                    st.markdown(answer, unsafe_allow_html=True)
                    log_event({"type":"error","agent":"code","query":effective_query,"error":msg})
                    st.session_state.debug_last={"router":{"route":route,"conf":conf,**meta},"agent":"code","error":msg}
                    st.session_state.messages.append({"role":"assistant","content":answer})
                    st.stop()

                # ---- unpack primary fields (with safe defaults) ----
                result = result or {}
                code = (result.get("code") or "").strip()
                rationale = result.get("rationale") or ""
                warnings = result.get("warnings") or ""
                raw_prompt = result.get("raw_prompt") or ""
                rag_joined = result.get("rag_joined") or ""
                rag_excerpts = result.get("rag_excerpts") or []
                raw_model = result.get("raw_model_outputs") or {}
                draft_raw = (raw_model.get("draft") or "").strip()
                repaired_raw = (raw_model.get("repaired") or "").strip()

                # ---- main SPEC output (as before) ----
                header = "<span class='agent-badge agent-code'>🛠️ CODE AGENT</span>"
                answer = f"{header}\n\n```spec\n{code}\n```"
                if rationale: answer += f"\n\n**Rationale:** {rationale}"
                if warnings and warnings not in {"no-code-intent"}: answer += f"\n\n**Note:** {warnings}"
                st.markdown(answer, unsafe_allow_html=True)

                # ---- NEW: RAG + raw model outputs UI ----
                with st.expander("🔎 Exact prompt sent to the model"):
                    st.code(raw_prompt, language="text")

                with st.expander("📚 RAG context (joined blob)"):
                    st.code(rag_joined, language="text")

                if rag_excerpts:
                    with st.expander(f"🧩 Retrieved chunks ({len(rag_excerpts)}) — previews"):
                        for i, chunk_head in enumerate(rag_excerpts, 1):
                            st.markdown(f"**Chunk {i}**")
                            st.code(chunk_head, language="text")

                with st.expander("🧠 Model raw outputs (no post-processing)"):
                    st.markdown("**Draft (first pass)**")
                    st.code(draft_raw or "<empty>", language="text")
                    st.markdown("**Repair (second pass)**")
                    st.code(repaired_raw or "<empty>", language="text")

                # ---- state + logs (keep existing) ----
                st.session_state.last_generated_code = code
                st.session_state.last_task = effective_query
                _record_intent_from_task(effective_query)

                log_event({
                    "type":"router","route":route,"conf":conf,"query":effective_query,
                    "beamline":st.session_state.beamline_mode
                })

                # enrich debug payload so your Debug panel shows the same info
                dbg_payload = {
                    "router":{"route":route,"conf":conf,**meta},
                    "agent":"code",
                    "retrieved": (result.get("_debug") or {}).get("retrieved", []),
                    "raw_prompt": raw_prompt,
                    "rag_joined": rag_joined[:2000],  # clip for panel
                    "raw_model_outputs": {
                        "draft_head": draft_raw[:1000],
                        "repaired_head": repaired_raw[:1000]
                    }
                }
                st.session_state.debug_last = dbg_payload
                st.session_state.messages.append({"role":"assistant","content":answer})


            # ---------------- TEXT route ----------------
            else:
                resp, err = run_with_timeout(text_answer, effective_query, timeout_s=30, beamline=st.session_state.beamline_mode)
                if err == "timeout":
                    fallback = "<span class='agent-badge agent-text'>📚 TEXT AGENT</span><br/>Timed out fetching an answer."
                    st.markdown(fallback, unsafe_allow_html=True)
                    log_event({"type":"timeout","agent":"text","query":effective_query})
                    st.session_state.debug_last={"router":{"route":route,"conf":conf,**meta},"agent":"text","error":"timeout"}
                    st.session_state.messages.append({"role":"assistant","content":"Timed out fetching an answer."})
                    st.stop()

                elif err and err.startswith("error:"):
                    msg = err.split("error:",1)[-1].strip()
                    fallback = f"<span class='agent-badge agent-text'>📚 TEXT AGENT</span><br/>Error while answering: {msg}"
                    st.markdown(fallback, unsafe_allow_html=True)
                    log_event({"type":"error","agent":"text","query":effective_query,"error":msg})
                    st.session_state.debug_last={"router":{"route":route,"conf":conf,**meta},"agent":"text","error":msg}
                    st.session_state.messages.append({"role":"assistant","content":fallback})
                    st.stop()

                # Accept both (text, cites, dbg) shape (always returned by our text_agent now)
                text, cites, dbg = resp if isinstance(resp, (list, tuple)) else ("", [], {})
                header = "<span class='agent-badge agent-text'>📚 TEXT AGENT</span>"
                st.markdown(header+"<br/>"+(text or ""), unsafe_allow_html=True)
                if cites:
                    with st.expander("Sources"):
                        for p, s in cites:
                            st.markdown(f"<div class='result-card'><code class='path'>{p}</code><br/>{s}</div>", unsafe_allow_html=True)
                log_event({"type":"router","route":route,"conf":conf,"query":effective_query,"beamline":st.session_state.beamline_mode})
                st.session_state.debug_last={
                    "router":{"route":route,"conf":conf,**meta},
                    "agent":"text",
                    "topk":[{"src":p,"preview":(s or "")[:200]} for p,s in (cites or [])],
                    "retrieval": dbg or {}
                }
                st.session_state.messages.append({"role":"assistant","content":text or ""})

# ---------------- Debug panel ----------------
if st.session_state.show_debug and st.session_state.debug_last:
    with st.expander("Debug info"):
        st.json(st.session_state.debug_last)
    st.caption("Events are also logged to: logs/session.jsonl")
