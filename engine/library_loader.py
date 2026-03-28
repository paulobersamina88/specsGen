import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

def _load_json(name: str):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)

def load_libraries():
    return {
        "dpwh": _load_json("dpwh_library_v2.json"),
        "office": _load_json("office_special_provisions_v2.json"),
        "ufgs": _load_json("ufgs_fallback_v2.json"),
        "synonyms": _load_json("synonym_dictionary_v2.json"),
    }
