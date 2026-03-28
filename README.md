# TechSpec PRO

A Streamlit starter app that converts uploaded BOQ items into draft technical specifications for Philippine projects using a DPWH-first and UFGS-fallback architecture.

## Features
- Upload CSV/XLSX BOQ files
- Map BOQ columns
- Classify BOQ items by trade
- Match against DPWH seed library first
- Fall back to UFGS seed library when needed
- Generate editable draft technical specifications
- Flag low-confidence items for manual review
- Export spec register CSV and compiled DOCX

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Recommended next steps
1. Expand `data/dpwh_library_seed.json`
2. Expand `data/ufgs_fallback_seed.json`
3. Add your office special provisions in `data/office_special_provisions_seed.json`
4. Tune the synonym dictionary
5. Add actual PDF ingestion later for your curated standards

## Important
This package generates draft technical specifications only. Final output must still be reviewed against the latest approved DPWH references, project drawings, special provisions, and applicable Philippine codes.
