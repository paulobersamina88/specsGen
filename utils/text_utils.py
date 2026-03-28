import re
from typing import Iterable


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def contains_any(text: str, keywords: Iterable[str]) -> int:
    text = normalize_text(text)
    return sum(1 for kw in keywords if normalize_text(kw) in text)
