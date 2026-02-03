import os
import re
import math
from collections import Counter
import pandas as pd


# ============================================================
# NORMALIZATION / TOKENIZATION
# ============================================================

def normalize_text(text, keep_case=False, remove_comments=False, code_mode=True):
    if text is None or (isinstance(text, float) and math.isnan(text)):
        return ""
    s = str(text)
    if remove_comments:
        s = "\n".join(
            line for line in s.splitlines()
            if not line.strip().startswith("#") and not line.strip().startswith("//")
        )
    if not keep_case:
        s = s.lower()
    if code_mode:
        s = s.replace('\r', '').replace('\t', ' ')
        s = re.sub(r'[ ]+', ' ', s)
        return s.strip()
    s = re.sub(r'`{3}.*?`{3}', '', s, flags=re.S)
    s = re.sub(r'[^a-z0-9\s\.\:\_\#\-]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def tokens(text, code_mode=True):
    return normalize_text(text, code_mode=code_mode).split()


def ngrams(tokens_list, n):
    if len(tokens_list) < n:
        return []
    return [tuple(tokens_list[i:i+n]) for i in range(len(tokens_list) - n + 1)]


# ============================================================
# METRIC UTILITIES
# ============================================================

def modified_precision(reference, hypothesis, n, code_mode=True):
    ref_toks = tokens(reference, code_mode)
    hyp_toks = tokens(hypothesis, code_mode)
    ref_ngrams = Counter(ngrams(ref_toks, n))
    hyp_ngrams = Counter(ngrams(hyp_toks, n))
    overlap = sum(min(cnt, ref_ngrams.get(ng, 0)) for ng, cnt in hyp_ngrams.items())
    total = max(sum(hyp_ngrams.values()), 1)
    return overlap / total


def brevity_penalty(ref_len, hyp_len):
    if hyp_len == 0:
        return 0.0
    if hyp_len > ref_len:
        return 1.0
    return math.exp(1 - ref_len / hyp_len)


def sentence_bleu(reference, hypothesis, max_n=4, code_mode=True):
    precisions = [modified_precision(reference, hypothesis, i + 1, code_mode) for i in range(max_n)]
    eps = 1e-12
    log_prec = sum((1 / max_n) * math.log(p + eps) for p in precisions)
    hyp_len = len(tokens(hypothesis, code_mode))
    ref_len = len(tokens(reference, code_mode))
    bp = brevity_penalty(ref_len, hyp_len)
    bleu = bp * math.exp(log_prec)
    return min(max(bleu, 0.0), 1.0), precisions, bp


def lcs_length(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            dp[i][j] = 1 + dp[i+1][j+1] if a[i] == b[j] else max(dp[i+1][j], dp[i][j+1])
    return dp[0][0]


def rouge_n(reference, hypothesis, n=1, code_mode=True):
    ref_toks = tokens(reference, code_mode)
    hyp_toks = tokens(hypothesis, code_mode)
    ref_ngrams = Counter(ngrams(ref_toks, n))
    hyp_ngrams = Counter(ngrams(hyp_toks, n))
    overlap = sum(min(ref_ngrams.get(ng, 0), cnt) for ng, cnt in hyp_ngrams.items())
    recall = overlap / max(sum(ref_ngrams.values()), 1)
    precision = overlap / max(sum(hyp_ngrams.values()), 1)
    f1 = 0 if recall + precision == 0 else 2 * recall * precision / (recall + precision)
    return {"f1": f1}


def rouge_l(reference, hypothesis, code_mode=True):
    ref_toks = tokens(reference, code_mode)
    hyp_toks = tokens(hypothesis, code_mode)
    lcs = lcs_length(ref_toks, hyp_toks)
    if not ref_toks or not hyp_toks:
        return {"f1": 0}
    recall = lcs / len(ref_toks)
    precision = lcs / len(hyp_toks)
    f1 = 0 if recall + precision == 0 else 2 * recall * precision / (recall + precision)
    return {"f1": f1}


def exact_match(reference, hypothesis, code_mode=True):
    return 1.0 if normalize_text(reference, code_mode=code_mode) == normalize_text(hypothesis, code_mode=code_mode) else 0.0


def compute_all(reference, hypothesis, code_mode=True):
    bleu, precisions, bp = sentence_bleu(reference, hypothesis, code_mode=code_mode)
    r1 = rouge_n(reference, hypothesis, 1, code_mode)
    r2 = rouge_n(reference, hypothesis, 2, code_mode)
    rl = rouge_l(reference, hypothesis, code_mode)
    return {
        "EM": exact_match(reference, hypothesis, code_mode),
        "BLEU": bleu,
        "BLEU_p1": precisions[0],
        "BLEU_p2": precisions[1],
        "BLEU_p3": precisions[2],
        "BLEU_p4": precisions[3],
        "BLEU_BP": bp,
        "ROUGE-1_f1": r1["f1"],
        "ROUGE-2_f1": r2["f1"],
        "ROUGE-L_f1": rl["f1"],
    }


# ============================================================
# MULTI-REFERENCE SUPPORT
# ============================================================

def parse_references(cell):
    if cell is None or (isinstance(cell, float) and math.isnan(cell)):
        return []
    text = str(cell).strip()

    # explicit separator
    if "|||" in text:
        return [p.strip() for p in text.split("|||") if p.strip()]

    # blank line separator
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    return parts if len(parts) > 1 else [text]


# ============================================================
# SCORING LOGIC
# ============================================================

def score_collated_df(df, ref_col, model_cols, latency_cols, code_mode=True):
    records = []
    per_model = {m: [] for m in model_cols}

    for idx, row in df.iterrows():
        refs = parse_references(row[ref_col])
        if not refs:
            continue

        for model in model_cols:
            hyp = row.get(model, "")
            best = None
            best_ref = None

            for r in refs:
                sc = compute_all(r, hyp, code_mode=code_mode)
                if best is None or sc["BLEU"] > best["BLEU"]:
                    best = sc
                    best_ref = r

            lat = None
            for lc in latency_cols:
                if model.lower().replace(" ", "") in lc.lower().replace(" ", ""):
                    val = row.get(lc, None)
                    try:
                        lat = float(val)
                    except:
                        lat = None

            rec = {
                "index": idx,
                "model": model,
                "hypothesis": hyp,
                "reference_used": best_ref,
                "latency_ms": lat,
            }
            rec.update(best)
            records.append(rec)
            per_model[model].append(rec)

    out_df = pd.DataFrame(records)

    summary = []
    for m, rows in per_model.items():
        if not rows:
            continue
        dfm = pd.DataFrame(rows)
        avg = dfm[["EM","BLEU","BLEU_p1","BLEU_p2","BLEU_p3","BLEU_p4","ROUGE-1_f1","ROUGE-2_f1","ROUGE-L_f1"]].mean()
        summary.append({
            "model": m,
            **avg.to_dict(),
            "avg_latency_ms": dfm["latency_ms"].mean(),
            "n_examples": len(dfm)
        })

    summary_df = pd.DataFrame(summary).set_index("model")
    return out_df, summary_df


# ============================================================
# MAIN (FIXED PATH)
# ============================================================

def main():
    INPUT_PATH = "/home/vallurs/research/data/scoring/master_table.csv"
    OUT_DIR = "/home/vallurs/research/data/scoring/score_results"

    print("Reading:", INPUT_PATH)
    df = pd.read_csv(INPUT_PATH)

    model_cols = [
        "Llama3 Output",
        "CodeLlama Output",
        "Mistral Output",
        "Deepseek-1.5 Output"
    ]

    latency_cols = [
        "Llama3 Latency (ms)",
        "CodeLlama Latency (ms)",
        "Mistral Latency (ms)",
        "Deepseek-1.5 Latency (ms)"
    ]

    ref_col = "Original Answer"

    out_df, summary_df = score_collated_df(
        df,
        ref_col=ref_col,
        model_cols=model_cols,
        latency_cols=latency_cols,
        code_mode=True
    )

    os.makedirs(OUT_DIR, exist_ok=True)

    per_ex_path = os.path.join(OUT_DIR, "per_example_scores.csv")
    summary_path = os.path.join(OUT_DIR, "summary_by_model.csv")

    out_df.to_csv(per_ex_path, index=False)
    summary_df.to_csv(summary_path)

    print("\n======================================")
    print("SCORING COMPLETE")
    print("Per-example scores:", per_ex_path)
    print("Summary by model:", summary_path)
    print("======================================\n")


if __name__ == "__main__":
    main()
