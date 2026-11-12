# Lab 6: Code and Branch Coverage (Mobile Data Plan, repo `SETAPESU26/L6_L7_45_mobile_data_plan`)

I measured the line and branch coverage of the starter tests for `mobile_data_plan.py`, then wrote two test files: one that reaches 100% line coverage, and one that reaches 100% branch coverage.

| Test file | Tests | Line coverage | Branch coverage | Missing |
|-----------|-------|---------------|-----------------|---------|
| `test_mobile_data_plan.py` (starter) | 2 | 38% (14/37) | 32% | lines 6, 8, 11, 15-23, 28, 30, 35-45 |
| `CodeCoverageTest_mobile_data_plan.py` | 11 | **100%** (37/37) | 98% (1 partial) | branch `21->23` |
| `BranchCoverageTest_mobile_data_plan.py` | 58 | **100%** (37/37) | **100%** (26/26) | nothing |

The percentages are for `mobile_data_plan.py`. `coverage report` also lists the test file itself, which is always 100% because every test function runs.

## Contents

| Path | Deliverable |
|------|-------------|
| `mobile_data_plan.py` | The module under test, unchanged from the lab repo |
| `test_mobile_data_plan.py` | The starter test file, unchanged (used for the baseline) |
| `CodeCoverageTest_mobile_data_plan.py` | Test cases for code (line) coverage |
| `BranchCoverageTest_mobile_data_plan.py` | Test cases for branch coverage |
| `screenshots/` | Terminal output of the coverage runs (listed below) |
| `reports/` | The same runs as text, plus the starter baseline (`baseline_line.txt`, `baseline_branch.txt`) |

The handout asks for screenshots only of results at 90% or more, so the 38% baseline is kept as text in `reports/` and not as a screenshot.

## Code coverage

`CodeCoverageTest_mobile_data_plan.py` adds one test for each group of lines the starter tests never ran:

| Function | Test | Lines it reaches |
|----------|------|------------------|
| `overage_charge` | unknown plan `"gold"` raises `ValueError` | 6 |
| | negative usage raises `ValueError` | 8 |
| | `standard`, 8 GB, home: 3 GB extra at rate 15 | 15, 17-19, 23 |
| | loyal `basic`, 15 GB, roaming: 12 GB extra at 40 + 10 + 5 | 10-11, 16, 20-22 |
| `recharge_allowed` | KYC pending, amount 150 | 28 |
| | amount 2500 is refused | 30 |
| `validity_status` | prepaid with add-on, 5 days left: `"active"` | 35-36, 39-42 |
| | postpaid, 0 days left: `"grace"` | 37-38, 43-44 |
| | prepaid, -20 days left: `"expired"` | 45 |

Every statement now runs (37/37, 100%). Running the same tests with `--branch` gives 98%, with one partial branch: `21->23`. This is the gap between line and branch coverage from the handout. Line 22 (`rate += 5`) runs, so line coverage is complete, but no test reaches line 21 with `is_roaming` False. That path is a heavy home user (more than 10 GB extra, not roaming), who should pay 15 + 10 = 25 per GB.

## Branch coverage

`coverage.py` counts 26 branches: 13 decisions (lines 5, 7, 10, 13, 15, 19, 21, 27, 29, 35, 39, 41, 43), each with a True and a False outcome. `BranchCoverageTest_mobile_data_plan.py` takes every one of them, including the missed `21->23`, and tests both sides of each boundary:

- **`overage_charge`**: unknown plans (`"gold"`, `"Basic"`, `""`, `None`) and negative usage raise errors, and the plan is checked before the usage. Usage exactly at the quota is free and just over it is charged. All four rate cases are covered: home 15, home heavy 25, roaming 40, roaming heavy 55. Each heavy case is checked at exactly 10 GB extra (not heavy) and 11 GB extra (heavy).
- **Line 10, `is_loyal and plan != "premium"`**: branch coverage only sees the line's overall True or False, so I tested both ways it can be False: a non-loyal user, and a loyal user on `premium`, who gets no bonus GB.
- **`recharge_allowed`**: with KYC pending, 200 is allowed and 201 is not, whatever the pending count. Without KYC, 2000 is allowed and 2001 is not. 2 pending recharges are allowed and 3 are not.
- **`validity_status`**: all four combinations of prepaid/postpaid and add-on/no add-on, which give cutoffs 0, 2, 3 and 5. For each cutoff, the test checks `cutoff` (active), `cutoff - 1` and `cutoff - 15` (grace), and `cutoff - 16` (expired).

All 58 tests pass. Line and branch coverage of `mobile_data_plan.py` are both 100%.

## Commits

One commit for each coverage stage, as the handout asks. Each commit adds the test file with its screenshots and reports:

```
807de6e  Lab 6: add code coverage test cases (100% line coverage)
9c5aec4  Lab 6: add branch coverage test cases (100% branch coverage)
```

A final commit adds this README and `04_git_log.png`.

## Screenshots

| File | Shows |
|------|-------|
| `01_code_coverage_line.png` | `coverage run -m pytest CodeCoverageTest_mobile_data_plan.py` and `coverage report -m`: 11 passed, 100% line coverage |
| `02_code_coverage_branch.png` | The same tests with `--branch`: 98%, partial branch `21->23` |
| `03_branch_coverage_branch.png` | `coverage run --branch -m pytest BranchCoverageTest_mobile_data_plan.py` and `coverage report -m`: 58 passed, 100% (26/26 branches, 0 partial) |
| `04_git_log.png` | The two Lab 6 commits for this folder, with the files each one added |

## Reproduce

```bash
pip install coverage pytest

coverage run -m pytest CodeCoverageTest_mobile_data_plan.py
coverage report -m
coverage run --branch -m pytest CodeCoverageTest_mobile_data_plan.py
coverage report -m

coverage run --branch -m pytest BranchCoverageTest_mobile_data_plan.py
coverage report -m
```

Run these from this folder. Python 3.11.9, coverage 7.17.2, pytest 9.2.0, Windows 11.
