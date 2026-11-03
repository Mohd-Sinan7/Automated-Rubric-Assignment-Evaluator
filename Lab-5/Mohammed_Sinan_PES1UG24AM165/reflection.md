# Lab 5: Reflection on Static Code Analysis

**Student:** Mohammed Sinan (PES1UG24AM165)  
**Assigned Repository:** `SETAPESU26/L5_40_bank_account_systen`  
**File Analyzed:** `bank_account_system.py`

---

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

### Easiest Issues:
The easiest issues to address were the style, formatting, and PEP 8 violations detected by Flake8 and Pylint. These included:
- Removing unused imports (`import sys`, `F401`).
- Replacing equality comparison with identity for `None` (`account_data.get(acc_id) == None` to `is None`, `E711`).
- Deleting the dead/unused variable `service_fee = 2.50` (`F841`).
- Wrapping lines exceeding 79 characters (`E501`) and appending the missing trailing newline (`W292`).
- Renaming functions to match `snake_case` conventions (`createAccount` -> `create_account`, `C0103`).

These issues required localized, single-line adjustments with deterministic fixes that posed zero risk of changing business logic or runtime behavior.

### Hardest Issues:
1. **Arbitrary Code Execution via `eval()` (Bandit B307 / Pylint W0123):**
   Simply removing or suppressing `eval()` was not an option because `compute_bonus()` relies on calculating an expression dynamically (`"bal * 0.05"`). Replacing it securely required parsing the expression into an Abstract Syntax Tree (AST) using Python's `ast` module and evaluating only whitelisted binary operations (`+`, `-`, `*`, `/`) and constant/numeric nodes. This prevented any malicious code injection (such as `__import__('os').system(...)`) while preserving full mathematical functionality.

2. **Mutable Default Argument (`transactions=[]`, Pylint W0102):**
   While the syntax fix is simple (`transactions=None` with initialization inside the body), understanding the underlying mechanism requires knowing how Python handles default arguments. Default parameters are evaluated only once at function definition time when the module is loaded, not upon each function call. Consequently, all callers without an explicit `transactions` argument inadvertently append to and mutate the exact same shared list in memory, causing cross-account data leakage.

3. **Subtle Security Flaws (Bandit B324, B311, B605, B105):**
   Addressing security issues required choosing cryptographically sound primitives: replacing MD5 with SHA-256 for PIN hashing, replacing the pseudo-random `random` module with `secrets` for cryptographic PIN generation, replacing `os.system` with native Python operations to avoid shell injection, and extracting sensitive tokens to environment variables (`os.getenv`).

---

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes. Static analysis inspects code structure without executing it, which can produce both **false positives** and **context-dependent warnings**:

1. **Unused Variable Warning on `bal` (Pylint W0612 / Flake8 F841):**
   In the original code:
   ```python
   def compute_bonus(acc_id, expr):
       bal = account_data[acc_id]["balance"]
       bonus = eval(expr)
       return bonus
   ```
   Both Flake8 and Pylint flagged `bal` as an unused local variable. In reality, `bal` was used at runtime when `eval("bal * 0.05")` looked up the variable in the local namespace. Because static analysis tools cannot introspect inside dynamic string expressions evaluated at runtime, they assumed `bal` was dead code. Removing `bal` based blindly on the tool's warning would have crashed the program with a runtime `NameError`. Once `eval()` was replaced with a structured AST evaluator receiving `{"bal": bal}`, the variable reference became explicit to both the Python compiler and static analyzers.

2. **Context-Dependent Findings in Bandit:**
   Bandit flags any use of MD5 (`B324`) or `random` (`B311`) as security vulnerabilities. If `random` is used solely for non-sensitive simulations (like dice rolling) or MD5 is used as a legacy cache key checksum (`usedforsecurity=False`), these flags would be false positives for security threats. However, in our banking context where the PIN and temporary tokens protect financial accounts, the warnings were true positives and required cryptographic upgrades (`secrets` and SHA-256).

3. **False Negatives in Secret Detection (Bandit B105):**
   Bandit detects hardcoded credentials by scanning variable names containing patterns like `token`, `secret`, or `password`. If an engineer names the variable `auth_data = "SUPER_SECRET_KEY"`, Bandit may pass without warning. This demonstrates that static analysis must always be paired with manual code reviews and dynamic testing.

---

## 3. How would you integrate static analysis tools into your actual software development workflow?

A robust software development lifecycle implements static code analysis at multiple concentric layers:

1. **Local IDE Integration (Real-Time Feedback):**
   Configure IDE plugins (VS Code, PyCharm, Antigravity) with Pylint and Flake8 / Ruff language servers. This provides immediate squiggly underlines and lint warnings as developers write code, allowing errors to be resolved at the lowest possible cost.

2. **Pre-Commit Git Hooks:**
   Implement client-side hooks using the `pre-commit` framework (`.pre-commit-config.yaml`):
   ```yaml
   repos:
     - repo: https://github.com/pycqa/flake8
       rev: 7.1.1
       hooks:
         - id: flake8
     - repo: https://github.com/PyCQA/bandit
       rev: 1.7.10
       hooks:
         - id: bandit
           args: ["-r", "-ll"]
   ```
   This prevents non-compliant or insecure code from ever being committed to local git history.

3. **Continuous Integration (CI) Quality Gates:**
   In GitHub Actions or GitLab CI, create an automated workflow running on every Pull Request:
   ```bash
   flake8 . --count --max-line-length=79
   bandit -r . -ll
   pylint **/*.py --fail-under=9.5
   ```
   Pull requests that fail these checks are automatically blocked from merging into `main`.

4. **Centralized Configuration:**
   Maintain unified configuration files (`pyproject.toml`, `.pylintrc`, `.flake8`) across the entire repository to ensure identical linting rules between developer machines and CI build runners.

---

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The transformation yielded dramatic, measurable improvements across security, correctness, and maintainability:

| Metric / Dimension | Baseline (Original) | Cleaned Version | Impact |
|---|---|---|---|
| **Pylint Score** | **5.62 / 10** | **10.00 / 10** | Perfect rating, 0 warnings or design issues |
| **Bandit Issues** | **6 issues (2 High, 1 Med, 3 Low)** | **0 issues** | Fully eliminated command injection, weak crypto, arbitrary eval |
| **Flake8 Violations**| **7 violations** | **0 violations** | Strict PEP 8 style conformance |
| **Security Posture** | Vulnerable to shell injection, code execution, MD5 collisions | Secure SHA-256, `secrets` CSPRNG, safe AST evaluation, env tokens | Eliminates attack surfaces entirely |
| **State Isolation** | `transactions=[]` caused cross-account data contamination | `transactions=None` initializes fresh list per account | Guarantees account isolation |
| **Error Handling** | Bare `except: pass` hid missing accounts silently | Explicit key checks with boolean status returns | Predictable runtime behavior and transparency |
| **Modular Execution** | Script executed side effects on plain `import` | Wrapped inside `if __name__ == "__main__":` | Module can now be cleanly imported and unit-tested |
| **Maintainability** | Non-standard names, missing docstrings, dead code | Comprehensive PEP 257 docstrings, snake_case, clean logic | High readability for peer developers |
