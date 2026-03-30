# from __future__ import annotations

# import sys
# import os
# import json
# from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError

# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# if PROJECT_ROOT not in sys.path:
#     sys.path.insert(0, PROJECT_ROOT)

# import streamlit as st
# from textgen_agent import ask_rag
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from rouge_score import rouge_scorer


# def run_with_timeout(func, *args, timeout_s: int = 120, **kwargs):
#     with ThreadPoolExecutor(max_workers=1) as ex:
#         fut = ex.submit(func, *args, **kwargs)
#         try:
#             return fut.result(timeout=timeout_s), None
#         except _TOError as e:
#             return None, f"timeout: {e}"
#         except Exception as e:
#             return None, f"error: {e}"



# @st.cache_resource
# def load_embedder():
#     return SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# embed_model = load_embedder()


# def compute_similarity(a, b):
#     emb1 = embed_model.encode([a])
#     emb2 = embed_model.encode([b])
#     return float(cosine_similarity(emb1, emb2)[0][0])


# rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)


# # @st.cache_data
# # def load_benchmark():
# #     with open("faq_benchmark.json", "r") as f:
# #         return json.load(f)

# # benchmark = load_benchmark()

# st.set_page_config(
#     page_title="QM2 Text Assistant",
#     page_icon="📄",
#     layout="wide",
# )

# st.markdown("<h2 style='text-align:center;'>QM2 Documentation Assistant</h2>", unsafe_allow_html=True)
# st.markdown("<p style='text-align:center;color:#666;'>Answers are generated from markdown documentation</p>", unsafe_allow_html=True)



# if "messages" not in st.session_state:
#     st.session_state.messages = []


# for m in st.session_state.messages:
#     with st.chat_message(m["role"]):
#         st.markdown(m["content"])
#         if "eval_entries" in m:
#             for eval_item in m["eval_entries"]:
#                 st.markdown("---")
#                 st.markdown(f"### Evaluation for: {eval_item['question']}")
#                 st.markdown(f"**Field Match Accuracy:** {eval_item['field_accuracy']:.2f}")
                
#                 if eval_item['field_accuracy'] == 1.0:
#                     st.success("All required fields present — correct")
#                 elif eval_item['field_accuracy'] > 0:
#                     st.warning("Partially correct — some required fields missing")
#                     for mf in eval_item['missing_fields']:
#                         st.markdown(f"- {mf}")
#                 else:
#                     st.error("Required information not found in answer")

#                 st.markdown(f"**Cosine Similarity:** {eval_item['similarity_score']:.4f}")
#                 st.markdown(f"**ROUGE-L (F1):** {eval_item['rouge_l']:.4f}")


# user_query = st.chat_input("Ask about procedures, commands, or setup…")

# if user_query:

#     with st.chat_message("user"):
#         st.markdown(user_query)

#     st.session_state.messages.append(
#         {"role": "user", "content": user_query}
#     )

#     result, err = run_with_timeout(ask_rag, user_query)

#     with st.chat_message("assistant"):

#         if err or not result:
#             assistant_msg = "Not found in the provided documents."
#             st.markdown(assistant_msg)
#             st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

#             if err:
#                 st.error(err)

#         else:
#             assistant_msg = result["answer"]
#             st.markdown(assistant_msg)
            
#             eval_entries_for_storage = []

#             matched_entries = []
#             for item in benchmark:
#                 sim = compute_similarity(user_query, item["question"])
#                 if sim > 0.85:
#                     matched_entries.append(item)

#             for gt_entry in matched_entries:
#                 st.markdown("---")
#                 st.markdown(f"### Evaluation for: {gt_entry['question']}")

#                 gt_fields = gt_entry["ground_truth"]["fields"]
#                 gt_full_answer = gt_entry["ground_truth"]["full_answer"]

#                 gt_values = list(gt_fields.values())
#                 assistant_lower = assistant_msg.lower()

