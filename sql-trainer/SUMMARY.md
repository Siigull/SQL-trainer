# SQL Trainer Summary

## Files
- `index.html` — standalone web app (loads sql.js from CDN)
- `validate.py` — runs all 55 executable hint SQLs against their datasets
- `validate_consistency.py` — 34 FK/semantic/data-integrity checks
- `review_report.md` — external review findings and resolutions
- `analyze_theory.py` — keyword signatures for theory/DDL questions

## Datasets (6, reused across 55 executable + 8 theory questions)
1. **Banka** — klient, pobocka, ucet, transakce (18 questions)
2. **Obchod** — zakaznik, zbozi, koupil (8 questions)
3. **Univerzita** — student, predmet, zapsal (8 questions)
4. **Firma** — zamestnanec, oddeleni (6 questions)
5. **Servis** — mechanik, auto, oprava (7 questions)
6. **Dodavatele** — dodavatel, zbozi, dodava (8 questions)

## Validation Results
- **55/55** executable queries execute without error on SQLite
- **34/34** consistency checks pass (FK integrity, expected cardinalities)
- JS syntax validated via Node.js parser
- HTML tag balance validated via Python HTMLParser
- Oracle-specific syntax (`ALL` quantified comparisons) rewritten to SQLite-compatible equivalents while preserving pedagogical intent
- Duplicate column name JS rendering bug fixed with auto-suffix deduplication
- Row-order checker made order-agnostic via canonical sorting
- DML/DDL detection added to prevent false-positive "Correct!" on non-SELECT statements
- Deterministic `ORDER BY` tie-breaks added to `LIMIT 1` questions
- **Keyword-based validation** for theory/DDL questions: checks student's answer against required keywords (e.g., `CURSOR`, `OPEN`, `FETCH`, `CLOSE`) before showing the reference answer

## How to use
Open `index.html` in a browser (or serve via `python -m http.server`).
