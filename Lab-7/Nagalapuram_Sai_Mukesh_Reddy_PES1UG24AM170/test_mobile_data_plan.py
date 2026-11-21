"""
Lab 7 - Fuzzing for Input Validation Bugs
Property-based fuzz tests for mobile_data_plan.py using Hypothesis.

Part A  - the three starter tests: any text (or None) must never crash a function.
Part B  - structured fuzzing: inputs that look almost valid ("plan:gb", CSV numbers,
          "bill|discount") so the fuzzer gets past split() and reaches the number
          parsing and the arithmetic, where the quieter bugs live.
Part C  - a few known-good inputs, so the fixes do not change correct behaviour.
"""
import math

from hypothesis import given, settings, strategies as st

from mobile_data_plan import parse_plan, usage_average, payable_bill

# More examples than the default 100, no deadline (slow machines don't flake), and one
# minimal falsifying example per test so every failure reads as a single line.
settings.register_profile("lab7", max_examples=300, deadline=None, report_multiple_bugs=False)
settings.load_profile("lab7")

# Strings that are sometimes valid numbers and sometimes not.
number_text = st.one_of(
    st.floats().map(repr),                      # 1.5, -0.0, nan, inf, -inf, 1e+308 ...
    st.integers().map(str),                     # 0, -7, 123456789 ...
    st.sampled_from(["", " ", "abc", "1e400", "NaN", "-inf", "1_000", "٣"]),
    st.text(max_size=8),
)


def short(value, limit=40):
    """repr() of a value, cut down so a 5000-character input doesn't flood the report."""
    text = repr(value)
    return text if len(text) <= limit else f"{text[:limit]}...<{len(value)} chars>"


def call(func, arg):
    """Call func(arg); any exception means the fuzzer found a crash."""
    try:
        return func(arg)
    except Exception as e:
        message = str(e).split(":")[0]
        raise AssertionError(f"{func.__name__}({short(arg)}) crashed with {type(e).__name__}: {message}") from None


# --------------------------------------------------------------------------
# Part A: starter tests - random text or None must not crash
# --------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_plan_no_crash(s):
    try:
        parse_plan(s)
    except Exception as e:
        assert False, f"parse_plan({s!r}) crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_usage_average_no_crash(s):
    try:
        usage_average(s)
    except Exception as e:
        assert False, f"usage_average({s!r}) crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill({s!r}) crashed with: {type(e).__name__}: {e}"


# --------------------------------------------------------------------------
# Part B: structured fuzzing
# --------------------------------------------------------------------------

@given(plan=st.text(max_size=12), sep=st.sampled_from([":", "::", ""]), gb=number_text)
def test_parse_plan_format_fuzz(plan, sep, gb):
    """Almost-valid 'plan:gb' strings: no crash, and anything accepted must be sane."""
    text = f"{plan}{sep}{gb}"
    result = call(parse_plan, text)
    if result is not None:
        name, data_gb = result
        assert isinstance(name, str) and name.strip(), f"parse_plan({text!r}) accepted an empty plan name"
        assert isinstance(data_gb, float)
        assert math.isfinite(data_gb) and data_gb >= 0, f"parse_plan({text!r}) accepted data_gb={data_gb}"


@given(gb=st.floats())
def test_parse_plan_data_must_be_finite_and_not_negative(gb):
    """A well-formed plan with nan / inf / negative GB has to be rejected (None)."""
    text = f"standard:{gb!r}"
    result = call(parse_plan, text)
    if math.isfinite(gb) and gb >= 0:
        assert result == ("Standard", gb)
    else:
        assert result is None, f"parse_plan({text!r}) returned {result} instead of None"


@given(st.lists(st.integers(min_value=-10**6, max_value=10**6), max_size=30))
def test_usage_average_matches_integer_mean(values):
    """CSV of integers: average must equal sum // len; empty or negative usage is rejected."""
    text = ",".join(map(str, values))
    result = call(usage_average, text)
    if not values or min(values) < 0:
        assert result is None, f"usage_average({text!r}) returned {result} instead of None"
    else:
        assert result == sum(values) // len(values)
        assert min(values) <= result <= max(values)


@given(st.lists(number_text | st.just(""), min_size=1, max_size=10))
def test_usage_average_messy_csv(tokens):
    """Empty fields, spaces, words, floats, nan ... in the CSV: no crash, result None or int >= 0."""
    text = ",".join(tokens)
    result = call(usage_average, text)
    assert result is None or (isinstance(result, int) and result >= 0), \
        f"usage_average({text!r}) returned {result!r}"


@given(st.integers(min_value=4301, max_value=6000))
def test_usage_average_huge_number(digits):
    """Python refuses int() on strings longer than 4300 digits - that must not crash the app."""
    call(usage_average, "9" * digits)


@given(bill=st.floats(), discount=st.floats())
def test_payable_bill_amounts(bill, discount):
    """Any float pair: the bill is a finite, non-negative amount in rupees, or the input is rejected."""
    text = f"{bill!r}|{discount!r}"
    result = call(payable_bill, text)
    if result is not None:
        assert isinstance(result, float), f"payable_bill({text!r}) returned {type(result).__name__} {result!r}"
        assert math.isfinite(result) and result >= 0, f"payable_bill({text!r}) returned {result}"
        assert round(result, 2) == result, f"payable_bill({text!r}) returned {result} (more than 2 decimals)"
    if not (math.isfinite(bill) and math.isfinite(discount)) or bill < 0 or discount < 0:
        assert result is None, f"payable_bill({text!r}) returned {result} instead of None"
    elif math.isfinite(bill * 1.18):
        assert result == round(max(bill * 1.18 - discount, 0.0), 2)


@given(bill=st.floats(min_value=0, max_value=1e6),
       discount=st.floats(min_value=-1e6, max_value=1e6))
def test_payable_bill_discount_never_increases_bill(bill, discount):
    """Metamorphic property: applying a discount can never make the bill bigger."""
    with_discount = call(payable_bill, f"{bill!r}|{discount!r}")
    without_discount = call(payable_bill, f"{bill!r}|0")
    if with_discount is not None:
        assert with_discount <= without_discount, \
            f"payable_bill('{bill!r}|{discount!r}') = {with_discount} > {without_discount} with no discount"


@given(st.lists(st.floats(min_value=0, max_value=1e6).map(repr), max_size=5).filter(lambda p: len(p) != 2))
def test_payable_bill_wrong_number_of_fields(parts):
    """Zero, one or three+ fields around '|': no crash, rejected."""
    text = "|".join(parts)
    result = call(payable_bill, text)
    assert result is None, f"payable_bill({text!r}) returned {result} instead of None"


# --------------------------------------------------------------------------
# Part C: known-good inputs keep working
# --------------------------------------------------------------------------

def test_known_good_inputs():
    assert parse_plan("standard:5") == ("Standard", 5.0)
    assert parse_plan("  premium plus : 12.5 ") == ("Premium Plus", 12.5)
    assert usage_average("300,450,800") == 516
    assert usage_average(" 300, 450 ,800 ") == 516
    assert payable_bill("399|50") == 420.82
    assert payable_bill("100|500") == 0.0
