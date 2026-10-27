# header-lint

Catch CSV header problems before they break a load or a SQL query: duplicate names (case-insensitive), blank headers, stray spaces, non-snake_case names and SQL reserved words like `user` or `order`. Each issue comes with a suggested snake_case name.

Pure Python stdlib. Handles a UTF-8 BOM.

```bash
python header_lint.py export.csv
```

Prints a JSON list of issues and exits `1` if there are any.

```bash
python -m unittest -v
```
