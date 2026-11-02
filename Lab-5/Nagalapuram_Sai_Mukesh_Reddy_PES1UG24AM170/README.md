# Lab 5: Static Code Analysis (Ticket Booking System, repo `SETAPESU26/L5_45_ticket_booking_system`)

I ran Pylint, Bandit and Flake8 on `ticket_booking_system.py`, documented the findings, and fixed all of them. I also fixed three problems that no tool reported.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.37/10 | **10.00/10** |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | No issues identified |
| Flake8 | 7 violations | 0 |

## Contents

| Path | Deliverable |
|------|-------------|
| `ticket_booking_system.py` | 1. The cleaned script (every reported issue fixed, not just four) |
| `issues.md` | 2. The issue table: tool code, type, lines, description and fix for each finding |
| `reflection.md` | 3. Answers to the four reflection questions |
| `reports/before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` for the original file |
| `reports/after/` | The same three reports for the fixed file. `flake8_report.txt` is empty because Flake8 prints nothing when there are no violations. |
| `screenshots/` | Terminal screenshots of each run (listed below) |

## Commits

One commit for each tool's fixes, as the handout asks. Each commit changes only this folder, so its diff shows exactly what that tool's fixes changed in `ticket_booking_system.py`.

```
a3df87f  Lab 5: add the original ticket_booking_system.py and baseline reports
cf939bd  Lab 5: fix all Bandit findings
29ce248  Lab 5: fix all Flake8 findings
515372a  Lab 5: fix all Pylint findings (5.37 -> 10.00/10)
40e9ab7  Lab 5: fix problems none of the three tools flagged
```

A final commit after these adds this README, `issues.md`, `reflection.md`, `reports/after/` and the screenshots.

## Screenshots

These were taken in my clone of the lab repo, so the commit hashes in `01`, `05` and `09` come from that clone, not from this repo.

| File | Shows |
|------|-------|
| `01_before_program_run.png` | The original code running and printing the box office secret |
| `02_before_pylint.png` | Pylint on the original code: 25 messages, 5.37/10 |
| `03a_before_bandit_top.png`, `03b_before_bandit_end.png` | Bandit on the original code: 5 issues (2 High, 1 Medium, 2 Low). The output is taller than the screen, so it is split into the start and the end. |
| `04_before_flake8.png` | Flake8 on the original code: 7 violations |
| `05_after_program_run.png` | The fixed code running, plus the new seating chart file |
| `06_after_pylint.png` | Pylint on the fixed code: 10.00/10 (previous run 5.37, +4.63) |
| `07_after_bandit.png` | Bandit on the fixed code: No issues identified |
| `08_after_flake8.png` | Flake8 on the fixed code: no output, `--count` prints 0 |
| `09_git_log.png` | The commit history in my clone of the lab repo |

## Reproduce

```bash
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install pylint bandit flake8
python ticket_booking_system.py
pylint ticket_booking_system.py > pylint_report.txt
bandit -r ticket_booking_system.py > bandit_report.txt
flake8 ticket_booking_system.py > flake8_report.txt
```

Versions used: Python 3.11.9, Pylint 4.1.3, Bandit 1.9.4, Flake8 7.5.0.
