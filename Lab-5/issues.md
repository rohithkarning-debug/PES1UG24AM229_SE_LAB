# Issues Found – ecommerce_cart_system.py

High and medium severity first.

| # | Issue | Tool / Code | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|---------|-------------|--------------|
| 1 | Shell command execution | Bandit B605 (High) | Security | 60 | `os.system("echo ... " + filename)` runs a shell with user-controlled text, allowing command injection | Removed the shell call and used `print()` instead |
| 2 | Weak hash | Bandit B324 (High) | Security | 49 | `hashlib.md5` is broken for security use | Switched to `hashlib.sha256` |
| 3 | Use of eval | Bandit B307 (Medium), Pylint W0123 | Security | 44 | `eval(discount_expr)` executes any string passed in | Function now takes a numeric `discount_rate`, validated to be between 0 and 1 |
| 4 | Hardcoded secret printed | Manual review | Security | 72, 81 | Live payment key hardcoded and printed to the console | Read from `PAYMENT_GATEWAY_KEY` env variable; only print whether it is set |
| 5 | Insecure random | Bandit B311 (Low) | Security | 53 | `random.randint` is predictable, unsuitable for a checkout PIN | Used `secrets.randbelow(9000) + 1000` |
| 6 | try/except/pass, bare except | Bandit B110 (Low), Pylint W0702, Flake8 E722 | Bug | 26–29 | All errors silently swallowed when removing an item | Catch only `KeyError` and return `False`/`True` |
| 7 | Mutable default argument | Pylint W0102 | Bug | 15 | `audit_log=[]` is shared across all calls | Default to `None` and create a new list inside |
| 8 | Global variable | Pylint W0603, C0103 | Bug / Design | 12, 16, 20 | `total_sales` ignored items already in the cart and was never reduced on removal | Removed the global; added `calculate_cart_total()` computed from the cart |
| 9 | Price truncated in log | Manual review, Pylint C0209 | Bug | 21 | `%d` turned 1.99 into 1 in the audit log | f-string with `{price:.2f}` |
| 10 | File not closed safely | Pylint R1732, W1514 | Bug | 57–59 | `open()` without `with` or encoding | `with open(filename, "w", encoding="utf-8")` |
| 11 | Unused import / variables | Flake8 F401, F841; Pylint W0611, W0612 | Style | 4, 33, 43, 65 | `math`, `handling_fee`, loop var `k` unused | Removed them |
| 12 | Comparison to None | Flake8 E711, Pylint C0121 | Style | 34 | `== None` instead of `is None` | Changed to `is None` |
| 13 | Shadowed name | Pylint W0621 | Style | 63 | Parameter `cart_items` hides the global | Renamed parameter to `items` |
| 14 | Naming / docstrings | Pylint C0103, C0114, C0116 | Style | All functions | camelCase names, no docstrings | snake_case names, module and function docstrings |
| 15 | Long line, missing newline | Flake8 E501, W292 | Style | 76, 84 | Line over 79 chars, no final newline | Shortened call, added final newline |
| 16 | Redundant if/else | Pylint R1703, R1705 | Style | 36–39 | `if ...: return True else: return False` | `return item["qty"] > 0` |
| 17 | Module-level call | Manual review | Design | 84 | `main()` ran on import | Wrapped in `if __name__ == "__main__":` |
