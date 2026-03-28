# TechSpec PRO Version 2

A more comprehensive Streamlit package for converting uploaded BOQ items into draft technical specifications for Philippine projects using a **DPWH-first**, **office-special-provisions-second**, and **UFGS-fallback** architecture.

## What's new in Version 2
- Multipage Streamlit workflow
- More structured standards library
- Better trade classification and synonym handling
- User-controlled source priority
- Manual override of matched section per BOQ item
- Project special provisions appender
- Spec register with confidence, review flags, and source traceability
- CSV, XLSX, TXT, and DOCX export
- Seed libraries expanded across civil, structural, architectural, plumbing, mechanical, and electrical scopes

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Recommended use
1. Start with `data/sample_boq_v2.xlsx` or upload your own BOQ.
2. Review the section library in the Standards Library page.
3. Generate draft technical specs.
4. Check fallback items carefully, especially UFGS-based matches.
5. Revise clauses before issuing final project specifications.

## Important
This package creates **draft** technical specifications only.
Final specifications must still be checked against:
- latest approved DPWH references and issuances
- project plans and details
- special provisions
- NSCP / PEC / Plumbing Code / Fire Code / NBCP as applicable
- agency-approved procurement and contract documents
