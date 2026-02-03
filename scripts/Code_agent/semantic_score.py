#!/usr/bin/env python3
"""
semantic_spec_scorer.py

Heuristic semantic scorer for SPEC-style tasks:
- Recognizes rotate/spin tasks and temperature set tasks
- Compares semantics (loop counts, angles/increments, temp target) rather than raw n-gram overlap

Usage: edit INPUT_PATH / OUT_DIR at the bottom and run:
    python semantic_spec_scorer.py
"""

import re
import math
import os
import pandas as pd

# ---------- helpers to extract numbers/keywords ----------
def find_integers(text):
    if text is None:
        return []
    return [int(x) for x in re.findall(r'\b(\d{1,4})\b', str(text))]

def find_floats(text):
    if text is None:
        return []
    return [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', str(text))]

def lower(x):
    return "" if x is None else str(x).lower()

# ---------- SPEC-specific extractors ----------
def extract_loop_count(text):
    """
    Heuristics to get loop count:
    - match for(...) constructs like for (i=0;i<10;...)
    - match "10 times", "spin 3 times", "3x", "for i 0 i 3 i" forms
    Returns int or None
    """
    s = lower(text)
    if not s:
        return None
    # common: for (i=0;i<10;i++) or for(i=0;i<10;i++)
    m = re.search(r'for\s*\(.*?[iI]\s*[<<=]+\s*(\d{1,4})', s)
    if m:
        return int(m.group(1))
    # forms like "for i 1 i 10 i"
    m = re.search(r'for\s+i\s+\d+\s+i\s+(\d{1,4})', s)
    if m:
        return int(m.group(1))
    # "10 times", "spin 3 times"
    m = re.search(r'\b(\d{1,4})\s*(?:times|x)\b', s)
    if m:
        return int(m.group(1))
    m = re.search(r'\bspin(?:\s+the)?\s*(?:crystal)?\s*(?:by)?\s*(\d{1,4})\b', s)
    if m:
        return int(m.group(1))
    # fallback: nearest small integer (<=100) found after "spin" or "rotate"
    if 'spin' in s or 'rotate' in s or 'rotat' in s:
        ints = find_integers(s)
        for i in ints:
            if i <= 100:  # reasonable loop count
                return i
    return None

def extract_rotation_angles_and_axes(text):
    """
    Find angle values and axis labels near rotation commands.
    Returns list of (axis, angle) pairs (angle as float)
    Recognizes patterns:
    - umv phi 360
    - inc or0 36
    - rotate 360
    - sspin / spin (may not include angle)
    """
    if text is None:
        return []
    s = str(text)
    s_low = s.lower()
    results = []
    # patterns: keyword axis? number
    # umv <axis> <num>
    for m in re.finditer(r'\b(?:umv|umvnt|umv_?)\s+([a-z0-9_]+)\s+(-?\d+\.?\d*)', s_low):
        axis = m.group(1)
        angle = float(m.group(2))
        results.append((axis, angle))
    # inc <axis> <num>
    for m in re.finditer(r'\binc\s+([a-z0-9_]+)\s+(-?\d+\.?\d*)', s_low):
        axis = m.group(1)
        angle = float(m.group(2))
        results.append((axis, angle))
    # explicit rotate/rotatesample/spin with number
    for m in re.finditer(r'\b(?:rotate|rotatesample|sspin|spin)\b[^\d\-]*(-?\d+\.?\d*)', s_low):
        angle = float(m.group(1))
        # axis unknown -> use 'phi' as generic if present
        axis = 'phi' if 'phi' in s_low else 'unknown'
        results.append((axis, angle))
    # patterns like "phi 360"
    for m in re.finditer(r'\b(phi|or0|or1|setor0|setor1|t|temperature|temp)\b[^\d\-]{0,8}(-?\d+\.?\d*)', s_low):
        axis = m.group(1)
        angle = float(m.group(2))
        results.append((axis, angle))
    # If nothing found but words indicate spin without numbers, record axisless spin
    if not results and ('spin' in s_low or 'rotate' in s_low or 'rotat' in s_low):
        results.append(('unknown', None))
    return results

def extract_temperature_target(text):
    """
    Find a temperature target (integer) in the text near settemp, umv T, or epics_put.
    Returns int or None
    """
    if text is None:
        return None
    s = lower(text)
    # direct patterns
    m = re.search(r'\bsettemp\b[^\d\-]*(\d{2,4})', s)
    if m:
        return int(m.group(1))
    m = re.search(r'\bumv\s+t\b[^\d\-]*(\d{2,4})', s)
    if m:
        return int(m.group(1))
    # epics_put("IOC:TEMP:Setpoint", 220) or similar
    m = re.search(r'epics_put\([^\d\-]*(\d{2,4})', s)
    if m:
        return int(m.group(1))
    # fallback: any 3-digit-ish number near keyword "temp" or "temperature"
    if 'temp' in s or 'temperature' in s:
        ints = find_integers(s)
        for i in ints:
            if 10 < i < 1000:
                return i
    return None

# ---------- semantic comparison ----------
def score_rotate_semantic(ref_text, hyp_text):
    """
    Returns a semantic score in [0,1] for rotate/spin tasks.
    Components:
      - loop count match (1 or 0)
      - angle equivalence (1 exact / 0.5 partial / 0)
      - axis match (1 or 0.5 if unknown/compatible)
    Returns dict with components and final score.
    """
    # extract
    ref_count = extract_loop_count(ref_text)
    hyp_count = extract_loop_count(hyp_text)

    ref_angles = extract_rotation_angles_and_axes(ref_text)
    hyp_angles = extract_rotation_angles_and_axes(hyp_text)

    # loop match
    loop_match = 0.0
    if ref_count is None and hyp_count is None:
        loop_match = 0.5  # both unspecified -> partial credit
    elif ref_count is not None and hyp_count is not None:
        loop_match = 1.0 if ref_count == hyp_count else 0.0
    elif ref_count is None and hyp_count is not None:
        loop_match = 0.5
    else:
        loop_match = 0.5

    # angle equivalence:
    # Strategy: compute typical "rotation per iteration" for ref and hyp.
    # - if ref has an angle 360 and loop count N -> rotation per iteration = 360
    # - if hyp uses inc angle (e.g., 36) with loop count 10 -> 36*10 == 360 (equivalent)
    def estimate_rotation_per_iteration(angles, loop_count):
        """
        angles: list of (axis, angle). angle may be None.
        loop_count: int or None
        Return estimated degrees-per-iteration (float) or None if unknown.
        """
        if not angles:
            return None
        # if angles contains an explicit 360 or similar, assume that's degrees per iteration
        # if multiple angles, take sum of absolute numeric angles ignoring None
        nums = [abs(a) for (_, a) in angles if a is not None]
        if not nums:
            return None
        # if loop_count present and there are small increment values, maybe total rotation = increment * loop_count
        if loop_count and len(nums) == 1:
            # if angle small (<90) and loop_count > 1, infer increments probably applied each iteration: total = angle * loop_count
            if nums[0] <= 90 and loop_count > 1:
                return nums[0] * loop_count
        # otherwise, use the max or sum as heuristic
        s = sum(nums)
        return s if s > 0 else None

    ref_rot = estimate_rotation_per_iteration(ref_angles, ref_count)
    hyp_rot = estimate_rotation_per_iteration(hyp_angles, hyp_count)

    angle_score = 0.0
    if ref_rot is None and hyp_rot is None:
        angle_score = 0.5
    elif ref_rot is not None and hyp_rot is not None:
        # treat equal within 5% as exact
        if abs(ref_rot - hyp_rot) <= max(1.0, 0.05 * abs(ref_rot)):
            angle_score = 1.0
        else:
            # partial credit proportional to closeness (cap at 1)
            ratio = min(ref_rot, hyp_rot) / max(ref_rot, hyp_rot)
            angle_score = ratio
    else:
        angle_score = 0.0

    # axis match: compare axis names if present
    def get_axes(angles):
        return {a for (a, v) in angles if a is not None}
    ref_axes = get_axes(ref_angles)
    hyp_axes = get_axes(hyp_angles)
    axis_score = 0.0
    if not ref_axes and not hyp_axes:
        axis_score = 0.5
    elif ref_axes & hyp_axes:
        axis_score = 1.0
    else:
        # consider phi vs or0 as possibly equivalent if both mention or/phi synonyms
        synonyms = [{'phi','or0','or1','setor0','setor1'}, {'t','temperature','temp'}]
        matched = 0
        for group in synonyms:
            if ref_axes & group and hyp_axes & group:
                matched = 1
                break
        axis_score = 1.0 if matched else 0.0

    # combine
    # weights: loop 0.35, angle 0.45, axis 0.2
    final = 0.35 * loop_match + 0.45 * angle_score + 0.20 * axis_score
    return {
        "loop_match": loop_match,
        "angle_score": angle_score,
        "axis_score": axis_score,
        "semantic_score": final,
        "ref_rot_est": ref_rot,
        "hyp_rot_est": hyp_rot,
        "ref_count": ref_count,
        "hyp_count": hyp_count,
        "ref_angles": ref_angles,
        "hyp_angles": hyp_angles
    }

def score_temp_semantic(ref_text, hyp_text):
    ref_temp = extract_temperature_target(ref_text)
    hyp_temp = extract_temperature_target(hyp_text)
    score = 0.0
    if ref_temp is None and hyp_temp is None:
        score = 0.5
    elif ref_temp is not None and hyp_temp is not None:
        score = 1.0 if ref_temp == hyp_temp else 0.0
    else:
        score = 0.0
    return {"ref_temp": ref_temp, "hyp_temp": hyp_temp, "semantic_score": score}

# ---------- top-level scoring for one pair ----------
def semantic_score_pair(ref_text, hyp_text, user_query=None):
    """
    Returns a dict containing:
      - task_type: 'rotate' | 'temperature' | 'unknown'
      - semantic_score: 0..1
      - breakdown fields depending on task
    """
    # decide task type from reference first, else user_query, else hypothesis
    sources = [ref_text, user_query, hyp_text]
    joined = " ".join([lower(s) for s in sources if s])
    if 'temp' in joined or 'settemp' in joined or 'temperature' in joined or 'epics' in joined:
        task = 'temperature'
    elif 'spin' in joined or 'rotate' in joined or 'rotat' in joined or 'sspin' in joined:
        task = 'rotate'
    else:
        task = 'unknown'

    out = {"task": task}

    if task == 'rotate':
        res = score_rotate_semantic(ref_text, hyp_text)
        out.update(res)
    elif task == 'temperature':
        res = score_temp_semantic(ref_text, hyp_text)
        out.update(res)
    else:
        # fallback: give a weak lexical similarity signal (fraction of tokens overlap)
        ref_tokens = set(re.findall(r'\w+', lower(ref_text)))
        hyp_tokens = set(re.findall(r'\w+', lower(hyp_text)))
        if not ref_tokens or not hyp_tokens:
            out["semantic_score"] = 0.0
        else:
            inter = len(ref_tokens & hyp_tokens)
            union = len(ref_tokens | hyp_tokens)
            out["semantic_score"] = inter / max(1, union)
        out["task"] = "unknown"
    return out

# ---------- Dataframe scoring utilities ----------
def score_dataframe_semantic(df,
                             ref_col='Original Answer',
                             model_cols=None,
                             input_col='User Query',
                             out_dir=None):
    if model_cols is None:
        # detect likely model columns heuristically
        model_cols = [c for c in df.columns if any(k in c.lower() for k in ['llama','codellama','mistral','deepseek','output','prediction']) and 'latency' not in c.lower()]
    # latency columns
    latency_cols = [c for c in df.columns if 'latency' in c.lower()]

    rows = []
    per_model = {m: [] for m in model_cols}

    for idx, row in df.iterrows():
        ref = row.get(ref_col, "")
        user_q = row.get(input_col, "")
        for m in model_cols:
            hyp = row.get(m, "")
            res = semantic_score_pair(ref, hyp, user_query=user_q)
            rec = {
                "index": idx,
                "model": m,
                "user_query": user_q,
                "hypothesis": hyp,
                "reference": ref,
                "task": res.get("task"),
                "semantic_score": res.get("semantic_score")
            }
            # include breakdown fields
            for k, v in res.items():
                if k not in rec:
                    rec[k] = v
            # attach latency if available
            lat = None
            for lc in latency_cols:
                if m.lower().replace(' ','') in lc.lower().replace(' ',''):
                    try:
                        lat = float(row.get(lc, math.nan))
                    except:
                        lat = math.nan
                    break
            rec['latency_ms'] = lat
            rows.append(rec)
            per_model[m].append(rec)

    out_df = pd.DataFrame(rows)
    # summary per model: average semantic_score and avg latency
    summary = []
    for m, recs in per_model.items():
        if not recs:
            continue
        d = pd.DataFrame(recs)
        summary.append({
            "model": m,
            "mean_semantic_score": float(d['semantic_score'].mean()),
            "median_semantic_score": float(d['semantic_score'].median()),
            "avg_latency_ms": float(d['latency_ms'].dropna().mean()) if 'latency_ms' in d.columns and not d['latency_ms'].dropna().empty else None,
            "n_examples": len(d)
        })
    summary_df = pd.DataFrame(summary).set_index('model') if summary else pd.DataFrame()
    # optionally save
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        per_path = os.path.join(out_dir, "per_example_semantic_scores.csv")
        sum_path = os.path.join(out_dir, "semantic_summary_by_model.csv")
        out_df.to_csv(per_path, index=False)
        summary_df.to_csv(sum_path)
        print("Wrote:", per_path)
        print("Wrote:", sum_path)
    return out_df, summary_df

# ---------- script entrypoint ----------
if __name__ == "__main__":
    # Edit these paths if needed
    INPUT_PATH = "/home/vallurs/research/data/scoring/master_table.csv"
    OUT_DIR = "/home/vallurs/research/data/scoring/semantic_scores"

    print("Reading:", INPUT_PATH)
    df = pd.read_csv(INPUT_PATH)

    # specify the exact model output columns present in your file
    model_cols = [
        "Llama3 Output",
        "CodeLlama Output",
        "Mistral Output",
        "Deepseek-1.5 Output"
    ]

    out_df, summary_df = score_dataframe_semantic(
        df,
        ref_col="Original Answer",
        model_cols=model_cols,
        input_col="User Query",
        out_dir=OUT_DIR
    )

    print("\nSummary (semantic):")
    print(summary_df)
    print("\nDone.")
