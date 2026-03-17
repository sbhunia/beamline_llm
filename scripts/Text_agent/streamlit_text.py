from __future__ import annotations

import sys
import os
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _TOError

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from textgen_agent import ask_rag
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer


def run_with_timeout(func, *args, timeout_s: int = 120, **kwargs):
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func, *args, **kwargs)
        try:
            return fut.result(timeout=timeout_s), None
        except _TOError as e:
            return None, f"timeout: {e}"
        except Exception as e:
            return None, f"error: {e}"



@st.cache_resource
def load_embedder():
    return SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

embed_model = load_embedder()


def compute_similarity(a, b):
    emb1 = embed_model.encode([a])
    emb2 = embed_model.encode([b])
    return float(cosine_similarity(emb1, emb2)[0][0])


rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)


# @st.cache_data
# def load_benchmark():
#     with open("faq_benchmark.json", "r") as f:
#         return json.load(f)

# benchmark = load_benchmark()

st.set_page_config(
    page_title="QM2 Text Assistant",
    page_icon="📄",
    layout="wide",
)

st.markdown("<h2 style='text-align:center;'>QM2 Documentation Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#666;'>Answers are generated from markdown documentation</p>", unsafe_allow_html=True)



if "messages" not in st.session_state:
    st.session_state.messages = []


for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if "eval_entries" in m:
            for eval_item in m["eval_entries"]:
                st.markdown("---")
                st.markdown(f"### Evaluation for: {eval_item['question']}")
                st.markdown(f"**Field Match Accuracy:** {eval_item['field_accuracy']:.2f}")
                
                if eval_item['field_accuracy'] == 1.0:
                    st.success("All required fields present — correct")
                elif eval_item['field_accuracy'] > 0:
                    st.warning("Partially correct — some required fields missing")
                    for mf in eval_item['missing_fields']:
                        st.markdown(f"- {mf}")
                else:
                    st.error("Required information not found in answer")

                st.markdown(f"**Cosine Similarity:** {eval_item['similarity_score']:.4f}")
                st.markdown(f"**ROUGE-L (F1):** {eval_item['rouge_l']:.4f}")


user_query = st.chat_input("Ask about procedures, commands, or setup…")

if user_query:

    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    result, err = run_with_timeout(ask_rag, user_query)

    with st.chat_message("assistant"):

        if err or not result:
            assistant_msg = "Not found in the provided documents."
            st.markdown(assistant_msg)
            st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

            if err:
                st.error(err)

        else:
            assistant_msg = result["answer"]
            st.markdown(assistant_msg)
            
            eval_entries_for_storage = []

            matched_entries = []
            for item in benchmark:
                sim = compute_similarity(user_query, item["question"])
                if sim > 0.85:
                    matched_entries.append(item)

            for gt_entry in matched_entries:
                st.markdown("---")
                st.markdown(f"### Evaluation for: {gt_entry['question']}")

                gt_fields = gt_entry["ground_truth"]["fields"]
                gt_full_answer = gt_entry["ground_truth"]["full_answer"]

                gt_values = list(gt_fields.values())
                assistant_lower = assistant_msg.lower()

                matched = 0
                missing_fields = []
                for value in gt_values:
                    if value.lower() in assistant_lower:
                        matched += 1
                    else:
                        missing_fields.append(value)

                field_accuracy = matched / len(gt_values)
                st.markdown(f"**Field Match Accuracy:** {field_accuracy:.2f}")

                if field_accuracy == 1.0:
                    st.success("All required fields present — correct")
                elif field_accuracy > 0:
                    st.warning("Partially correct — some required fields missing")
                    st.markdown("**Missing fields:**")
                    for mf in missing_fields:
                        st.markdown(f"- {mf}")
                else:
                    st.error("Required information not found in answer")

                # -------- Cosine Similarity --------
                similarity_score = compute_similarity(assistant_msg, gt_full_answer)
                st.markdown(f"**Cosine Similarity:** {similarity_score:.4f}")

                # -------- ROUGE-L --------
                rouge_scores = rouge.score(gt_full_answer, assistant_msg)
                rouge_l = rouge_scores["rougeL"].fmeasure
                st.markdown(f"**ROUGE-L (F1):** {rouge_l:.4f}")
                
                eval_entries_for_storage.append({
                    "question": gt_entry['question'],
                    "field_accuracy": field_accuracy,
                    "missing_fields": missing_fields,
                    "similarity_score": similarity_score,
                    "rouge_l": rouge_l
                })

            retrieved = result.get("retrieved", [])
            if retrieved:
                with st.expander(f" Retrieved chunks ({len(retrieved)})"):
                    for i, r in enumerate(retrieved, 1):
                        st.markdown(f"**Chunk {i} | Score: {r['score']:.4f}** \nFile: `{r.get('source_file')}`")
                        st.code(r["content"])

            st.session_state.messages.append({
                "role": "assistant", 
                "content": assistant_msg,
                "eval_entries": eval_entries_for_storage
            })