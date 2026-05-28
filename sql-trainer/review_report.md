# SQL Trainer Review Report

**Date:** 2026-05-27  
**Files reviewed:**
- `sql-trainer/index.html`
- `sql-trainer/validate.py`
- `sql-trainer/validate_consistency.py`

**Summary:**
- All datasets are **syntactically consistent** across the three files.
- `validate.py` executes **55 / 55** hint queries without error.
- `validate_consistency.py` passes **32 / 32** integrity and semantic checks.
- Foreign keys are clean and data is logically coherent.

However, a few **determinism**, **pedagogical**, and **checker-robustness** issues were found. The most impactful is that the `resultsEqual()` function in `index.html` compares row order exactly, while many hint queries lack deterministic `ORDER BY` clauses. This means a student can write a perfectly correct query and still be marked wrong because SQLite returned rows in a different order.

---

## 1. Blockers (must fix before exam)

### 1.1 `u6` — Non-deterministic LIMIT 1 (3-way tie)

- **Question:** *Město s nejvíce studenty* (`u6`)
- **Hint:**
  ```sql
  SELECT s.mesto, COUNT(DISTINCT s.cisloS) AS pocet
  FROM student s JOIN zapsal z ON s.cisloS = z.cisloS
  WHERE z.ak_rok = 2021
  GROUP BY s.mesto
  ORDER BY pocet DESC LIMIT 1
  ```
- **Problem:** Brno, Bratislava and Praha each have exactly **2** enrolled students. `ORDER BY pocet DESC LIMIT 1` returns an arbitrary city depending on SQLite’s internal group-order (in Python we got *Praha*, on another run it could be *Brno*).
- **Impact:** The expected result is unstable. A student writing the exact same query may see a different city in the "Expected Result" panel on a fresh page load, and a correct student query might mismatch.
- **Fix:** Add a deterministic tie-break and optionally mention it in the assignment text.
  ```sql
  SELECT s.mesto, COUNT(DISTINCT s.cisloS) AS pocet
  FROM student s JOIN zapsal z ON s.cisloS = z.cisloS
  WHERE z.ak_rok = 2021
  GROUP BY s.mesto
  ORDER BY pocet DESC, s.mesto ASC
  LIMIT 1
  ```
  **Files to update:** `index.html` (question object for `u6`) and `validate.py`.

---

### 1.2 `s1` — Non-deterministic LIMIT 1 (3-way tie)

- **Question:** *Mechanik s nejvíce auty* (`s1`)
- **Hint:**
  ```sql
  SELECT m.cisloM, m.meno, COUNT(DISTINCT o.spz) AS pocet_aut
  FROM mechanik m JOIN oprava o ON m.cisloM = o.cisloM
  GROUP BY m.cisloM, m.meno
  ORDER BY pocet_aut DESC LIMIT 1
  ```
- **Problem:** Adam, Betka and Cyril each repair **3** distinct cars. SQLite returns one of them arbitrarily (in the test run it returned *Cyril*).
- **Impact:** Same as above—unstable expected result.
- **Fix:** Add a secondary sort.
  ```sql
  … ORDER BY pocet_aut DESC, m.cisloM ASC LIMIT 1
  ```
  **Files to update:** `index.html` and `validate.py`.

---

### 1.3 Row-order sensitivity in `resultsEqual()`

