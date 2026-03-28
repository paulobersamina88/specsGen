from typing import Dict
import pandas as pd
from utils.text_utils import normalize_text

COLUMN_ALIASES = {
    "item_no": ["item no", "item number", "pay item", "item", "payitem", "no."],
    "description": ["description", "item description", "scope", "work description", "particulars"],
    "unit": ["unit", "uom"],
    "quantity": ["qty", "quantity", "qnty"],
    "remarks": ["remarks", "comment", "notes"],
    "division": ["division", "trade", "discipline", "category"],
}

def find_column(df: pd.DataFrame, aliases):
    cols = {normalize_text(c): c for c in df.columns}
    for alias in aliases:
        if alias in cols:
            return cols[alias]
    for key, original in cols.items():
        if any(alias in key for alias in aliases):
            return original
    return ""

def auto_map_columns(df: pd.DataFrame) -> Dict[str, str]:
    return {key: find_column(df, aliases) for key, aliases in COLUMN_ALIASES.items()}

def standardize_boq(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    result = pd.DataFrame()
    for key in COLUMN_ALIASES:
        src = mapping.get(key, "")
        result[key] = df[src] if src else ""
    result = result.fillna("")
    result = result[result["description"].astype(str).str.strip() != ""].copy()
    result["row_id"] = range(1, len(result) + 1)
    return result[["row_id", "item_no", "description", "unit", "quantity", "remarks", "division"]]
