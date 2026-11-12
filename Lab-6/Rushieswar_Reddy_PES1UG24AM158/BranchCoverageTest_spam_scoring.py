"""Branch coverage tests for spam_scoring.py.

Covers every statement (39/39, 100%) and every decision branch (26/26, 100%,
0 partial) including all boundary values, compound boolean conditions, and
the `17->19` branch missed by CodeCoverageTest_spam_scoring.py.
"""
import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------- score_message: text & word branches ----------

def test_score_empty_text():
    # Loop `for word in text.split()` executes 0 times (6->11)
    assert score_message("", False, 0) == 0


@pytest.mark.parametrize(
    "word",
    ["free", "winner", "prize", "urgent", "cash", "FREE!", "Winner.", "Prize,", "!urgent."],
)
def test_score_all_spam_words_case_and_punctuation(word):
    # Line 7 True -> Line 8: all SPAM_WORDS with case folding and .strip("!.,")
    assert score_message(word, False, 0) == 2


def test_score_short_uppercase_not_penalized():
    # Line 9 compound condition: word.isupper() True, len(word) > 3 False (<= 3 chars)
    assert score_message("BUY NOW OK", False, 0) == 0


def test_score_mixed_case_not_penalized():
    # Line 9 compound condition: word.isupper() False, len(word) > 3 True
    assert score_message("Offer Deal Hello", False, 0) == 0


def test_score_long_uppercase_adds_one_per_word():
    # Line 9 True -> Line 10: length == 4 ("SALE") and > 4 ("OFFER")
    assert score_message("SALE OFFER", False, 0) == 2


def test_score_combines_spam_uppercase_and_plain_words():
    # Covers 7->8 (spam), 9->10 (uppercase >3), and 9->6 (plain/short word) in one loop
    assert score_message("hello URGENT BUY OFFER", False, 0) == 3


# ---------- score_message: link_count boundaries ----------

@pytest.mark.parametrize(
    ("link_count", "expected"),
    [
        (0, 0),   # 11->13 False, 13->15 False
        (1, 1),   # 11->13 False, 13->14 True
        (3, 1),   # boundary: 3 is not > 3, so takes 13->14
        (4, 4),   # boundary: 4 > 3 takes 11->12
    ],
)
def test_score_link_count_boundaries(link_count, expected):
    assert score_message("hello", False, link_count) == expected


# ---------- score_message: sender_known & clamping ----------

def test_known_sender_clamps_when_initial_score_below_three():
    # Line 15 True, Line 17 True -> Line 18: 2 - 3 = -1 -> clamped to 0
    assert score_message("free", True, 0) == 0


def test_known_sender_exact_three_does_not_trigger_negative_clamp():
    # Line 15 True, Line 17 False (17->19): 3 - 3 = 0, score < 0 is False
    assert score_message("free", True, 1) == 0


def test_known_sender_above_three_keeps_positive_remainder():
    # Line 15 True, Line 17 False (17->19): (2 + 4) - 3 = 3
    assert score_message("free", True, 4) == 3


def test_unknown_sender_skips_deduction():
    # Line 15 False (15->19): score stays 2
    assert score_message("free", False, 0) == 2


# ---------- classify: threshold boundaries ----------

@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0, "clean"),
        (3, "clean"),       # boundary just below suspicious (4)
        (4, "suspicious"),  # exact boundary for suspicious
        (7, "suspicious"),  # boundary just below spam (8)
        (8, "spam"),        # exact boundary for spam
        (12, "spam"),
    ],
)
def test_classify_boundaries(score, expected):
    assert classify(score) == expected


# ---------- filter_inbox ----------

def test_filter_inbox_empty():
    # Loop `for text, known, links in messages:` runs 0 times (32->35)
    assert filter_inbox([]) == {"spam": 0, "suspicious": 0, "clean": 0}


def test_filter_inbox_mixed_messages():
    messages = [
        ("free cash winner", False, 4),   # 2+2+2+4 = 10 -> spam
        ("URGENT OFFER", False, 2),       # 2+1+1 = 4 -> suspicious
        ("free prize", True, 1),          # 2+2+1-3 = 2 -> clean
        ("lunch at noon?", True, 0),      # 0-3 -> 0 -> clean
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 2}


# ---------- inbox_status: ratio boundaries ----------

def test_inbox_status_empty():
    # Line 40 True -> Line 41
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


@pytest.mark.parametrize(
    ("counts", "expected"),
    [
        ({"spam": 0, "suspicious": 2, "clean": 3}, "healthy"),  # ratio = 0.0
        ({"spam": 1, "suspicious": 1, "clean": 3}, "healthy"),  # boundary ratio == 0.2 (not > 0.2)
        ({"spam": 1, "suspicious": 0, "clean": 3}, "noisy"),    # ratio = 0.25 (> 0.2, <= 0.5)
        ({"spam": 1, "suspicious": 1, "clean": 0}, "noisy"),    # boundary ratio == 0.5 (not > 0.5)
        ({"spam": 3, "suspicious": 1, "clean": 1}, "flooded"),  # ratio = 0.6 (> 0.5)
        ({"spam": 1, "suspicious": 0, "clean": 0}, "flooded"),  # ratio = 1.0 (> 0.5)
    ],
)
def test_inbox_status_ratio_boundaries(counts, expected):
    assert inbox_status(counts) == expected
