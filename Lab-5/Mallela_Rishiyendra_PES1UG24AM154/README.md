# Lab 5: Static Code Analysis – Digital Wallet & Payment Tracker

**Student:** Rishyendra M (PES1UG24AM154) – Section C, AIML
**Assigned repository:** [SETAPESU26/L5_29_digital_wallet](https://github.com/SETAPESU26/L5_29_digital_wallet)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.69/10 (25 messages) | **10.00/10** |
| Bandit | 4 issues (High 1, Medium 1, Low 2) | **0 issues** |
| Flake8 | 4 issues | **0 issues** |

## Contents

| Path | Description |
|------|-------------|
| `digital_wallet.py` | Cleaned, fixed script |
| `issues.md` | Issue table (12 issues, high/medium severity first) |
| `reflection.md` | Answers to the reflection questions |
| `reports/before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`, program output before fixes |
| `reports/after/` | Same reports after fixes |
| `screenshots/` | Terminal screenshots before/after for program run and each tool, plus git log |

## Commits

1. Original script + baseline reports
2. Fix Bandit issues (security)
3. Fix Pylint issues (quality)
4. Fix Flake8 issues (style) + after reports, issue table and reflection

## How to reproduce

```
python digital_wallet.py
python -m pylint digital_wallet.py > pylint_report.txt
python -m bandit -r digital_wallet.py > bandit_report.txt
python -m flake8 digital_wallet.py > flake8_report.txt
```
