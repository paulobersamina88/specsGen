import json
from utils.config import DATA_DIR


def load_json(name: str):
    path = DATA_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_libraries():
    return {
        "dpwh": load_json("dpwh_library_seed.json"),
        "ufgs": load_json("ufgs_fallback_seed.json"),
        "office": load_json("office_special_provisions_seed.json"),
        "synonyms": load_json("synonym_dictionary.json"),
    }
