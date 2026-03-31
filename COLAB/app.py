from __future__ import annotations
import streamlit as st
from rag_engine import ask_rag, rebuild_indexes

# PAGE CONFIG

st.set_page_config(
    page_title="QM2 Assistant",
    page_icon="🤖",
    layout="wide",
)

 # GLOBAL CSS  

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

/* ── FORCE LIGHT MODE ─────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], [data-testid="stHeader"],
[data-testid="stSidebar"], .stChatFloatingInputContainer,
[data-baseweb="base-input"], [data-baseweb="textarea"],
.stTextInput, .stChatInput {
    color-scheme: light !important;
    background-color: #f5f6fa !important;
    color: #1a1a1a !important;
}

/* Force all text to dark */
html, body, p, span, div, label, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText {
    color: #1a1a1a !important;
}

/* ── BASE FONTS & BACKGROUND ──────────────────────────────── */
html, body, [class*="block-container"] {
    font-family: "Inter", sans-serif !important;
    background: #f5f6fa !important;
}

.block-container {
    padding-top: 90px !important;
}

/* ── TOP BAR ──────────────────────────────────────────────── */
.topbar {
    background: linear-gradient(90deg, #b50f2b, #d41f3c);
    height: 60px;
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    padding: 0 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.topbar-title {
    color: #fff !important;
    font-size: 26px;
    font-weight: 800;
}
.topbar-logo {
    margin-left: auto;
    color: #fff !important;
    font-size: 30px;
    font-weight: 900;
}

/* ── PLAQUE ───────────────────────────────────────────────── */
.plaque {
    background: #ffffff !important;
    padding: 18px 26px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    margin-bottom: 12px;
    color: #1a1a1a !important;
}

/* ── SUBTEXT ──────────────────────────────────────────────── */
.helper {
    text-align: center;
    font-size: 15px;
    color: #676767 !important;
    margin-bottom: 20px;
}

/* ── CHAT MESSAGES ────────────────────────────────────────── */
.stChatMessage {
    background: #ffffff !important;
    border-radius: 16px !important;
    padding: 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
}
.stChatMessage[data-testid="stChatMessageUser"] {
    background: #e6f3ff !important;
    border-left: 4px solid #1f77d0 !important;
}
.stChatMessage[data-testid="stChatMessageAssistant"] {
    background: #fef6f6 !important;
    border-left: 4px solid #c71c2b !important;
}

/* ── AGENT BADGE ──────────────────────────────────────────── */
.agent-badge {
    background: #ffecef;
    padding: 5px 10px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 12px;
    color: #b50f2b !important;
    border: 1px solid #f9cbd2;
    display: inline-block;
    margin-bottom: 6px;
}

/* ── SIDEBAR ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #fafbff !important;
    box-shadow: 2px 0px 8px rgba(0,0,0,0.08);
}

/* ── BUTTONS ──────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(90deg, #b50f2b, #d41f3c) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    border: none !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #9a0b24, #b50f2b) !important;
}

/* ── CHAT INPUT BOX ───────────────────────────────────────── */
.stChatInput textarea,
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #1a1a1a !important;
    border: 1px solid #dde1ea !important;
    border-radius: 12px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# TOP BAR

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
    "<div class='helper'>Ask questions about HDRM / SPEC / Lakeshore / Cryocooler documentation.</div>",
    unsafe_allow_html=True,
)

# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR

with st.sidebar:
    if st.button("🗑️ New chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    if st.button("🔄 Rebuild indexes"):
        with st.spinner("Rebuilding FAISS indexes from source files…"):
            rebuild_indexes()
        st.success("Indexes rebuilt!")

    st.markdown("---")
    st.markdown("### History")
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    for i, msg in enumerate(user_msgs[-5:][::-1], 1):
        label = (msg["content"][:30] + "…") if len(msg["content"]) > 30 else msg["content"]
        if st.button(label, key=f"hist_{i}"):
            st.session_state.messages.append(msg)
            st.rerun()

# REPLAY CHAT

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "assistant":
            st.markdown("<span class='agent-badge'> RAG AGENT</span>", unsafe_allow_html=True)
        st.markdown(m["content"], unsafe_allow_html=True)

# CHAT INPUT

user_query = st.chat_input("Type your question here…")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        st.markdown("<span class='agent-badge'> RAG AGENT</span>", unsafe_allow_html=True)
        with st.spinner("Searching markdown & PDF documents…"):
            answer = ask_rag(user_query)
        st.markdown(answer, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer})