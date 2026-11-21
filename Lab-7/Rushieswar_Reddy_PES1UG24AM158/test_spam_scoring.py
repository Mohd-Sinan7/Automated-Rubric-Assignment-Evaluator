"""
Lab 7: Fuzzing for Input Validation Bugs using Hypothesis
Tests for spam_scoring module.
"""

from hypothesis import given, strategies as st
from spam_scoring import sender_domain, first_link, shout_ratio

# --- Core Fuzz Tests (No-Crash Guarantees) ---

@given(st.text() | st.none())
def test_sender_domain_no_crash(s):
    try:
        sender_domain(s)
    except Exception as e:
        assert False, f"sender_domain crashed with: {e}"

@given(st.text() | st.none())
def test_first_link_no_crash(s):
    try:
        first_link(s)
    except Exception as e:
        assert False, f"first_link crashed with: {e}"

@given(st.text() | st.none())
def test_shout_ratio_no_crash(s):
    try:
        shout_ratio(s)
    except Exception as e:
        assert False, f"shout_ratio crashed with: {e}"

# --- Property-Based Invariant Tests ---

@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(), st.booleans()))
def test_sender_domain_properties(val):
    """Domain should always be a lowercased string and never raise."""
    domain = sender_domain(val)
    assert isinstance(domain, str)
    assert domain == domain.lower()

@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(), st.booleans()))
def test_first_link_properties(val):
    """Extracted link should be string starting with 'http' and contain no space."""
    link = first_link(val)
    assert isinstance(link, str)
    if link:
        assert link.startswith("http")
        assert " " not in link

@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(), st.booleans()))
def test_shout_ratio_bounds(val):
    """Shout ratio must always be a float between 0.0 and 1.0 inclusive."""
    ratio = shout_ratio(val)
    assert isinstance(ratio, float)
    assert 0.0 <= ratio <= 1.0

# --- Functional Correctness / Known Cases ---

def test_sender_domain_known_cases():
    assert sender_domain("offers@Deals.com") == "deals.com"
    assert sender_domain("user@sub.domain.org") == "sub.domain.org"
    assert sender_domain("invalid-email") == ""
    assert sender_domain("") == ""
    assert sender_domain(None) == ""

def test_first_link_known_cases():
    assert first_link("Check https://example.com for deals") == "https://example.com"
    assert first_link("Visit http://test.org now") == "http://test.org"
    assert first_link("No links here") == ""
    assert first_link("") == ""
    assert first_link(None) == ""

def test_shout_ratio_known_cases():
    assert round(shout_ratio("FREE prize NOW"), 4) == round(7 / 12, 4)
    assert shout_ratio("hello") == 0.0
    assert shout_ratio("HELLO") == 1.0
    assert shout_ratio("12345!@#$") == 0.0
    assert shout_ratio("") == 0.0
    assert shout_ratio(None) == 0.0
