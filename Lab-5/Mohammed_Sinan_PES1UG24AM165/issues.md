# Static Code Analysis Issues — Bank Account System

**Target File:** `bank_account_system.py`  
**Repository:** `SETAPESU26/L5_40_bank_account_systen`  
**Student:** Mohammed Sinan (PES1UG24AM165)

---

## Issue Documentation Table

| Issue | Tool & Code | Type | Line(s) | Severity | Description | Fix Approach |
|---|---|---|---|---|---|---|
| **Arbitrary Code Execution via `eval()`** | Bandit B307 / Pylint W0123 | Security / Bug | 39 | High / Medium | Use of `eval(expr)` allows execution of arbitrary code through unvalidated input strings. | Replace `eval` with a safe recursive AST evaluator (`ast.parse` and whitelist allowed math operators `+`, `-`, `*`, `/`) restricting input strictly to mathematical calculations. |
| **Insecure Cryptographic Hash (MD5)** | Bandit B324 | Security | 44 | High | `hashlib.md5()` is cryptographically weak, vulnerable to collision attacks, and unsuitable for security/PIN hashing. | Replaced MD5 hashing with SHA-256 (`hashlib.sha256(pin.encode('utf-8')).hexdigest()`), ensuring cryptographic integrity. |
| **Shell Command Injection via `os.system`** | Bandit B605 | Security | 55 | High | `os.system("echo Backup complete: " + filename)` spawns an OS shell, vulnerable to command injection if `filename` contains metacharacters. | Replaced shell process execution with native Python output (`print(f"Backup complete: {filename}")`), eliminating shell exposure. |
| **Weak Pseudo-Random Number Generator** | Bandit B311 | Security | 48 | Low / Medium | `random.randint()` is a deterministic PRNG unsuitable for authentication tokens or PINs. | Replaced `random` with Python's cryptographically secure `secrets.SystemRandom().randint(1000, 9999)`. |
| **Silent Exception Suppression (`try-except-pass`)** | Bandit B110 / Pylint W0702 / Flake8 E722 | Security / Bug | 20–23 | Low / Medium | Bare `except:` catching and suppressing all exceptions with `pass`, hiding errors and failing silently. | Removed bare try-except and replaced with explicit key check (`if acc_id not in account_data: return False`) and proper balance update. |
| **Hardcoded Secret / Token** | Bandit B105 | Security | 59 | Low / Medium | Hardcoded credentials string `admin_token = "SUPER_SECRET_BANK_TOKEN_2026"` embedded in source code. | Extracted token retrieval to environment variables (`os.getenv("ADMIN_TOKEN", "...")`) to decouple configuration from code. |
| **Mutable Default Argument** | Pylint W0102 | Bug | 11 | High | `transactions=[]` defines a mutable list as a default argument, which is evaluated once and shared across all subsequent calls. | Set default argument to `transactions=None` and initialize `transactions = []` inside the function body if `None`. |
| **Unused Variable (`service_fee`)** | Flake8 F841 / Pylint W0612 | Bug / Dead Code | 27 | Medium | Variable `service_fee = 2.50` is assigned in `withdraw()` but never used or deducted from balance. | Removed unused local variable `service_fee` to prevent dead code and eliminate developer confusion. |
| **Singleton Comparison with `== None`** | Flake8 E711 / Pylint C0121 | Style / Quality | 28 | Low | Comparison to `None` performed using equality operator `== None` instead of identity `is None`. | Changed `account_data.get(acc_id) == None` to `account_data.get(acc_id) is None`. |
| **Unused Module Import (`sys`)** | Flake8 F401 / Pylint W0611 | Style / Quality | 6 | Low | `sys` was imported at module top level but never referenced anywhere in the script. | Removed `import sys` from the imports section. |
| **Non-PEP 8 Function Name (`createAccount`)** | Pylint C0103 | Convention | 11 | Low | Function name `createAccount` violates PEP 8 `snake_case` naming conventions for functions. | Renamed function to `create_account` and updated caller in `main()`. |
| **Unnecessary `else` After `return`** | Pylint R1705 | Refactoring | 30–34 | Low | Unneeded `else` block following `if account_data[acc_id]["balance"] < amount: return False`. | Removed redundant `else` and de-indented the subsequent logic. |
| **Unspecified Encoding & Missing Context Manager in File I/O** | Pylint W1514 / R1732 | Quality / Resource | 52–54 | Medium | `open(filename, "w")` without explicit UTF-8 encoding and without using `with` context manager risks resource leaks. | Refactored to `with open(filename, "w", encoding="utf-8") as file_handle:`. |
| **Missing Function & Method Docstrings** | Pylint C0116 | Documentation | Multiple | Low | Missing PEP 257 docstrings for module functions (`create_account`, `deposit`, `withdraw`, etc.). | Added informative docstrings to all functions detailing parameters and return behavior. |
| **Legacy String Formatting (`%`)** | Pylint C0209 | Style | 15 | Low | String formatting done using old C-style `%` syntax instead of modern f-strings. | Replaced with f-string: `f"Created {acc_id} with initial balance {initial_deposit}"`. |
| **Line Length Exceeded (> 79 Chars)** | Flake8 E501 | Style | 15 | Low | Line exceeded standard PEP 8 maximum length of 79 characters. | Formatted and split string assignment within PEP 8 character limits. |
| **Missing Trailing Newline at End of File** | Flake8 W292 / Pylint C0304 | Style | 70 | Low | File ended abruptly without POSIX-standard trailing newline. | Added final newline at the end of the file. |
