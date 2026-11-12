"""Code (line) coverage tests for spam_scoring.py.

Each test exercises statements that the starter test suite does not reach so
that every statement in spam_scoring.py executes at least once (100% line
coverage). This suite intentionally targets statement coverage only and leaves
the False branch of `if score < 0:` (line 17 -> line 19, where a known sender's
score remains non-negative after the -3 adjustment) untested, which
BranchCoverageTest_spam_scoring.py covers.
"""
from spam_scoring import score_message, classify, filter_inbox, inbox_status


# ---------- score_message ----------

def test_plain_message_scores_zero():
    # Lines 5-7, 9, 11, 13, 15, 19: plain words, unknown sender, zero links
    assert score_message("hello there", False, 0) == 0


def test_spam_words_and_many_links():
    # Lines 7-8, 11-12: spam words (+2 each) and link_count > 3 (+4)
    assert score_message("Claim your free prize!", False, 4) == 8


def test_uppercase_word_and_few_links():
    # Lines 9-10, 13-14: uppercase word > 3 chars (+1) and 1 <= link_count <= 3 (+1)
    assert score_message("SPECIAL OFFER", False, 2) == 3


def test_known_sender_clamps_negative_score_to_zero():
    # Lines 15-18: known sender deducts 3, clamping negative score (1 - 3 = -2) to 0
    assert score_message("hello", True, 1) == 0


# ---------- classify ----------

def test_classify_all_categories():
    # Lines 23-27: all three classification return paths
    assert classify(10) == "spam"
    assert classify(5) == "suspicious"
    assert classify(1) == "clean"


# ---------- filter_inbox ----------

def test_filter_inbox_counts_messages():
    # Lines 31-35: iterates through messages and aggregates label counts
    messages = [
        ("free cash winner", False, 4),
        ("URGENT OFFER", False, 2),
        ("see you soon", False, 0),
    ]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


# ---------- inbox_status ----------

def test_inbox_status_empty():
    # Lines 39-41: total == 0 returns "empty"
    assert inbox_status({"spam": 0, "suspicious": 0, "clean": 0}) == "empty"


def test_inbox_status_flooded():
    # Lines 42-44: spam ratio > 0.5 returns "flooded"
    assert inbox_status({"spam": 3, "suspicious": 0, "clean": 1}) == "flooded"


def test_inbox_status_noisy():
    # Lines 45-46: 0.2 < spam ratio <= 0.5 returns "noisy"
    assert inbox_status({"spam": 1, "suspicious": 0, "clean": 2}) == "noisy"


def test_inbox_status_healthy():
    # Line 47: spam ratio <= 0.2 returns "healthy"
    assert inbox_status({"spam": 0, "suspicious": 1, "clean": 4}) == "healthy"