#                 matched = 0
#                 missing_fields = []
#                 for value in gt_values:
#                     if value.lower() in assistant_lower:
#                         matched += 1
#                     else:
#                         missing_fields.append(value)

#                 field_accuracy = matched / len(gt_values)
#                 st.markdown(f"**Field Match Accuracy:** {field_accuracy:.2f}")

#                 if field_accuracy == 1.0:
#                     st.success("All required fields present — correct")
#                 elif field_accuracy > 0:
#                     st.warning("Partially correct — some required fields missing")
#                     st.markdown("**Missing fields:**")
#                     for mf in missing_fields:
#                         st.markdown(f"- {mf}")
#                 else:
#                     st.error("Required information not found in answer")

#                 # -------- Cosine Similarity --------
#                 similarity_score = compute_similarity(assistant_msg, gt_full_answer)
#                 st.markdown(f"**Cosine Similarity:** {similarity_score:.4f}")

#                 # -------- ROUGE-L --------
#                 rouge_scores = rouge.score(gt_full_answer, assistant_msg)
#                 rouge_l = rouge_scores["rougeL"].fmeasure
#                 st.markdown(f"**ROUGE-L (F1):** {rouge_l:.4f}")
                
#                 eval_entries_for_storage.append({
#                     "question": gt_entry['question'],
#                     "field_accuracy": field_accuracy,
#                     "missing_fields": missing_fields,
#                     "similarity_score": similarity_score,
#                     "rouge_l": rouge_l
#                 })

#             retrieved = result.get("retrieved", [])
#             if retrieved:
#                 with st.expander(f" Retrieved chunks ({len(retrieved)})"):
#                     for i, r in enumerate(retrieved, 1):
#                         st.markdown(f"**Chunk {i} | Score: {r['score']:.4f}** \nFile: `{r.get('source_file')}`")
#                         st.code(r["content"])

#             st.session_state.messages.append({
#                 "role": "assistant", 
#                 "content": assistant_msg,
#                 "eval_entries": eval_entries_for_storage
#             })

from __future__ import annotations
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError

try:
    from textgen_agent import (
        ask_rag,
        rebuild_indexes,
        check_ollama,
        AVAILABLE_MODELS,
        OLLAMA_BASE,
    )
except ImportError:
    from scripts.Text_agent.textgen_agent import (
        ask_rag,
        rebuild_indexes,
        check_ollama,
        AVAILABLE_MODELS,
        OLLAMA_BASE,
    )

# ===============================
# TIMEOUT HELPER
# ===============================

def run_with_timeout(func, *args, timeout_s: int = 180, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func, *args, **kwargs)
        try:
            return fut.result(timeout=timeout_s), None
        except _TOError:
            return None, "Request timed out. The model may be loading or too slow."
        except Exception as e:
            return None, str(e)

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="QM2 Assistant (Local)",
    page_icon="🖥️",
    layout="wide",
)

# ===============================
# CSS
# ===============================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="block-container"] {
    font-family: "Inter", sans-serif !important;
    background: #f5f6fa !important;
}

.block-container {
    padding-top: 90px !important;
}

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
    color: #fff;
    font-size: 26px;
    font-weight: 800;
}
.topbar-logo {
    margin-left: auto;
    color: #fff;
    font-size: 30px;
    font-weight: 900;
}

.plaque {
    background: #ffffff;
    padding: 18px 26px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 800;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    margin-bottom: 12px;
}

.helper {
    text-align: center;
    font-size: 15px;
    color: #676767;
    margin-bottom: 20px;
}

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

.agent-badge {
    background: #ffecef;
    padding: 5px 10px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 12px;
    color: #b50f2b;
    border: 1px solid #f9cbd2;
    display: inline-block;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] {
    background: #fafbff !important;
    box-shadow: 2px 0px 8px rgba(0,0,0,0.08);
}

