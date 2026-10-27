"""header-lint: catch CSV header problems (duplicates, blanks, spaces, bad names, SQL reserved words) before load."""
import argparse, csv, json, re, sys
from collections import Counter

RESERVED = {"select", "from", "where", "order", "group", "table", "user", "date", "time",
            "timestamp", "key", "value", "index", "desc", "asc", "limit", "join", "default", "check"}
SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")

def snake(name):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name.strip())
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    return ("c_" + s) if s[:1].isdigit() else (s or "unnamed")

def lint(headers):
    issues = []
    dup = Counter(h.strip().lower() for h in headers)
    for i, h in enumerate(headers, 1):
        def add(kind): issues.append({"position": i, "header": h, "issue": kind, "suggest": snake(h)})
        if not h.strip(): add("blank"); continue
        if h != h.strip(): add("leading/trailing whitespace")
        if dup[h.strip().lower()] > 1: add("duplicate (case-insensitive)")
        if not SNAKE.match(h.strip()): add("not snake_case")
        if h.strip().lower() in RESERVED: add("SQL reserved word")
    return issues

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv")
    a = p.parse_args(argv)
    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        headers = next(csv.reader(f), [])
    issues = lint(headers)
    print(json.dumps(issues, indent=2))
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(main())
