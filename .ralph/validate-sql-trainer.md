# Validate SQL Trainer Dataset

Thoroughly validate every (question, dataset, hint sql, expected output) tuple in the SQL trainer.

## Goals
- Ensure every hint SQL executes without errors on its dataset using SQLite
- Ensure result sets match semantic expectations (non-empty where expected, correct columns)
- Ensure dataset schemas and data are consistent
- Ensure no Oracle-only syntax slips into executable questions (ALL/ANY/SOME/ROWNUM/TO_DATE etc.) unless covered by SQLite equivalent
- Fix any discrepancies in `sql-trainer/index.html`

## Checklist
- [x] Write automated validation script (Python + sqlite3) — `validate.py`
- [x] Run all 55 executable questions through validator — **55/55 PASS**
- [x] Fix syntax errors (ALL/ANY → MAX/MIN subqueries, type mismatches)
- [x] Fix data inconsistencies (added orphan customer + subject, added Jana Mala account for b14, changed Cyril repair type for s6)
- [x] Fix schema mismatches (firma notNull display)
- [x] Fix JS bugs (duplicate column names, row-order sensitivity in checker, DML detection)
- [x] Add deterministic ORDER BY to LIMIT 1 questions with ties (u6, s1)
- [x] Harden b13 against NULL branches
- [x] Write consistency validator — `validate_consistency.py`
- [x] Run 34 FK/semantic checks — **34/34 PASS**
- [x] Validate JS syntax via Node.js parser — OK
- [x] Validate HTML tag balance — OK
- [x] Delegate subagent review (`reviewer`) and address all findings
- [x] Re-run validators after all fixes — **100% pass**
- [x] Ensure web app HTML is syntactically valid

## Verification
- `sql-trainer/validate.py`: **55/55 PASS**
- `sql-trainer/validate_consistency.py`: **34/34 PASS**
- `node --check` on extracted JS: **OK**
- Python HTMLParser tag balance: **OK**
- `reviewer` subagent report: all findings addressed

## Files delivered
- `sql-trainer/index.html` — standalone web app (55 executable + 8 theory questions)
- `sql-trainer/validate.py` — executes all hint SQLs, reports pass/fail
- `sql-trainer/validate_consistency.py` — FK & semantic data-integrity checks
- `sql-trainer/SUMMARY.md` — project overview
- `sql-trainer/review_report.md` — external review findings

## Notes
- SQLite does NOT support `> ALL (subquery)`. Replaced with `> (SELECT MAX(...) FROM subquery)`.
- Oracle-specific features (triggers, cursors, materialized views) covered as non-executable theory questions.
- ResultsEqual now sorts rows canonically before comparison, so row order does not matter.
