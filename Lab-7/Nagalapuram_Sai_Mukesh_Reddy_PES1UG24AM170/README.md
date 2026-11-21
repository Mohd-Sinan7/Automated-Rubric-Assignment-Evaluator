# Lab 7: Fuzzing for Input Validation Bugs

**Student:** Nagalapuram Sai Mukesh Reddy (PES1UG24AM170)
**Assigned repository:** [`SETAPESU26/L6_L7_45_mobile_data_plan`](https://github.com/SETAPESU26/L6_L7_45_mobile_data_plan) (`Lab 7/`)
**Tools:** Python 3.11.9, Hypothesis 6.170.17, pytest 9.2.0

The assigned module `mobile_data_plan.py` has three functions that read user input:

| Function | Input | Output |
|---|---|---|
| `parse_plan(text)` | `"standard:5"` (plan name : data in GB) | `('Standard', 5.0)` |
| `usage_average(usage_csv)` | `"300,450,800"` (daily usage in MB) | `516` (whole MB) |
| `payable_bill(text)` | `"399\|50"` (bill \| discount) | `420.82` (bill + 18% GST - discount) |

The repository calls the files `mobile_data_plan.py` / `test_mobile_data_plan.py`. The handout calls
them `processor.py` / `test_processor.py`, so both names are included (same code; `test_processor.py`
only imports from `processor`).

## Files

| File | What it is |
|---|---|
| `PES1UG24AM170_Nagalapuram_Sai_Mukesh_Reddy_Lab7.pdf` | Lab report with all screenshots |
| `mobile_data_plan.py` | **Fixed** application (hardened against invalid input) |
| `processor.py` | Same fixed application, under the handout's file name |
| `mobile_data_plan_buggy.py` | Original application from the lab repository, unchanged, for comparison |
| `test_mobile_data_plan.py` | **Completed** Hypothesis fuzz tests (12 tests) |
| `test_processor.py` | Same tests, importing from `processor.py` |
| `screenshots/` | Console screenshots for steps 2, 4, 5 and 6, plus the git log |
| `reports/` | Plain-text copies of the same console output (full tracebacks in `02_...`) |

## Steps

1. **Install** - `pip install hypothesis` and `pip install pytest` (in a virtual environment).
2. **Run the buggy program** - `python mobile_data_plan.py`.
   Valid input works, but `premium:nan`, `300,-450,800` and `399|-50` are silently accepted
   (`nan` GB, a negative average, a discount that *raises* the bill to `520.8199999999999`), and
   `standard`, `300,,800` and `399` crash the program with a `ValueError`.
   Screenshots `01`-`03`.
3. **Complete the test file** - `test_mobile_data_plan.py` (see below).
4. **Run the tests on the buggy code** - `python -m pytest test_mobile_data_plan.py -v --tb=no -rf`:
   **11 failed, 1 passed**. The one passing test is the known-good-input check.
   Screenshots `04`-`05`, full log in `reports/02_hypothesis_fuzz_failing.txt`.
5. **Fix the program** and run it again - every bad input now gets a clear "Invalid input" message
   and the program carries on. Screenshot `06`.
6. **Re-run the tests on the fixed code** - `python -m pytest test_mobile_data_plan.py -v`:
   **12 passed**. Screenshot `07`.
   As an extra check every fuzz test was also run with up to 20,000 examples each; none failed.

## The fuzz tests

Hypothesis is set to 300 examples per test (default is 100) and to report one shrunk,
minimal failing input per test.

| Test | Strategy | Property checked |
|---|---|---|
| `test_parse_plan_no_crash` | `st.text() \| st.none()` | never raises |
| `test_usage_average_no_crash` | `st.text() \| st.none()` | never raises |
| `test_payable_bill_no_crash` | `st.text() \| st.none()` | never raises |
| `test_parse_plan_format_fuzz` | random name + `:`/`::`/nothing + number-like text | no crash; anything accepted has a non-blank name and finite GB >= 0 |
| `test_parse_plan_data_must_be_finite_and_not_negative` | `"standard:" + st.floats()` | `nan`, `inf`, negative GB are rejected; good values are returned exactly |
| `test_usage_average_matches_integer_mean` | `st.lists(st.integers())` joined by `,` | result is `sum // len`, between min and max; empty or negative usage is rejected |
| `test_usage_average_messy_csv` | lists of number-like text and empty fields | no crash; result is `None` or an `int >= 0` |
| `test_usage_average_huge_number` | 4301-6000 digit numbers | no crash (Python refuses `int()` on more than 4300 digits) |
| `test_payable_bill_amounts` | any two `st.floats()` | result is `None` or a finite `float >= 0` with at most 2 decimals; invalid amounts rejected; valid ones equal `round(max(bill*1.18 - discount, 0), 2)` |
| `test_payable_bill_discount_never_increases_bill` | bill and discount floats | metamorphic: bill with a discount <= bill with no discount |
| `test_payable_bill_wrong_number_of_fields` | 0, 1 or 3+ fields joined by `\|` | no crash, rejected |
| `test_known_good_inputs` | fixed examples | the fix keeps correct behaviour (`standard:5`, `300,450,800`, `399\|50` ...) |

## Bugs found by fuzzing

Running the same tests on the original code with `report_multiple_bugs=True` and 3000 examples
gives every distinct failure Hypothesis can find. Each row shows the minimal input it shrank to.

| # | Function | Failing input (Hypothesis's minimal example first) | Original behaviour |
|---|---|---|---|
| 1 | `parse_plan` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` |
| 2 | `parse_plan` | `''`, `'standard'` | `ValueError: not enough values to unpack` |
| 3 | `parse_plan` | `'::0.0'` | `ValueError: too many values to unpack` |
| 4 | `parse_plan` | `':'` | `ValueError: could not convert string to float: ''` |
| 5 | `parse_plan` | `':0.0'` | accepted an empty plan name `('', 0.0)` |
| 6 | `parse_plan` | `'standard:inf'`, `'standard:-1.0'`, `'premium:nan'` | accepted infinite / negative / NaN data |
| 7 | `usage_average` | `None` | `AttributeError` |
| 8 | `usage_average` | `''`, `'300,,800'` | `ValueError: invalid literal for int() with base 10: ''` |
| 9 | `usage_average` | `'9' * 4301` | `ValueError: Exceeds the limit (4300 digits) for integer string conversion` |
| 10 | `usage_average` | `'-1'`, `'300,-450,800'` | accepted negative usage (`-1`, `216`) |
| 11 | `payable_bill` | `None` | `AttributeError` |
| 12 | `payable_bill` | `''`, `'399'`, `'1\|2\|3'` | `ValueError: not enough / too many values to unpack` |
| 13 | `payable_bill` | `'\|'` | `ValueError: could not convert string to float: ''` |
| 14 | `payable_bill` | `'0.0\|-1.0'`, `'399\|-50'` | a negative discount *increased* the bill (`1.0`, `520.8199999999999`) |
| 15 | `payable_bill` | `'0.0\|nan'` | returned `nan` |
| 16 | `payable_bill` | `'0.0\|1.0'` | returned `int 0` instead of a float |
| 17 | `payable_bill` | `'1.0\|1.0'` | returned `0.17999999999999994` (not rounded to paise) |

## Fixes (defensive programming)

Every function now returns `None` for invalid input instead of raising, and `main()` prints a
helpful message when it gets `None`.

- **Type check first** - anything that is not a `str` (e.g. `None`) is rejected before `.split()`.
- **Exact separator count** - `parse_plan` needs exactly one `:`, `payable_bill` exactly one `|`,
  so unpacking can never fail.
- **Safe number parsing** - `_finite_number()` wraps `float()` in `try/except` and rejects `nan`,
  `inf` and overflow; `usage_average` wraps each `int()` in `try/except ValueError`, which also
  covers empty fields and the 4300-digit limit.
- **Range checks** - plan name must not be blank; GB, usage values, bill and discount must be `>= 0`.
- **Overflow check** - a bill like `1.6e308` that overflows to `inf` after GST is rejected.
- **Consistent money output** - `payable_bill` always returns a `float` rounded to 2 decimals and
  `0.0` (not `int 0`) when the discount covers the whole bill.
- **`main()`** - `input()` hitting end-of-file is treated as an empty answer instead of crashing.

## How to run

```powershell
python -m venv venv
venv\Scripts\activate
pip install hypothesis pytest
python mobile_data_plan_buggy.py           # original program
python mobile_data_plan.py                 # fixed program
python -m pytest test_mobile_data_plan.py -v
python -m pytest test_processor.py -v
```
