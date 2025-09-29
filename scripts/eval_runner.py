import json, time, argparse, yaml
from rouge_score import rouge_scorer
from scripts.router import route as route_query
from scripts.codegen_agent import run_codegen_ui
from scripts.text_agent import answer as text_answer

def run_case(q, ref):
    r_route,_,_=route_query(q)
    if r_route=="code":
        out=run_codegen_ui(q)
        pred=json.dumps(out,ensure_ascii=False)
        kind="code"
    else:
        pred,_=text_answer(q)
        kind="text"
    return kind,pred

def main(path):
    tests=yaml.safe_load(open(path,"r",encoding="utf-8"))
    scorer=rouge_scorer.RougeScorer(["rougeL"],use_stemmer=True)
    rows=[]
    for t in tests:
        q,ref=t["query"],t.get("reference","")
        kind,pred=run_case(q,ref)
        score=scorer.score(ref,pred)["rougeL"].fmeasure if kind=="text" and ref else None
        rows.append({"query":q,"kind":kind,"rougeL":score,"pred":pred[:500]})
        time.sleep(0.1)
    print(json.dumps(rows,indent=2,ensure_ascii=False))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--yaml",required=True)
    args=ap.parse_args()
    main(args.yaml)