.stButton>button {
    background: linear-gradient(90deg, #b50f2b, #d41f3c) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ===============================
# TOP BAR
# ===============================

st.markdown(
    """
<div class="topbar">
  <div class="topbar-title">QM2 Assistant (Local)</div>
  <div class="topbar-logo">M</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='plaque'>QM2 ASSISTANT — LOCAL MODELS</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='helper'>Ask questions about HDRM / SPEC / Lakeshore / Cryocooler documentation. Powered by Ollama.</div>",
    unsafe_allow_html=True,
)

# ===============================
# SESSION STATE
# ===============================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===============================
# SIDEBAR
# ===============================

with st.sidebar:
    st.markdown("### Ollama Model")

    if "ollama_status" not in st.session_state:
        running, pulled = check_ollama()
        st.session_state.ollama_running = running
        st.session_state.ollama_pulled = pulled
        st.session_state.ollama_status = True  # mark as checked

    ollama_running = st.session_state.ollama_running
    ollama_pulled  = st.session_state.ollama_pulled

    if ollama_running:
        st.success(f"Ollama connected — {len(ollama_pulled)} model(s) available")
        model_options = ollama_pulled if ollama_pulled else AVAILABLE_MODELS
    else:
        st.error(f"Ollama not detected at {OLLAMA_BASE}")
        st.markdown("Start Ollama with: `ollama serve`")
        model_options = AVAILABLE_MODELS

    selected_model = st.selectbox(
        "Choose model",
        options=model_options,
        index=0,
    )

    st.markdown("---")

    if st.button("🗑️ New chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔄 Rebuild indexes"):
        with st.spinner("Rebuilding FAISS indexes from source files…"):
            rebuild_indexes()
        st.success("Indexes rebuilt! Restart the app to use new indexes.")

    if st.button("🔃 Refresh Ollama"):
        running, pulled = check_ollama()
        st.session_state.ollama_running = running
        st.session_state.ollama_pulled = pulled
        st.rerun()

    st.markdown("---")
    st.markdown("### History")
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    for i, msg in enumerate(user_msgs[-5:][::-1], 1):
        label = (msg["content"][:30] + "…") if len(msg["content"]) > 30 else msg["content"]
        if st.button(label, key=f"hist_{i}"):
            st.session_state.messages.append(msg)
            st.rerun()

# ===============================
# REPLAY CHAT
# ===============================

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["role"] == "assistant" and "model" in m:
            st.markdown(
                f"<span class='agent-badge'>🖥️ {m['model']}</span>",
                unsafe_allow_html=True,
            )
        st.markdown(m["content"], unsafe_allow_html=True)

# ===============================
# CHAT INPUT
# ===============================

user_query = st.chat_input("Type your question here…")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        with st.spinner(f"Searching docs & querying {selected_model}…"):
            result, err = run_with_timeout(
                ask_rag, user_query, selected_model,
                timeout_s=180,
            )

        if err:
            st.error(f"Error: {err}")
            answer = "Request failed — see error above."
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "model": selected_model}
            )

        elif result is None:
            answer = "No response received."
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "model": selected_model}
            )

        else:
            answer = result["answer"]
            model_used = result.get("model", selected_model)

            st.markdown(
                f"<span class='agent-badge'>🖥️ {model_used}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(answer, unsafe_allow_html=True)

            retrieved = result.get("retrieved", [])
            if retrieved:
                with st.expander(f"📎 Retrieved chunks ({len(retrieved)})"):
                    for i, r in enumerate(retrieved, 1):
                        icon = "📄" if r["doc_type"] == "pdf" else "📝"
                        st.markdown(
                            f"**Chunk {i}** {icon} "
                            f"`{r['source']}` | Score: `{r['score']:.4f}`"
                        )
                        st.code(r["content"][:600])

            st.session_state.messages.append(
                {"role": "assistant", "content": answer, "model": model_used}
            )
