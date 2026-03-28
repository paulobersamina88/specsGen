from dataclasses import dataclass
from typing import Dict
import pandas as pd

COLUMN_ALIASES = {
    "item_no": ["item no", "item number", "pay item", "item", "payitem", "item_no"],
    "description": ["description", "item description", "scope", "work description", "particulars"],
    "unit": ["unit", "uom"],
    "quantity": ["qty", "quantity", "qnty"],
    "remarks": ["remarks", "notes", "comment"],
}


@dataclass
class ParsedBOQ:
    df: pd.DataFrame
    column_map: Dict[str, str]


def _normalize_col(text: str) -> str:
    return " ".join(str(text).strip().lower().split())


def auto_map_columns(df: pd.DataFrame) -> Dict[str, str]:
    normalized = {_normalize_col(c): c for c in df.columns}
    result = {}
    for key, aliases in COLUMN_ALIASES.items():
        chosen = ""
        for alias in aliases:
            if alias in normalized:
                chosen = normalized[alias]
                break
        if not chosen:
            for ncol, orig in normalized.items():
                if any(alias in ncol for alias in aliases):
                    chosen = orig
                    break
        result[key] = chosen
    return result


def standardize_boq(df: pd.DataFrame, column_map: Dict[str, str]) -> pd.DataFrame:
    out = pd.DataFrame()
    for key in ["item_no", "description", "unit", "quantity", "remarks"]:
        col = column_map.get(key, "")
        out[key] = df[col] if col and col in df.columns else ""
    out = out.fillna("")
    out = out[out["description"].astype(str).str.strip() != ""].copy()
    return out.reset_index(drop=True)
