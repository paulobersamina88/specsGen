from typing import Dict, List
import pandas as pd

from engine.classifier import classify_trade
from engine.matcher import match_item, match_library
from engine.clause_builder import generic_record, merge_records
from engine.generator import render_spec_text
from engine.qa_checker import review_flags

def build_spec_register(
    boq_df: pd.DataFrame,
    libraries: Dict,
    project_meta: Dict,
    source_priority: List[str],
    append_office_clauses: bool = True,
) -> pd.DataFrame:
    rows = []
    for _, row in boq_df.iterrows():
        trade, trade_score = classify_trade(str(row["description"]), libraries["synonyms"])
        match = match_item(str(row["description"]), trade, libraries, source_priority)
        primary_record = match["record"] or generic_record(trade)

        secondary_record = None
        office_record = None

        if match["secondary_source"] == "UFGS":
            secondary_record = match_library(str(row["description"]), libraries["ufgs"], trade)
        elif match["secondary_source"] == "OFFICE":
            secondary_record = match_library(str(row["description"]), libraries["office"], trade)

        if append_office_clauses:
            office_record = match_library(f"{row['description']} {trade}", libraries["office"], trade)

        merged = merge_records(primary_record, secondary_record=secondary_record, office_record=office_record)
        flags = review_flags(
            primary_source=match["primary_source"],
            confidence=match["confidence"],
            spec_record=merged,
            description=str(row["description"]),
        )
        generated_spec = render_spec_text(
            project_meta=project_meta,
            row=row.to_dict(),
            spec=merged,
            primary_source=match["primary_source"],
            secondary_source=match["secondary_source"],
            flags=flags,
        )
        rows.append({
            **row.to_dict(),
            "trade": trade,
            "trade_score": trade_score,
            "primary_source": match["primary_source"],
            "secondary_source": match["secondary_source"],
            "confidence": match["confidence"],
            "fallback_used": match["fallback_used"],
            "candidate_scores": match["candidates"],
            "matched_section_id": merged.get("id", ""),
            "matched_section_title": merged.get("title", ""),
            "review_flags": " | ".join(flags),
            "generated_spec": generated_spec,
        })
    return pd.DataFrame(rows)