- **Location:** `index.html` → `resultsEqual(a, b)`
- **Problem:** The equality checker iterates rows **in their returned order**. If a student produces the correct rows but in a different order than the hint, the app does **not** show the green “Correct!” banner. This is especially confusing for questions whose assignment text does **not** ask for a specific order.
- **Affected questions (non-exhaustive):** `b6`, `b8`, `b10`, `b11`, `b12`, `b13`, `b15`, `b16`, `o1`, `o5`, `o8`, `u1`, `u3`, `u4`, `u8`, `f1`, `f4`, `f5`, `s2`, `s3`, `s5`, `s7`, `d6`, `d8`, and many others.
- **Fix options (choose one):**
  1. **Quick fix:** Add an explicit `ORDER BY` to **every** hint query that returns >1 row and update the assignment text to say “Sort the results by X”. This is the safest short-term fix.
  2. **Robust fix:** Make `resultsEqual` order-agnostic by sorting both result sets by a canonical JSON representation before comparison. Example patch:
     ```js
     function canonicalSort(rows) {
       return [...rows].sort((a,b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
     }
     // inside resultsEqual:
     const aSorted = canonicalSort(a);
     const bSorted = canonicalSort(b);
     // then compare aSorted[i] with bSorted[i]
     ```
  **Recommendation:** Apply option 1 to the most obvious queries (all `SELECT *` or `GROUP BY` without `ORDER BY`) and schedule option 2 as a future enhancement.

---

## 2. Pedagogical/Data Issues

### 2.1 Empty result sets for concepts not specifically testing emptiness

| Question | Current rows | Why it is empty |
|----------|--------------|-----------------|
| **b14** | 0 | The only non-Brno client (`Jana Mala`) has **no account**, so the `HAVING` clause is never evaluated. |
| **u7**  | 0 | No student is enrolled in all 7 subjects. |
| **s4**  | 0 | No car brand is repaired **exclusively** by Adam (Ford is also repaired by Cyril). |
| **s6**  | 0 | No mechanic performed all three repair types (`brzdy`, `vymena`, `oprava`). |

- **Impact:** When a student runs their query and sees *“No rows.”* they often assume they made a mistake. It is valid to test empty results for concepts like `NOT EXISTS`, but having **four** such cases is excessive for an exam-level trainer.
- **Suggestion (one of the following per question):**
  1. **b14:** Give `Jana Mala` an account (e.g. 9999999, 90000, `625622/6249`, `'Palackeho'`) so her total balance (90 000) exceeds every Brno client’s total (max Brno total = 80 000 for Josef Moudry). This will shift `b10`, `b11`, `b12` slightly, but all those questions are robust to the change.
  2. **u7:** Add a few enrollments so that **student 1** (`Pavel` from Brno) ends up in all 7 subjects. Then `u7` returns 1 row. Side effects: `u1` (kredit count) and `u4` (top student) need to be rechecked. Alternatively, leave `u7` as-is if the learning goal is explicitly to produce an empty set with double `NOT EXISTS`.
  3. **s4:** Remove Cyril’s repair on `spz = 123` (Ford) so Ford is **only** repaired by Adam. Then `s4` returns `'Ford'` (1 row). Side effects: `s2` sum for Ford drops from 109 500 → 100 000 (still > 50 000), `s3` Ford average changes slightly, `s1` tie becomes Adam & Betka (still needs the tie-break fix from blocker 1.2).
  4. **s6:** Change one repair for a mechanic so that they cover all three types. For example, change Cyril’s repair on `spz = 123` from `oprava` to `vymena`. Then Cyril has `oprava` (555), `brzdy` (777), `vymena` (123) → 3 types, and `s6` returns 1 row. Side effect: `s4` remains empty unless the Ford-only fix above is also applied.

---

### 2.2 `b14` — overly complex hint for the level

- **Hint:** Uses a doubly-nested subquery (`SELECT MAX(...) FROM (SELECT SUM(...) ... )`) to simulate `> ALL (...)`.
- **Note:** While mathematically correct, the sheer length makes it hard to read. Simpler, equivalent form:
  ```sql
  SELECT k.jmeno, k.r_cislo, k.mesto, SUM(u.stav) AS celkem
  FROM klient k JOIN ucet u ON k.r_cislo = u.r_cislo
  WHERE k.mesto <> 'Brno'
  GROUP BY k.jmeno, k.r_cislo, k.mesto
  HAVING SUM(u.stav) > (
      SELECT MAX(t.total)
      FROM (
          SELECT SUM(u2.stav) AS total
          FROM klient k2 JOIN ucet u2 ON k2.r_cislo = u2.r_cislo
          WHERE k2.mesto = 'Brno'
          GROUP BY k2.r_cislo
      ) t
  )
  ```
