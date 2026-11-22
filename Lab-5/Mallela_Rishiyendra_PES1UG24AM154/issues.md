# Lab 5 – Issue Table (digital_wallet.py)

**Student:** Rishyendra M (PES1UG24AM154), Section C
**Assigned repo:** https://github.com/SETAPESU26/L5_29_digital_wallet

Scores: Pylint **5.69/10 → 10.00/10**, Bandit **4 issues (1 High, 1 Medium, 2 Low) → 0**, Flake8 **4 issues → 0**.

| # | Issue | Tool / Code | Type | Severity | Line(s) (original) | Description | Fix Approach |
|---|-------|-------------|------|----------|--------------------|-------------|--------------|
| 1 | Weak hash (SHA-1) for PIN | Bandit B324 | Security | **High** | 14 | `hashlib.sha1` is broken for security use; PINs hashed with it can be attacked. | Switched to `hashlib.sha256` and compare with `hmac.compare_digest` (constant time, no timing leak). |
| 2 | Insecure temp file | Bandit B306 | Security | **Medium** | 60 | `tempfile.mktemp()` only returns a name – another process can create the file first (race / symlink attack, CWE-377). | Replaced with `tempfile.mkstemp()`, which atomically creates the file, then close the descriptor. |
| 3 | Hardcoded secret / PIN | Bandit B105 | Security | Low (but real) | 6–7 | Gateway key `sk_demo_wallet_0000` and PIN `4321` stored in plain text in source. | Gateway key read from env var `WALLET_GATEWAY_SECRET`; only a SHA-256 hash of the PIN is kept (overridable by `WALLET_PIN_HASH`). |
| 4 | Non-crypto RNG for OTP | Bandit B311 | Security | Low | 64 | `random.randint` is predictable; OTPs must be unguessable. | Use `secrets.randbelow(900000) + 100000`. |
| 5 | Mutable default argument | Pylint W0102 | Bug | Medium | 17 | `log=[]` is shared across every call to `addMoney`, so entries leak between calls. | Default `log=None`, create a new list inside the function. |
| 6 | Global statement | Pylint W0603 | Design | Medium | 28 | `setDailyLimit` rebinds module global `daily_limit`. | Store limit in the `wallet` dict (`wallet["daily_limit"]`), no `global` needed. |
| 7 | Unused argument | Pylint W0613 | Code smell | Low | 50 | `merchantType` accepted but never used. | Renamed to `merchant_type=None` and explicitly documented/ignored; cashback rate moved to constant `CASHBACK_RATE`. |
| 8 | Naming convention | Pylint C0103 | Style | Low | 9,13,17,27,32,45,50,54,58,78 | camelCase function/argument/variable names (`hashPin`, `addMoney`, `newLimit`, `creditAmounts` …). | Renamed to snake_case (`hash_pin`, `add_money`, `new_limit`, `credit_amounts` …). |
| 9 | Missing docstrings | Pylint C0114/C0116 | Style | Low | 1 and every function | No module or function documentation. | Added module docstring and a docstring for every function. |
| 10 | Inline comment spacing | Flake8 E261 | Style | Low | 76 | Only one space before `#`. | Two spaces before inline comment. |
| 11 | Missing whitespace around operator / after comma | Flake8 E225, E231 | Style | Low | 78, 79 | `creditAmounts=[...]`, `print("Total credited:",sum(...))`. | Added whitespace per PEP 8. |
| 12 | Missing blank lines / top-level call | Flake8 E305 | Style | Low | 80 | `main()` called directly after function with no blank lines; runs on import. | Two blank lines and an `if __name__ == "__main__":` guard. |

Program output is unchanged after the fixes (same messages, final balance Rs. 1900.0, total credited 2500), except the OTP which is random by design.
