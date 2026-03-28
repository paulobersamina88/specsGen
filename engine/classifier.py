from typing import Dict, Tuple
from utils.text_utils import apply_synonyms

TRADE_RULES = {
    "Earthworks": ["excavation", "backfill", "embankment", "subgrade", "grading", "fill material", "compaction"],
    "Concrete Works": ["structural concrete", "concrete", "formworks", "slab", "beam", "column", "footing"],
    "Reinforcement": ["rebar", "reinforcing steel", "deformed bar", "tie wire"],
    "Masonry": ["chb", "masonry", "blockwork", "concrete hollow block"],
    "Architectural Finishes": ["plaster", "painting", "tile", "ceiling", "partition", "doors", "windows", "hardware"],
    "Roofing": ["roof", "roofing", "longspan", "gutter", "downspout", "flashing", "ridge roll"],
    "Plumbing / Sanitary": ["plumbing", "sanitary", "waterline", "sewer", "storm drain", "ppr", "u-pvc", "cleanout", "fixture"],
    "Mechanical": ["air conditioning", "hvac", "ventilation", "duct", "air handling", "exhaust", "refrigerant"],
    "Electrical": ["electrical", "wire", "cable", "conduit", "panel", "lighting", "fdas", "cctv", "data", "network", "grounding"],
    "Site Development": ["curb", "gutter", "fence", "pavement", "sidewalk", "drainage", "riprap", "canal"],
}

def classify_trade(description: str, synonyms: Dict[str, list]) -> Tuple[str, int]:
    text = apply_synonyms(description, synonyms)
    best_trade, best_score = "Unclassified", 0
    for trade, keywords in TRADE_RULES.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > best_score:
            best_trade, best_score = trade, score
    return best_trade, best_score
