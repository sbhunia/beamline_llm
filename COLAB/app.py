# from __future__ import annotations
# import streamlit as st

# # ===============================
# # IMPORT YOUR REAL BACKEND
# # ===============================
# from rag_engine import ask_rag   # <-- THIS IS YOUR REAL GEMINI+FAISS CODE

# # ===============================
# # PAGE CONFIG
# # ===============================

# st.set_page_config(
#     page_title="QM2 Assistant",
#     page_icon="🤖",
#     layout="wide",
# )

# # ===============================
# # GLOBAL CSS (UNCHANGED LOOK)
# # ===============================

# st.markdown(
#     """
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

# html, body, [class*="block-container"] {
#     font-family: "Inter", sans-serif !important;
#     background: #f5f6fa !important;
# }

# .block-container {
#     padding-top: 90px !important;
# }

# /* TOP BAR */
# .topbar {
#     background: linear-gradient(90deg, #b50f2b, #d41f3c);
#     height: 60px;
#     position: fixed;
#     top: 0; left: 0; right: 0;
#     z-index: 9999;
#     display: flex;
#     align-items: center;
#     padding: 0 24px;
#     box-shadow: 0 2px 8px rgba(0,0,0,0.15);
# }
# .topbar-title {
#     color: #fff;
#     font-size: 26px;
#     font-weight: 800;
# }
# .topbar-logo {
#     margin-left: auto;
#     color: #fff;
#     font-size: 30px;
#     font-weight: 900;
# }

# /* PLAQUE */
# .plaque {
#     background: #ffffff;
#     padding: 18px 26px;
#     border-radius: 12px;
#     font-size: 20px;
#     font-weight: 800;
#     text-align: center;
#     box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
#     margin-bottom: 12px;
# }

# /* SUBTEXT */
# .helper {
#     text-align: center;
#     font-size: 15px;
#     color: #676767;
#     margin-bottom: 20px;
# }

# /* CHAT */
# .stChatMessage {
#     background: #ffffff !important;
#     border-radius: 16px !important;
#     padding: 16px !important;
#     box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
# }
# .stChatMessage[data-testid="stChatMessageUser"] {
#     background: #e6f3ff !important;
#     border-left: 4px solid #1f77d0 !important;
# }
# .stChatMessage[data-testid="stChatMessageAssistant"] {
#     background: #fef6f6 !important;
#     border-left: 4px solid #c71c2b !important;
# }

# /* BADGE */
# .agent-badge {
#     background: #ffecef;
#     padding: 5px 10px;
#     border-radius: 8px;
#     font-weight: 700;
#     font-size: 12px;
#     color: #b50f2b;
#     border: 1px solid #f9cbd2;
#     display: inline-block;
#     margin-bottom: 6px;
# }

# /* SIDEBAR */
# section[data-testid="stSidebar"] {
#     background: #fafbff !important;
#     box-shadow: 2px 0px 8px rgba(0,0,0,0.08);
# }

# /* BUTTONS */
# .stButton>button {
#     background: linear-gradient(90deg, #b50f2b, #d41f3c) !important;
#     color: white !important;
#     border-radius: 8px !important;
#     padding: 8px 20px !important;
#     font-weight: 600 !important;
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ===============================
# # TOP BAR
# # ===============================

# st.markdown(
#     """
# <div class="topbar">
#   <div class="topbar-title">QM2 Assistant</div>
#   <div class="topbar-logo">M</div>
# </div>
# """,
#     unsafe_allow_html=True,
# )

# st.markdown("<div class='plaque'>QM2 ASSISTANT</div>", unsafe_allow_html=True)
# st.markdown(
#     "<div class='helper'>Ask questions about HDRM / SPEC documentation.</div>",
#     unsafe_allow_html=True,
# )

# # ===============================
# # SESSION STATE
# # ===============================

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ===============================
# # SIDEBAR
# # ===============================

# with st.sidebar:
#     if st.button("New chat"):
#         st.session_state.messages = []
#         st.rerun()

#     st.markdown("### History")
#     user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
#     for i, msg in enumerate(user_msgs[-5:][::-1], 1):
#         label = (msg["content"][:30] + "…") if len(msg["content"]) > 30 else msg["content"]
#         if st.button(label, key=f"hist_{i}"):
#             st.session_state.messages.append(msg)
#             st.rerun()

# # ===============================
# # REPLAY CHAT
# # ===============================

# for m in st.session_state.messages:
#     with st.chat_message(m["role"]):
#         if m["role"] == "assistant":
#             st.markdown("<span class='agent-badge'> RAG AGENT</span>", unsafe_allow_html=True)
#         st.markdown(m["content"], unsafe_allow_html=True)

# # ===============================
# # CHAT INPUT (REAL RAG CALL)
# # ===============================

# user_query = st.chat_input("Type your question here…")

# if user_query:
#     # Show user message
#     with st.chat_message("user"):
#         st.markdown(user_query)

#     st.session_state.messages.append(
#         {"role": "user", "content": user_query}
#     )

#     # BACKEND CALL
#     with st.chat_message("assistant"):
#         st.markdown("<span class='agent-badge'> RAG AGENT</span>", unsafe_allow_html=True)
#         with st.spinner("Searching documents and querying Gemini…"):
#             answer = ask_rag(user_query)
#         st.markdown(answer, unsafe_allow_html=True)

#     st.session_state.messages.append(
#         {"role": "assistant", "content": answer}
#     )
from __future__ import annotations
import streamlit as st
import json
import os

# Import your modified Gemini backend
from rag_engine import ask_rag 

# ===============================
# PAGE CONFIG & CSS (Keep your existing styles)
# ===============================
st.set_page_config(page_title="QM2 Assistant", page_icon="🤖", layout="wide")

# ... (Include your CSS block here) ...

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR (Improved History)
# ===============================
with st.sidebar:
    st.title("Settings")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Evaluation File")
    # This checks if your benchmark file is present for testing
    if os.path.exists("faq_benchmark.json"):
        st.success(" benchmark.json found")
    else:
        st.warning("⚠️ benchmark.json not found")

# ===============================
# CHAT DISPLAY
# ===============================
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "assistant":
            st.markdown("<span class='agent-badge'> RAG AGENT</span>", unsafe_allow_html=True)
            st.markdown(m["content"])
            # Display sources if they exist in history
            if "sources" in m:
                with st.expander("View Retrieved Sources"):
                    for src in m["sources"]:
                        st.write(f"**Source:** {src['source_file']}")
                        st.caption(src['content'])
        else:
            st.markdown(m["content"])

# ===============================
# CHAT INPUT
# ===============================
user_query = st.chat_input("Type your question here…")

if user_query:
    # 1. Show & Save User Query
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Call Backend
    with st.chat_message("assistant"):
        st.markdown("<span class='agent-badge'> RAG AGENT</span>", unsafe_allow_html=True)
        
        with st.spinner("Gemini is thinking..."):
            # This now returns {'answer': '...', 'retrieved': [...]}
            response_dict = ask_rag(user_query)
            
            full_answer = response_dict["answer"]
            sources = response_dict["retrieved"]
            
        # 3. Display Answer
        st.markdown(full_answer)
        
        # 4. Display Sources (The "Ollama-style" source list)
        with st.expander("Retrieved Sources"):
            for item in sources:
                st.write(f"**{item['source_file']}**")
                st.info(item['content'])

    # 5. Save to History
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_answer,
        "sources": sources
    })