- **Verdict:** Acceptable, but consider shortening the alias names (`brno_totals` → `t`) in the final hint.

---

### 2.3 `o2` — wording ambiguity on “po roce 2000”

- **Text:** *“Která zboží nakupovali pouze zákazníci narození po roce 2000?”*
- **Hint:** Uses `za.dat_nar <= '2000-12-31'` to exclude older customers.
- **Issue:** “Po roce 2000” naturally means *from 1. 1. 2001 onward*. The hint matches this, but students often confuse inclusive/exclusive boundaries.
- **Suggestion:** Add a clarifying parenthesis to the assignment: *„(tj. od 1. 1. 2001)“*.

---

### 2.4 `b13` — NULL branch edge case not covered by hint

- **Hint:** `… AND NOT EXISTS (SELECT 1 FROM ucet u2 WHERE u2.r_cislo = k.r_cislo AND u2.pobocka <> 'Janska')`
- **Issue:** If a client had an account with `pobocka IS NULL`, the condition `<> 'Janska'` would evaluate to `UNKNOWN`, so `NOT EXISTS` would still be true and the client would incorrectly appear as “only Jánská”.
- **Current data:** No NULL branches exist, so the bug is latent.
- **Suggestion:** Harden the hint for future data edits:
  ```sql
  … AND NOT EXISTS (
      SELECT 1 FROM ucet u2
      WHERE u2.r_cislo = k.r_cislo
        AND (u2.pobocka <> 'Janska' OR u2.pobocka IS NULL)
  )
  ```

---

## 3. Minor / Cosmetic Issues

### 3.1 `firma` schema display omits `NOT NULL`

- **Location:** `index.html` → `datasets.firma.schema.zamestnanec`
- **Issue:** The `oddelenie` column is `TEXT NOT NULL` in the DDL but the JSON schema object shows it without `notNull: true`.
- **Fix:** Add `notNull: true` to the schema row for `oddelenie`.

---

### 3.2 `validate.py` and `validate_consistency.py` redundancy

- The two Python files each contain the full dataset strings and query lists, duplicating the source of truth in `index.html`.
- **Suggestion:** A future refactor could load datasets from a shared JSON or YAML file, but for a single-exam project this is acceptable.

---

## 4. Verified Correct Behavior

| Area | Status | Evidence |
|------|--------|----------|
| FK integrity (all 6 datasets) | ✅ | `validate_consistency.py` — 0 orphan rows across all tables |
| Hint SQL syntax (SQLite) | ✅ | No `ALL/ANY/SOME`, `TO_DATE`, or `ROWNUM` found in any executable hint |
| Data richness for questions | ✅ | Every aggregate, join, and subquery has sufficient rows to produce meaningful results |
| Theory questions (t1–t8) | ✅ | Marked `executable: false`; hints match typical exam/reference syntax |
| `validate.py` execution | ✅ | 55/55 PASS |
| `validate_consistency.py` | ✅ | 32/32 PASS |

---

## 5. Recommended Priority Fix List

1. **Blocker** — Add deterministic `ORDER BY` tie-break to `u6` and `s1` hints.
2. **Blocker** — Decide on a strategy for row-order checking:
   - **Option A:** Add `ORDER BY` clauses to all hints where order is undefined (especially `b6`, `b8`, `b10`, `b11`, `o1`, `u1`, `u3`, `f1`, `s2`, `s3`, `d6`, `d8`).
   - **Option B:** Patch `resultsEqual` to sort rows canonically before comparing.
3. **High** — Choose **2–3** of the empty-result questions (`b14`, `s4`, `s6`, `u7`) and adjust data so that at least one row is returned, making the questions less confusing.
4. **Medium** — Harden `b13` hint against NULL branches.
5. **Low** — Add `notNull: true` to `firma` schema display for `oddelenie`.

---

*End of review.*
