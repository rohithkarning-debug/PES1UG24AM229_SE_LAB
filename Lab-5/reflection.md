# Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style issues from Flake8 and Pylint, such as the unused `math` import, `== None`, the missing final newline and the missing docstrings. Each one points at an exact line and the fix is a one-line change. The hardest was the `eval()` in `calculateDiscountedTotal`. I could not just delete it because the function depended on it, so I had to change what the function accepts (a numeric discount rate instead of an expression string) and update the caller. Removing the `total_sales` global was also harder than it looked, because the value was wrong anyway (it ignored items already in the cart and never went down on removal), so I replaced it with a function that computes the total from the cart.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Bandit's B311 warning on `random.randint` would be a false positive in many programs, for example shuffling a list for display. Here it was a real issue because the value was a checkout PIN. The MD5 warning (B324) is similar: the hash is only used as an item identifier, not for passwords, so it could have been kept with `usedforsecurity=False`, but switching to SHA-256 was just as easy. Some Pylint naming warnings, like `total_sales` needing UPPER_CASE, are also arguably false positives because it was a mutable variable, not a constant. On the other side, the tools missed some real problems: Bandit did not flag the hardcoded payment key (its name doesn't contain "password"), and none of the tools noticed the `%d` that cut 1.99 down to 1 in the audit log.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run Flake8 and Pylint automatically through a pre-commit hook so style problems are caught before they are committed, and run all three tools, including Bandit, in a CI pipeline (for example GitHub Actions) on every push and pull request. The pipeline would fail if Bandit finds any medium or high issue or the Pylint score drops below a set threshold such as 9.5. A shared config file (`.pylintrc`, `setup.cfg`) would keep the rules the same for the whole team.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 3.86/10 to 10.00/10, Bandit went from 5 issues (2 high, 1 medium, 2 low) to 0, and Flake8 went from 7 warnings to 0. The code is safer: no arbitrary code execution through `eval`, no shell call, no secret printed to the console and a secure PIN generator. It is more robust: removing a missing item now returns `False` instead of silently hiding every error, the audit log is no longer shared between calls, and the receipt file is always closed. It is also easier to read, with consistent snake_case names, docstrings on every function and simpler logic, and the program now prints a correct cart total.
