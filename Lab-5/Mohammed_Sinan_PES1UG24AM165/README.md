# Lab 5: Static Code Analysis (Bank Account System, repo `SETAPESU26/L5_40_bank_account_systen`)

**Student:** Mohammed Sinan (PES1UG24AM165)  
**Assigned Repository:** [`SETAPESU26/L5_40_bank_account_systen`](https://github.com/SETAPESU26/L5_40_bank_account_systen)

I ran **Pylint**, **Bandit**, and **Flake8** on `bank_account_system.py`, documented all findings, and resolved every single issue. In addition, I fixed critical security vulnerabilities (arbitrary code execution via `eval`, shell injection via `os.system`, weak MD5 hashing, predictable PRNG) and logic bugs (shared mutable default arguments, silent exception suppression).

## Summary Score Comparison

| Tool | Before Fixes | After Fixes | Target |
|---|---|---|---|
| **Pylint** | **5.62 / 10** | **10.00 / 10** | > 9.5 / 10 |
| **Bandit** | **6 issues (2 High, 1 Medium, 3 Low)** | **0 issues (No issues identified)** | 0 issues |
| **Flake8** | **7 violations** | **0 violations** | 0 violations |

---

## Directory Contents

| Path | Description |
|---|---|
| `bank_account_system.py` | Cleaned and refactored Python script with all security, style, and quality issues fixed |
| `issues.md` | Comprehensive documentation table detailing each issue, severity, code, line numbers, and fix approach |
| `reflection.md` | In-depth answers to the four lab reflection questions |
| `reports/before/` | Original baseline static analysis reports (`pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`) |
| `reports/after/` | Final verification static analysis reports confirming clean execution across all three tools |
| `screenshots/` | Screenshots of terminal commands demonstrating the before and after states and git commits |

---

## Git Commits

Three separate commits were created to systematically address issues raised by the three tools:

```
b658b60  Fix code quality, naming conventions, docstrings, and mutable defaults reported by Pylint (Score: 10.00/10)
ba6cb71  Fix code style and PEP 8 formatting issues reported by Flake8 (F401, F841, E501, E711)
28fd3be  Fix security issues reported by Bandit (B105, B110, B307, B311, B324, B605)
9a8bb65  Add files via upload (Initial repository baseline)
```

---

## Screenshots Guide

The following screenshots correspond to the verification steps:

| File Name | Description |
|---|---|
| `01_before_program_run.png` | Initial execution of `bank_account_system.py` displaying the raw output |
| `02_before_pylint.png` | Initial Pylint run on the unedited script showing rating `5.62/10` |
| `03a_before_bandit_top.png` | Initial Bandit run showing high-severity security vulnerabilities (Part 1) |
| `03b_before_bandit_end.png` | Initial Bandit run summary showing 6 detected issues (Part 2) |
| `04_before_flake8.png` | Initial Flake8 run showing 7 PEP 8 style violations |
| `05_after_program_run.png` | Execution of fixed `bank_account_system.py` showing secure output and SHA-256 hash |
| `06_after_pylint.png` | Final Pylint run showing a perfect score of **10.00 / 10** |
| `07_after_bandit.png` | Final Bandit run showing **No issues identified** |
| `08_after_flake8.png` | Final Flake8 run showing **0 violations** (`--count` returns 0) |
| `09_git_log.png` | Git commit log showing the 3 distinct commits for the three tools |

---

## Reproduction Commands

To reproduce the environment and verify the deliverables:

```bash
# Setup virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
venv\Scripts\activate.bat
# On Linux/macOS:
source venv/bin/activate

# Install static analysis tools
pip install pylint bandit flake8

# Run baseline verification
pylint bank_account_system.py > reports/before/pylint_report.txt
bandit -r bank_account_system.py > reports/before/bandit_report.txt
flake8 bank_account_system.py > reports/before/flake8_report.txt

# Run fixed verification
pylint bank_account_system.py > reports/after/pylint_report.txt
bandit -r bank_account_system.py > reports/after/bandit_report.txt
flake8 bank_account_system.py > reports/after/flake8_report.txt
```

**Environment Used:** Python 3.13.14, Pylint 4.1.3, Bandit 1.9.4, Flake8 7.5.0 on Windows.
