# Lab 7: Fuzzing for Input Validation Bugs (Ride Share Fare)

**Student:** Mohammed Sinan (PES1UG24AM165)  
**Assigned Repository:** [`SETAPESU26/L6_L7_40_ride_share_fare/Lab 7`](https://github.com/SETAPESU26/L6_L7_40_ride_share_fare/tree/main/Lab%207)  
**Course:** Software Engineering (UE24CS341A) — 5th Semester  
**Module:** Automated Rubric Assignment Evaluator  

---

## 1. Executive Summary

This lab explores **fuzz testing (property-based testing)** as a dynamic quality assurance and security technique using Python's **Hypothesis** library. Unlike standard example-based tests that only evaluate anticipated scenarios, fuzz testing automatically generates hundreds of randomized, malformed, empty, and boundary inputs to aggressively uncover unhandled exceptions, type errors, buffer issues, and input validation vulnerabilities.

### Key Outcomes:
- **Bug Discovery via Hypothesis:** Successfully uncovered 3 critical exception groups across all three functions (`parse_trip`, `fare_average`, `payable_fare`) resulting in `AttributeError`, `ValueError`, and `ZeroDivisionError`.
- **Defensive Hardening:** Refactored the core application `ride_share_fare.py` using defensive programming techniques to guarantee that no unhandled exceptions are raised on any malformed input.
- **100% Test Pass Rate:** Verified with Hypothesis property-based fuzz tests and deterministic edge-case tests, achieving 100% pass rate across 9 comprehensive test suites.

---

## 2. Fuzz Testing Findings & Root Cause Analysis

When fuzzed with `@given(st.text() | st.none())`, the initial `ride_share_fare.py` application crashed immediately:

| Function | Falsifying Input (Minimized by Hypothesis) | Exception Triggered | Underlying Bug & Root Cause |
|---|---|---|---|
| `parse_trip(text)` | `s = None` | `AttributeError: 'NoneType' object has no attribute 'split'` | No type checking before calling string methods. |
| `parse_trip(text)` | `s = ''` | `ValueError: not enough values to unpack (expected 2, got 1)` | Direct unpacking `cab, km = text.split(':')` assumes delimiter always exists. |
| `parse_trip(text)` | `s = ':'` | `ValueError: could not convert string to float: ''` | Unchecked float conversion on empty distance string. |
| `fare_average(csv)` | `s = None` | `AttributeError: 'NoneType' object has no attribute 'split'` | Unhandled `None` input. |
| `fare_average(csv)` | `s = ''` | `ValueError: invalid literal for int() with base 10: ''` | List comprehension `int(r)` on empty string slice. |
| `fare_average(csv)` | `s = ',,'` | `ZeroDivisionError: integer division by zero` | Empty list of parsed fares causes division by zero. |
| `payable_fare(text)` | `s = None` | `AttributeError: 'NoneType' object has no attribute 'split'` | Unhandled `None` input. |
| `payable_fare(text)` | `s = '|'` | `ValueError: could not convert string to float: ''` | Missing numeric values on either side of pipe. |
| `payable_fare(text)` | `s = '250|abc'` | `ValueError: could not convert string to float` | Non-numeric promo code string passed to `float()`. |

---

## 3. Defensive Programming & Hardening Strategy

The application was systematically hardened:
1. **Type & Null Safeguards:** Validate that incoming arguments are non-null and instances of `str`.
2. **Delimiter Presence & Count Validation:** Verify that expected delimiters (`:`, `|`) occur exactly once before attempting tuple unpacking.
3. **Safe Numeric Conversion:** Wrap `float()` and `int()` conversions inside defensive `try...except (ValueError, TypeError)` blocks.
4. **Boundary & Sanitization Checks:** 
   - Strip leading and trailing whitespace.
   - Guard against negative distances and fares (`km >= 0`, `fare >= 0`, `promo >= 0`).
   - Guard against non-finite floating point numbers (`math.isnan()`, `math.isinf()`).
5. **Predictable Fallbacks:** Return safe, well-defined default values (`None` for invalid trips, `0` for empty fare averages, `0.0` for invalid payable fares) without raising unhandled exceptions.

---

## 4. Directory Contents & Deliverables

| Deliverable Path | Description | Handout Requirement |
|---|---|---|
| `Lab7_Fuzz_Testing_Mohammed_Sinan_PES1UG24AM165.pdf` | Formatted PDF document compiling all execution steps, edge cases, and screenshots | **Deliverable 1** |
| `ride_share_fare.py` | Fixed and hardened application Python script | **Deliverable 2** |
| `test_ride_share_fare.py` | Updated Hypothesis test suite with fuzz tests, property tests, and unit tests | **Deliverable 3** |
| `reports/failing_tests_report.txt` | Pytest output showing Hypothesis uncovering initial crashes | Verification Report |
| `reports/passing_tests_report.txt` | Pytest output showing 9/9 tests passing on the hardened script | Verification Report |
| `screenshots/` | High-resolution terminal capture screenshots: | Step Screenshots |
| ↳ `01_buggy_program_run.png` | Step 2: Running initial buggy application | Required SS |
| ↳ `02_failing_tests.png` | Step 4: Running Hypothesis tests showing failures | Required SS |
| ↳ `03_fixed_program_run.png` | Step 5: Running hardened application | Required SS |
| ↳ `04_passing_tests.png` | Step 6: Running Hypothesis tests showing 100% pass | Required SS |
| ↳ `05_git_log.png` | Commit history showing step-by-step development | Version Control |

---

## 5. Reproduction & Verification Commands

```bash
# 1. Install dependencies
pip install hypothesis pytest

# 2. Run the hardened application
python ride_share_fare.py

# 3. Run the complete Hypothesis fuzz and unit test suite
pytest test_ride_share_fare.py -v
```
