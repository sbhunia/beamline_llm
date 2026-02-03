from __future__ import annotations

import sys
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from scripts.Text_agent.textgen_agent import run_text_ui


# ---------------- Timeout wrapper ----------------

def run_with_timeout(func, *args, timeout_s: int = 60, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func, *args, **kwargs)
        try:
            return fut.result(timeout=timeout_s), None
        except _TOError as e:
            return None, f"timeout: {e}"
        except Exception as e:
            return None, f"error: {e}"


# ---------------- Page config ----------------

st.set_page_config(
    page_title="QM2 Text Assistant",
    page_icon="📄",
    layout="wide",
)

# ---------------- Header ----------------

st.markdown(
    """
<style>
.block-container { padding-top: 80px !important; }
.agent-badge {
    background: #eef2ff;
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 12px;
    color: #3730a3;
    border: 1px solid #c7d2fe;
}
.warn {
    background: #fff4e5;
    border-left: 4px solid #ff9800;
    padding: 10px 14px;
    color: #8a4b00;
    border-radius: 8px;
    margin-top: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h2 style='text-align:center;'>QM2 Documentation Assistant</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#666;'>Answers are generated from markdown documentation</p>",
    unsafe_allow_html=True,
)

# ---------------- Session state ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- Sidebar ----------------

with st.sidebar:
    if st.button("New chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Recent questions")
    for i, m in enumerate(
        [x for x in st.session_state.messages if x["role"] == "user"][-5:][::-1],
        1,
    ):
        label = m["content"][:30] + ("…" if len(m["content"]) > 30 else "")
        if st.button(label, key=f"hist_{i}"):
            st.session_state.messages.append(
                {"role": "user", "content": m["content"]}
            )
            st.rerun()


# ---------------- Replay history ----------------

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "assistant":
            st.markdown(
                "<span class='agent-badge'> TEXT AGENT</span>",
                unsafe_allow_html=True,
            )
        st.markdown(m["content"])


# ---------------- Chat input ----------------

user_query = st.chat_input("Ask about procedures, commands, or setup…")

if user_query:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    # Call text agent
    result, err = run_with_timeout(run_text_ui, user_query)

    with st.chat_message("assistant"):
        st.markdown(
            "<span class='agent-badge'> TEXT AGENT</span>",
            unsafe_allow_html=True,
        )

        if err or not result:
            assistant_msg = "Not found in the provided documents."
            st.markdown(assistant_msg)
            st.markdown(
                f"<div class='warn'>Detail: {err or 'unknown error'}</div>",
                unsafe_allow_html=True,
            )
        else:
            assistant_msg = result.get("answer") or "Not found in the provided documents."
            st.markdown(assistant_msg)

            # 🔍 Retrieved chunks debug panel
            retrieved = result.get("retrieved", [])
            if retrieved:
                with st.expander(f"🔎 Retrieved chunks ({len(retrieved)})"):
                    for i, r in enumerate(retrieved, 1):
                        st.markdown(
                            f"""
**[{i}] Source:** `{r['source']}`  
**Kind:** `{r['kind']}`  
**Score:** `{r['score']:.4f}`
{r['snippet']}
"""
                        )

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_msg}
    )
