from typing import Dict, List, Optional
from utils.text_utils import normalize_text


def score_record(text: str, record: Dict) -> int:
    text = normalize_text(text)
    score = 0
    for kw in record.get("keywords", []):
        if normalize_text(kw) in text:
            score += 3
    for trade in [record.get("trade", "")]:
        if trade and normalize_text(trade) in text:
            score += 1
    return score


def match_library(text: str, records: List[Dict]) -> Optional[Dict]:
    best = None
    best_score = 0
    for rec in records:
        score = score_record(text, rec)
        if score > best_score:
            best = rec
            best_score = score
    if best:
        best = {**best, "_score": best_score}
    return best


def match_item(description: str, trade: str, libraries: Dict) -> Dict:
    query = f"{description} {trade}"
    dpwh = match_library(query, libraries["dpwh"])
    office = match_library(query, libraries["office"])
    ufgs = match_library(query, libraries["ufgs"])

    if dpwh and dpwh["_score"] >= 3:
        return {
            "primary_source": "DPWH",
            "record": dpwh,
            "secondary_source": "OFFICE" if office and office["_score"] >= 3 else ("UFGS" if ufgs and ufgs["_score"] >= 3 else ""),
            "confidence": "High" if dpwh["_score"] >= 6 else "Medium",
            "fallback_used": False,
        }
    if office and office["_score"] >= 3:
        return {
            "primary_source": "OFFICE",
            "record": office,
            "secondary_source": "UFGS" if ufgs and ufgs["_score"] >= 3 else "",
            "confidence": "Medium",
            "fallback_used": False,
        }
    if ufgs and ufgs["_score"] >= 3:
        return {
            "primary_source": "UFGS",
            "record": ufgs,
            "secondary_source": "",
            "confidence": "Medium",
            "fallback_used": True,
        }
    return {
        "primary_source": "GENERIC",
        "record": None,
        "secondary_source": "",
        "confidence": "Low",
        "fallback_used": True,
    }
