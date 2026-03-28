import re
from typing import Dict, Iterable, List

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())

def contains_phrase(text: str, phrase: str) -> bool:
    return normalize_text(phrase) in normalize_text(text)

def apply_synonyms(text: str, synonyms: Dict[str, List[str]]) -> str:
    text_n = normalize_text(text)
    additions = []
    for canonical, variants in synonyms.items():
        canonical_n = normalize_text(canonical)
        if canonical_n in text_n:
            additions.append(canonical_n)
            continue
        for variant in variants:
            if normalize_text(variant) in text_n:
                additions.append(canonical_n)
                break
    if additions:
        return f"{text_n} " + " ".join(sorted(set(additions)))
    return text_n

def dedupe_keep_order(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        item_n = item.strip()
        if item_n and item_n not in seen:
            seen.add(item_n)
            result.append(item_n)
    return result
