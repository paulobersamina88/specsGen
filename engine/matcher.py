from typing import Dict, List, Optional
from utils.text_utils import normalize_text, apply_synonyms

def _score_record(text: str, record: Dict) -> int:
    score = 0
    text_n = normalize_text(text)
    for kw in record.get("keywords", []):
        if normalize_text(kw) in text_n:
            score += 4
    for phrase in record.get("preferred_phrases", []):
        if normalize_text(phrase) in text_n:
            score += 6
    trade = record.get("trade", "")
    if trade and normalize_text(trade) in text_n:
        score += 2
    for bad in record.get("negative_keywords", []):
        if normalize_text(bad) in text_n:
            score -= 4
    return score

def match_library(text: str, records: List[Dict], trade: str = "") -> Optional[Dict]:
    query = f"{text} {trade}".strip()
    best = None
    best_score = 0
    for rec in records:
        score = _score_record(query, rec)
        if score > best_score:
            best = rec
            best_score = score
    if not best:
        return None
    enriched = {**best, "_score": best_score}
    return enriched

def _confidence(score: int) -> str:
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"

def match_item(description: str, trade: str, libraries: Dict, source_priority: List[str]) -> Dict:
    text = apply_synonyms(description, libraries["synonyms"])
    candidates = {
        "DPWH": match_library(text, libraries["dpwh"], trade),
        "OFFICE": match_library(text, libraries["office"], trade),
        "UFGS": match_library(text, libraries["ufgs"], trade),
    }

    primary_source = "GENERIC"
    primary_record = None
    secondary_source = ""
    ranked = []

    for source in source_priority:
        if source == "GENERIC":
            continue
        rec = candidates.get(source)
        if rec and rec["_score"] >= 4:
            ranked.append((source, rec["_score"], rec))

    ranked.sort(key=lambda x: (-x[1], source_priority.index(x[0])))

    if ranked:
        primary_source, _, primary_record = ranked[0]
        if len(ranked) > 1:
            secondary_source = ranked[1][0]

    return {
        "primary_source": primary_source,
        "record": primary_record,
        "secondary_source": secondary_source,
        "confidence": _confidence(primary_record["_score"]) if primary_record else "Low",
        "fallback_used": primary_source in {"UFGS", "GENERIC"},
        "candidates": {k: (v["_score"] if v else 0) for k, v in candidates.items()},
    }
