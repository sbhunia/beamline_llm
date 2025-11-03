from __future__ import annotations
import os, time, statistics, uuid
from typing import Dict, Any, List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

from scripts.load_drive_code import load_drive_docs
from scripts.log_utils import log_stage, log_event
from scripts.query_rewrite import rewrite_user_query, normalize_macro_query
from scripts.prompt_template import BASE_PROMPT_CODE
from scripts.spec_parser import validate_spec_code

OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("CODE_MODEL", "codellama:7b-instruct")
TOP_K = int(os.getenv("RAG_TOP_K", "8"))
_VS: FAISS | None = None

# ---------- vector store ----------
def _build_vs(request_id: str) -> FAISS:
    global _VS
    if _VS: return _VS
    docs: List[Document] = load_drive_docs() or [
        Document(page_content="SPEC macro reference placeholder.", metadata={"source":"dummy"})
    ]
    emb_model = "sentence-transformers/all-mpnet-base-v2"
    emb = HuggingFaceEmbeddings(model_name=emb_model)
    _VS = FAISS.from_documents(docs, emb)
    log_stage("vectorstore_init", {
        "agent":"code","request_id":request_id,"source":"load_drive_docs",
        "vector_dim":768,
        "retrieved":f"chunks={len(docs)}, emb_model={emb_model}"
    })
    return _VS

# ---------- retrieval ----------
def _search(task: str, vs: FAISS, request_id: str, k: int=TOP_K) -> Tuple[List[Tuple[Document,float]], float]:
    query_vec = vs.embedding_function.embed_query(task)
    log_stage("embedding_query",{
        "agent":"code","request_id":request_id,
        "vector_dim":len(query_vec),"vector_preview":[round(x,5) for x in query_vec[:10]]
    })
    hits = vs.similarity_search_with_score(task,k=k)
    keywords=["def ","ascan","flyscan","macro","loop","if","umv","open","close"]
    boosted=[]
    for doc,score in hits:
        if any(kw in (doc.page_content or "").lower() for kw in keywords):
            boosted.append((doc,score*0.9))
    merged=sorted(hits+boosted,key=lambda x:x[1])[:k]
    scores=[float(s) for _,s in merged]
    best,avg,spread=min(scores),statistics.mean(scores),max(scores)-min(scores)
    confidence=round(1/(1+avg),4)
    log_stage("retrieval",{
        "agent":"code","request_id":request_id,
        "retrieved":[{"source":d.metadata.get("source","unknown"),
                      "score":float(s),
                      "snippet":d.page_content} for d,s in merged],
        "best_score":best,"avg_score":avg,"spread":spread,"confidence":confidence
    })
    return merged,confidence

# ---------- LLM ----------
def _call_llm(prompt:str,request_id:str)->Tuple[str,float]:
    start=time.time()
    llm=ChatOllama(model=DEFAULT_MODEL,base_url=OLLAMA_BASE,temperature=0.0)
    out=llm.invoke([{"role":"user","content":prompt}])
    latency=(time.time()-start)*1000
    response=getattr(out,"content",str(out)) or ""
    log_stage("llm_call",{
        "agent":"code","request_id":request_id,
        "model":DEFAULT_MODEL,"latency_ms":round(latency,2),
        "prompt_chars":len(prompt),"prompt_full":prompt,"llm_output_full":response
    })
    return response,latency

# ---------- main ----------
def run_codegen_ui(task:str)->Dict[str,Any]:
    request_id="REQ_"+uuid.uuid4().hex[:8]

    # event: query received
    log_event("user_query_received",{
        "agent":"code","request_id":request_id,
        "original_query":task,"method":"llm-rag"
    })

    # event: rewrite
    normalized=normalize_macro_query(task)
    rewritten=rewrite_user_query(normalized)
    log_event("query_rewrite",{
        "agent":"code","request_id":request_id,
        "original_query":task,"normalized_query":normalized,
        "rewritten_query":rewritten
    })

    # build vs & search
    vs=_build_vs(request_id)
    hits,confidence=_search(rewritten,vs,request_id,k=TOP_K)

    # assemble prompt
    retrieved_chunks=[{
        "source":d.metadata.get("source","unknown"),
        "score":float(s),"snippet":d.page_content
    } for d,s in hits]
    rag_blob="\n\n---\n\n".join([r["snippet"] for r in retrieved_chunks])
    prompt=BASE_PROMPT_CODE.format(task=rewritten,manual=rag_blob)
    prompt_tokens_est=len(prompt)//4
    log_stage("prompt",{
        "agent":"code","request_id":request_id,
        "prompt_chars":len(prompt),"prompt_tokens_est":prompt_tokens_est,
        "retrieved":[r["source"] for r in retrieved_chunks],
        "retrieved_full":rag_blob,"prompt_full":prompt
    })

    # model call
    raw_out,latency=_call_llm(prompt,request_id)
    draft=(raw_out or "").strip()

    # parser
    parser_ok=validate_spec_code(draft)
    log_stage("parser_check",{
        "agent":"code","request_id":request_id,
        "parser_passed":parser_ok,"parser_result":str(parser_ok),"parser_input":draft
    })

    # final
    log_stage("final",{
        "agent":"code","request_id":request_id,
        "confidence":confidence,"latency_ms":round(latency,2),
        "parser_passed":parser_ok,"final_output_full":draft
    })

    # ui return
    log_event("ui_return",{
        "agent":"code","request_id":request_id,
        "original_query":task,"rewritten_query":rewritten,
        "confidence":confidence,"parser_passed":parser_ok,
        "sources":[r["source"] for r in retrieved_chunks],
        "prompt_chars":len(prompt),"prompt_full":prompt,
        "retrieved_full":rag_blob,"llm_output_full":draft,
        "final_output_full":draft,"preview":draft
    })

    return {
        "code":draft or 'print "insufficient evidence"',
        "retrieved":retrieved_chunks,
        "debug":{
            "exact_prompt":prompt,
            "rag_context":rag_blob,
            "raw_output":raw_out,
            "confidence_est":confidence,
            "parser_ok":parser_ok,
            "latency_ms":latency,
            "scores":{
                "best":min([r["score"] for r in retrieved_chunks]) if retrieved_chunks else None,
                "avg":statistics.mean([r["score"] for r in retrieved_chunks]) if retrieved_chunks else None,
                "spread":(max([r["score"] for r in retrieved_chunks])-min([r["score"] for r in retrieved_chunks])) if len(retrieved_chunks)>1 else None,
                "confidence":confidence
            }
        },
        "method":"llm-rag"
    }
