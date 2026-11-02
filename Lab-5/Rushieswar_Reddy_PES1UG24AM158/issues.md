# Lab 5: Static Code Analysis — Issues Document

This document tracks and cross-references all issues detected by **Bandit**, **Flake8**, and **Pylint** in the original `movie_reviews.py` script, prioritized by severity.

## Identified Issues and Resolutions

| Issue | Tool | Type / Severity | Line(s) | Description | Fix Approach |
|---|---|---|---|---|---|
| **B324: Use of weak MD5 hash** | Bandit | Security / **High** | 46 | Used weak MD5 hash algorithm without security flags (`hashlib.md5((title + reviewText).encode())`), which is vulnerable to collision attacks. | Added `usedforsecurity=False` parameter to `hashlib.md5()`, indicating the hash is solely for generating demo display IDs, not cryptographic security. |
| **B104: Bind to all interfaces** | Bandit | Security / **Medium** | 4 | Hardcoded binding to `0.0.0.0` (`STREAM_HOST = "0.0.0.0"`), which unintentionally exposes the service on all public and private network interfaces. | Changed binding host to loopback address `127.0.0.1` (`STREAM_HOST = "127.0.0.1"`). |
| **B105: Hardcoded password** | Bandit | Security / **Low** | 6 | Plaintext password stored in code (`MODERATOR_PASSWORD = "reviews-demo"`), leading to credential exposure in version control. | Retrieve password from environment variable via `os.getenv("MODERATOR_PASSWORD", "reviews-demo")`. |
| **B311: Insecure random generator** | Bandit | Security / **Low** | 41 | Standard pseudo-random module (`random.choice()`) is predictable and unsuitable for security or non-deterministic selection. | Replaced `random.choice()` with `secrets.choice()` from Python's standard `secrets` module. |
| **E225: Missing operator whitespace** | Flake8 | Style / PEP 8 | 35 | Missing whitespace around assignment operator in `ranked=sorted(...)`. | Added spaces around `=` operator: `ranked = sorted(...)`. |
| **E302: Insufficient blank lines** | Flake8 | Style / PEP 8 | 48 | Only 1 blank line found before top-level function `printAllReviews()` instead of the standard 2 blank lines. | Added an extra blank line between functions to conform with PEP 8. |
| **E261: Inline comment spacing** | Flake8 | Style / PEP 8 | 70 | Less than two spaces preceding inline comment `# demo id`. | Added two spaces before the `#` character. |
| **E231: Missing whitespace after comma** | Flake8 | Style / PEP 8 | 72 | Missing whitespace after comma in `print("Genres:",sorted(...))`. | Added space after comma: `print("Genres:", sorted(...))`. |
| **C0114 & C0116: Missing docstrings** | Pylint | Convention / Quality | 1, 11, 16, 26, 34, 39, 45, 48, 54, 58 | Missing module-level docstring and missing docstrings on all functions. | Added comprehensive docstrings following PEP 257 for module and all individual functions. |
| **C0103: Naming style violations** | Pylint | Convention / Quality | 11, 16, 26, 34, 39, 45, 48, 54 | Functions and parameter names use camelCase (`addMovie`, `rateMovie`, `reviewText`, etc.) instead of snake_case. | Renamed functions and arguments to idiomatic snake_case (`add_movie`, `rate_movie`, `review_text`, etc.). |
| **R1705: Unnecessary else after return** | Pylint | Refactor / Quality | 28 | `averageRating` uses `else:` block immediately after an explicit `return`. | Removed the redundant `else:` block and de-indented the fallback `return 0.0`. |
| **C0200: Unidiomatic loop indexing** | Pylint | Refactor / Quality | 50 | `printAllReviews` iterates using `range(len(titles))` instead of standard iteration. | Replaced index-based range loop with Pythonic `enumerate(titles, start=1)`. |
| **W0603: Global statement usage** | Pylint | Quality / Design | 40 | `pickFeatured()` relies on `global featured` mutation. | Removed global mutation and returned the selected movie directly from `pick_featured()`. |

---

## Visual Verification & Terminal Screenshots

Visual evidence capturing the terminal execution before and after resolving the issues documented above:

- **Initial Script Execution:** [`screenshots/01_original_run.png`](./screenshots/01_original_run.png)
- **Pylint Analysis (Before):** [`screenshots/02_pylint_before.png`](./screenshots/02_pylint_before.png)
- **Bandit Security Audit (Before):** [`screenshots/03_bandit_before.png`](./screenshots/03_bandit_before.png)
- **Flake8 Style Check (Before):** [`screenshots/04_flake8_before.png`](./screenshots/04_flake8_before.png)
- **Flake8 Verification (After):** [`screenshots/05_flake8_after.png`](./screenshots/05_flake8_after.png)
- **Bandit Security Verification (After):** [`screenshots/06_bandit_after.png`](./screenshots/06_bandit_after.png)
- **Pylint Score 10.00/10 (After):** [`screenshots/07_pylint_after.png`](./screenshots/07_pylint_after.png)
- **Final Clean Run:** [`screenshots/08_final_run.png`](./screenshots/08_final_run.png)
