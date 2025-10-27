from __future__ import annotations
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError
import streamlit as st  

from scripts.codegen_agent import run_codegen_ui
from scripts.log_utils import log_event

# ---------------- Timeout helper ----------------
def run_with_timeout(func, *args, timeout_s: int = 45, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func, *args, **kwargs)
        try:
            return fut.result(timeout=timeout_s), None
        except _TOError as e:
            return None, f"timeout: {e}"
        except Exception as e:
            return None, f"error: {e}"

# ---------------- UI config + styles ----------------
st.set_page_config(page_title="QM2 Assistant", page_icon="🤖", layout="wide")

st.markdown(
    """
<style>
.topbar { background:#b50f2b; height:52px; width:100%; position:fixed;
          top:0; left:0; right:0; z-index:9999;
          display:flex; align-items:center; padding:0 18px;
          box-shadow:0 1px 0 rgba(0,0,0,0.08); }
.topbar-title { color:#fff; font-weight:700; font-size:24px; }
.topbar-logo { margin-left:auto; color:#fff; font-weight:800; font-size:28px; }
.block-container { padding-top:80px; }
.plaque { background:#d5d1bf; display:block; text-align:center;
          padding:12px 22px; border-radius:3px; font-weight:800;
          letter-spacing:.5px; color:#1a1a1a; margin-bottom:12px; }
.helper { color:#6b7280; font-size:14px; text-align:center; margin:-4px 0 16px; }
.agent-badge { display:inline-block; padding:4px 8px; border-radius:6px;
               font-weight:700; font-size:12px; margin-bottom:8px; }
.agent-code { background:#fff1f2; color:#9f1239; border:1px solid #fecdd3; }
.agent-text { background:#eef2ff; color:#1e3a8a; border:1px solid #c7d2fe; }
.warn { background:#fff7ed; border:1px solid #fed7aa; color:#9a3412;
        padding:10px 12px; border-radius:6px; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="topbar">
  <div class="topbar-title">QM2 Assistant</div>
  <div class="topbar-logo">M</div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("<div class='plaque'>QM2 ASSISTANT</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='helper'>Ask me for SPEC macros or explanations. I'll route to the right agent. </div>",
    unsafe_allow_html=True,
)

# ---------------- Session state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False

# ---------------- Sidebar ----------------
with st.sidebar:
    if st.button("New chat", key="btn_new"):
        st.session_state.messages = []
        st.rerun()

    st.session_state.show_debug = st.toggle(
        "Show debug panel",
        value=st.session_state.show_debug,
        help="Show router decision and a few metrics.",
        key="toggle_debug",
    )

    st.markdown("### History")
    user_msgs = [m for m in st.session_state.messages if m.get("role") == "user"]
    if user_msgs:
        for i, msg in enumerate(user_msgs[-5:][::-1], start=1):
            label = (msg["content"][:30] + "…") if len(msg["content"]) > 30 else msg["content"]
            if st.button(f"🔄 {label}", key=f"hist_{i}"):
                st.session_state.messages.append({"role": "user", "content": msg["content"]})
                st.rerun()
    else:
        st.caption("No conversation history yet.")

# ---------------- Replay chat history ----------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("code_block") is not None:
            st.markdown(m["badge_html"], unsafe_allow_html=True)
            st.code(m["code_block"], language="spec")
            if m.get("footnote"):
                st.markdown(m["footnote"], unsafe_allow_html=True)
        else:
            st.markdown(m["content"], unsafe_allow_html=True)

# ---------------- Chat input ----------------
# ---------------- Chat input ----------------
user_query = st.chat_input("Type your SPEC macro request here…")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Code generation
    result, err = run_with_timeout(run_codegen_ui, user_query, timeout_s=60)
    badge = "<span class='agent-badge'>🛠️ CODE AGENT</span>"

    if err or not result:
        code_out = 'print "error or timeout"'
        with st.chat_message("assistant"):
            st.markdown(badge, unsafe_allow_html=True)
            st.code(code_out, language="spec")
            st.markdown(f"<div class='warn'>Detail: {err or 'unknown'}</div>", unsafe_allow_html=True)
        log_event("error", {"agent": "code", "query": user_query, "error": err or "unknown"})
        st.session_state.messages.append({
            "role": "assistant",
            "badge_html": badge,
            "code_block": code_out,
            "footnote": f"<div class='warn'>Detail: {err or 'unknown'}</div>"
        })

    else:
        code = (result.get("code") or "").strip() or 'print "insufficient evidence"'
        retrieved = result.get("retrieved", [])
        debug_info = result.get("debug", {})

        with st.chat_message("assistant"):
            st.markdown(badge, unsafe_allow_html=True)
            st.code(code, language="spec")

            if st.session_state.show_debug:
                with st.expander("🔎 Debug Info"):
                    st.write(debug_info)

            if retrieved:
                with st.expander(f"📚 Retrieved Chunks ({len(retrieved)})"):
                    for i, chunk in enumerate(retrieved, 1):
                        st.markdown(f"**[{i}]** score={chunk['score']:.4f} src={chunk['source']}  \n"
                                    f"{chunk['snippet']}...")

        st.session_state.messages.append({
            "role": "assistant",
            "badge_html": badge,
            "code_block": code
        })
