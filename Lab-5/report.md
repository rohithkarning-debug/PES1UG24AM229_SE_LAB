# Lab 5: Static Code Analysis – Report

**Name:** Rohith Karning  **SRN:** PES1UG24AM229
**Assigned program:** `ecommerce_cart_system.py` (E-Commerce Cart System)
**Tools:** Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1 (Python 3.13)

## 1. Objective

Analyse the assigned Python program with Pylint, Bandit and Flake8, document the issues found, fix them in order of severity, and verify the fixes by re-running the tools.

## 2. Commands Used

```bash
python3 -m venv venv
source venv/bin/activate
pip install pylint bandit flake8
python ecommerce_cart_system.py
pylint ecommerce_cart_system.py > pylint_report.txt
bandit -r ecommerce_cart_system.py > bandit_report.txt
flake8 ecommerce_cart_system.py > flake8_report.txt
```

## 3. Results – Before vs After

| Tool | Before | After |
|------|--------|-------|
| Pylint | 3.86/10 (35 messages) | **10.00/10** (0 messages) |
| Bandit | 5 issues: 2 High, 1 Medium, 2 Low | **0 issues** |
| Flake8 | 7 warnings (F401, E722, F841 ×2, E711, E501, W292) | **0 warnings** |

Reports are in `reports/before/` and `reports/after/`.

## 4. Commits

| Commit | Tool | Summary |
|--------|------|---------|
| 1 | Bandit | Removed `eval`, `os.system`, MD5, `random` PIN and try/except/pass; moved payment key to an environment variable |
| 2 | Flake8 | Removed unused import and variable, fixed `== None`, added final newline |
| 3 | Pylint | Docstrings, snake_case names, mutable default fixed, global removed, `with open`, simplified logic, `__main__` guard |

## 5. Program Output After Fixes

```
Is ITEM1 in cart: True
Discounted Price: 22.5
Item Hash: de124cf18e4be214c25c0c75410474d1b4c4b45679baa47caf3404bd34c806dc
Checkout PIN: 7701
Receipt saved to: receipt.txt
Total items: 6
Cart total: 220.00
Gateway key configured: False
```

The program still works as before. The secret key is no longer printed, and a correct cart total is shown (ITEM1 50 + ITEM3 135 + ITEM4 35 = 220).

## 6. Issues Found and Fixes

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

## 7. Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style issues from Flake8 and Pylint, such as the unused `math` import, `== None`, the missing final newline and the missing docstrings. Each one points at an exact line and the fix is a one-line change. The hardest was the `eval()` in `calculateDiscountedTotal`. I could not just delete it because the function depended on it, so I had to change what the function accepts (a numeric discount rate instead of an expression string) and update the caller. Removing the `total_sales` global was also harder than it looked, because the value was wrong anyway (it ignored items already in the cart and never went down on removal), so I replaced it with a function that computes the total from the cart.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit's B311 warning on `random.randint` would be a false positive in many programs, for example shuffling a list for display. Here it was a real issue because the value was a checkout PIN. The MD5 warning (B324) is similar: the hash is only used as an item identifier, not for passwords, so it could have been kept with `usedforsecurity=False`, but switching to SHA-256 was just as easy. Some Pylint naming warnings, like `total_sales` needing UPPER_CASE, are also arguably false positives because it was a mutable variable, not a constant. On the other side, the tools missed some real problems: Bandit did not flag the hardcoded payment key (its name doesn't contain "password"), and none of the tools noticed the `%d` that cut 1.99 down to 1 in the audit log.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint automatically through a pre-commit hook so style problems are caught before they are committed, and run all three tools, including Bandit, in a CI pipeline (for example GitHub Actions) on every push and pull request. The pipeline would fail if Bandit finds any medium or high issue or the Pylint score drops below a set threshold such as 9.5. A shared config file (`.pylintrc`, `setup.cfg`) would keep the rules the same for the whole team.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 3.86/10 to 10.00/10, Bandit went from 5 issues (2 high, 1 medium, 2 low) to 0, and Flake8 went from 7 warnings to 0. The code is safer: no arbitrary code execution through `eval`, no shell call, no secret printed to the console and a secure PIN generator. It is more robust: removing a missing item now returns `False` instead of silently hiding every error, the audit log is no longer shared between calls, and the receipt file is always closed. It is also easier to read, with consistent snake_case names, docstrings on every function and simpler logic, and the program now prints a correct cart total.
