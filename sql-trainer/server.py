#!/usr/bin/env python3
"""
sql-trainer companion server.
Provides enhanced theory validation via sqlglot when available.
 Falls back to keyword-only validation if sqlglot not installed.

Usage:
    python server.py        # serves on http://localhost:8787
    
Endpoints:
    GET  /                    -> redirect to index.html
    GET  /api/health          -> {sqlglot_available: bool, version: str}
    POST /api/validate-theory -> validate a theory question answer
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ── try to import sqlglot ───────────────────────────────────────
SQLGLOT_AVAILABLE = False
SQLGLOT_VERSION = None
try:
    import sqlglot
    SQLGLOT_AVAILABLE = True
    SQLGLOT_VERSION = sqlglot.__version__
except Exception:
    pass

# ── question signatures (mirrors index.html) ────────────────────
QUESTIONS = {
    "t1": {
        "title": "DDL: Vytvoření tabulky",
        "required": ["CREATE", "TABLE", "PRIMARY KEY", "NOT NULL"],
        "sql_dialect": "oracle",
    },
    "t2": {
        "title": "DDL: Cizí klíč s CASCADE",
        "required": ["ALTER", "TABLE", "FOREIGN KEY", "REFERENCES", "ON DELETE", "CASCADE"],
        "sql_dialect": "oracle",
    },
    "t3": {
        "title": "DCL: GRANT",
        "required": ["GRANT", "ON", "TO"],
        "sql_dialect": "oracle",
    },
    "t4": {
        "title": "Teorie: SAVEPOINT",
        "required": ["SAVEPOINT", "ROLLBACK", "COMMIT"],
        "sql_dialect": None,
    },
    "t5": {
        "title": "Teorie: UNION vs UNION ALL",
        "required": ["UNION", "ALL", "duplicit"],
        "sql_dialect": None,
    },
    "t6": {
        "title": "DDL: Trigger pro audit",
        "required": ["CREATE", "TRIGGER", "BEFORE", "DELETE", "ON", "BEGIN", "INSERT INTO", "END"],
        "sql_dialect": "oracle",
    },
    "t7": {
        "title": "DCL: CURSOR",
        "required": ["CURSOR", "OPEN", "FETCH", "CLOSE", "SELECT"],
        "sql_dialect": "oracle",
    },
    "t8": {
        "title": "DDL: Materializovaný pohled",
        "required": ["CREATE", "MATERIALIZED VIEW", "SELECT", "COUNT"],
        "sql_dialect": "oracle",
    },
    "t8": {
        "title": "DDL: Materializovaný pohled",
        "required": ["CREATE", "MATERIALIZED VIEW", "SELECT", "COUNT"],
        "sql_dialect": "oracle",
    },
}


def validate_with_keywords(text: str, required: list) -> dict:
    txt = text.upper()
    found = []
    missing = []
    for kw in required:
        if kw.upper() in txt:
            found.append(kw)
        else:
            missing.append(kw)
    return {
        "found": found,
        "missing": missing,
        "total": len(required),
        "score": len(found),
        "passed": len(missing) == 0,
        "mode": "keywords",
    }


def validate_with_sqlglot(text: str, q: dict) -> dict:
    """Use sqlglot for token-level analysis + keywords."""
    dialect = q.get("sql_dialect")
    required = q.get("required", [])
    base = validate_with_keywords(text, required)

    tokens_info = []
    ast_type = None
    parse_error = None

    if dialect and SQLGLOT_AVAILABLE:
        try:
            trees = sqlglot.parse(text, read=dialect)
            if trees and trees[0]:
                ast_type = type(trees[0]).__name__
                # Extract recognized keywords from tokens
                for node in trees[0].walk():
                    name = type(node).__name__
                    if name not in tokens_info:
                        tokens_info.append(name)
        except Exception as e:
            parse_error = str(e)
            # Tokenize as fallback
            try:
                for tok in sqlglot.Dialect.get_or_raise(dialect)().tokenizer_class().tokenize(text):
                    tname = tok.token_type.name
                    if tname not in tokens_info:
                        tokens_info.append(tname)
            except Exception:
                pass

    base["sqlglot_available"] = SQLGLOT_AVAILABLE
    base["ast_type"] = ast_type
    base["tokens"] = tokens_info[:30]  # cap
    base["parse_error"] = parse_error
    return base


def validate_answer(qid: str, text: str) -> dict:
    q = QUESTIONS.get(qid)
    if not q:
        return {"error": "Unknown question id", "qid": qid}

    if SQLGLOT_AVAILABLE:
        return validate_with_sqlglot(text, q)
    else:
        return validate_with_keywords(text, q["required"])


# ── HTTP handler ────────────────────────────────────────────────
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def log_message(self, fmt, *args):
        # quiet
        sys.stderr.write(f"[{self.address_string()}] {fmt % args}\n")

    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/api/health":
            self._json(200, {
                "ok": True,
                "sqlglot_available": SQLGLOT_AVAILABLE,
                "sqlglot_version": SQLGLOT_VERSION,
                "questions_loaded": len(QUESTIONS),
            })
            return
        if p.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        p = urlparse(self.path)
        if p.path == "/api/validate-theory":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8") if content_len else "{}"
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {}
            # support both JSON and form-encoded
            qid = data.get("id") or data.get("qid")
            text = data.get("text") or ""
            if not qid:
                self._json(400, {"error": "Missing 'id' or 'qid' field"})
                return
            result = validate_answer(qid, text)
            result["qid"] = qid
            self._json(200, result)
            return
        self._json(404, {"error": "Not found"})

    def _json(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    server = HTTPServer(("", port), Handler)
    print(f"SQL Trainer server running on http://localhost:{port}")
    print(f"sqlglot available: {SQLGLOT_AVAILABLE} {SQLGLOT_VERSION or ''}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()
