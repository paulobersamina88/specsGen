from typing import Dict, Tuple
from utils.text_utils import normalize_text


def apply_synonyms(text: str, synonyms: Dict[str, list]) -> str:
    text_n = normalize_text(text)
    additions = []
    for canonical, variants in synonyms.items():
        if canonical in text_n:
            additions.append(canonical)
            continue
        for v in variants:
            if normalize_text(v) in text_n:
                additions.append(canonical)
                break
    if additions:
        return text_n + " " + " ".join(additions)
    return text_n


def classify_trade(description: str, synonyms: Dict[str, list]) -> Tuple[str, int]:
    text = apply_synonyms(description, synonyms)
    trade_rules = {
        "Earthworks": ["excavation", "backfill", "embankment", "earthwork", "grading"],
        "Structural": ["concrete", "rebar", "reinforcing steel", "footing", "beam", "column", "slab"],
        "Masonry": ["chb", "masonry", "blockwork", "concrete hollow block"],
        "Finishes": ["plaster", "painting", "tile", "ceiling", "partition"],
        "Roofing": ["roof", "roofing", "longspan", "gutter", "downspout"],
        "Plumbing/Sanitary": ["plumbing", "sanitary", "waterline", "sewer", "storm drain", "ppr", "u-pvc"],
        "Mechanical": ["air conditioning", "hvac", "ventilation", "duct", "mechanical"],
        "Electrical": ["electrical", "wire", "cable", "conduit", "panel", "lighting", "fdas", "cctv", "data", "network"],
    }
    best_trade = "Unclassified"
    best_score = 0
    for trade, keywords in trade_rules.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_trade = trade
            best_score = score
    return best_trade, best_score
