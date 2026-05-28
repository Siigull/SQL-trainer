#!/usr/bin/env python3
"""
Use sqlglot to analyze theory question answers and extract required keyword signatures.
The output is JSON that can be embedded into the web app for lightweight validation.
"""
import json

# We can run this manually; for now we define signatures manually based on sqlglot capabilities.
# sqlglot token_type mapping for Oracle dialect:
# CREATE, TRIGGER, OR, REPLACE, BEFORE, AFTER, DELETE, INSERT, UPDATE, ON, BEGIN, END,
# DECLARE, CURSOR, IS, OPEN, FETCH, INTO, CLOSE, GRANT, ALL, SELECT, MATERIALIZED, VIEW,
# REFRESH, COMMIT, SAVEPOINT, ROLLBACK, UNION, UNION_ALL, etc.

THEORY_QUESTIONS = [
    {
        "id": "t1",
        "title": "DDL: Vytvoření tabulky",
        "required_tokens": ["CREATE", "TABLE", "PRIMARY_KEY", "NOT_NULL"],
        "case_insensitive": True,
        "notes": "Must contain CREATE TABLE, a PRIMARY KEY, and a NOT NULL constraint."
    },
    {
        "id": "t2",
        "title": "DDL: Cizí klíč s CASCADE",
        "required_tokens": ["ALTER", "TABLE", "ADD", "FOREIGN_KEY", "REFERENCES", "ON", "DELETE", "CASCADE"],
        "case_insensitive": True,
        "notes": "Must contain ALTER TABLE, ADD CONSTRAINT/FOREIGN KEY, REFERENCES, ON DELETE CASCADE."
    },
    {
        "id": "t3",
        "title": "DCL: GRANT",
        "required_tokens": ["GRANT", "ALL", "ON", "TO"],
        "case_insensitive": True,
        "notes": "GRANT ALL ON ... TO user01"
    },
    {
        "id": "t4",
        "title": "Teorie: SAVEPOINT",
        "required_keywords": ["SAVEPOINT", "ROLLBACK", "COMMIT"],
        "case_insensitive": True,
        "notes": "Explanation must mention SAVEPOINT, ROLLBACK, and COMMIT."
    },
    {
        "id": "t5",
        "title": "Teorie: UNION vs UNION ALL",
        "required_keywords": ["UNION", "ALL", "duplicit"],
        "case_insensitive": True,
        "notes": "Must mention UNION, UNION ALL, and something about duplicates/duplicity."
    },
    {
        "id": "t6",
        "title": "DDL: Trigger pro audit",
        "required_tokens": ["CREATE", "TRIGGER", "BEFORE", "DELETE", "ON", "BEGIN", "INSERT", "INTO", "END"],
        "case_insensitive": True,
        "notes": "Must contain CREATE TRIGGER, BEFORE DELETE, BEGIN/END block, and INSERT INTO."
    },
    {
        "id": "t7",
        "title": "DCL: CURSOR",
        "required_tokens": ["CURSOR", "IS", "SELECT", "OPEN", "FETCH", "INTO", "CLOSE"],
        "case_insensitive": True,
        "notes": "Must contain CURSOR declaration, SELECT, OPEN, FETCH INTO, CLOSE."
    },
    {
        "id": "t8",
        "title": "DDL: Materializovaný pohled",
        "required_tokens": ["CREATE", "MATERIALIZED", "VIEW", "SELECT", "COUNT"],
        "case_insensitive": True,
        "notes": "Must contain CREATE MATERIALIZED VIEW, SELECT, and COUNT."
    }
]

def print_json():
    print(json.dumps(THEORY_QUESTIONS, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print_json()
