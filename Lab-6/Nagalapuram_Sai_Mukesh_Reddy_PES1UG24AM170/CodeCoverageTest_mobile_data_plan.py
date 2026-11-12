"""Code (line) coverage tests for mobile_data_plan.py.

Each test runs statements the starter tests never reach, so every line of
the module executes at least once. This file only targets line coverage:
it leaves one branch untaken (overage_charge line 21, where extra > 10 but
the user is not roaming), which BranchCoverageTest_mobile_data_plan.py adds.
"""
import pytest
from mobile_data_plan import overage_charge, recharge_allowed, validity_status


# ---------- overage_charge ----------

def test_unknown_plan_raises_error():
    # Line 6: a plan missing from INCLUDED_GB is rejected
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_data_usage_raises_error():
    # Line 8: negative usage is rejected
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


def test_within_included_data_is_free():
    # Lines 13-14: usage inside the quota costs nothing
    assert overage_charge("standard", 3, False, False) == 0


def test_home_overage_uses_home_rate():
    # Lines 15, 17-18, 19, 23: 3 GB extra at the home rate of 15
    assert overage_charge("standard", 8, False, False) == 3 * 15


def test_loyal_roaming_heavy_user_pays_highest_rate():
    # Lines 10-11: loyal basic user gets 1 GB more (2 + 1 = 3 GB)
    # Line 16: roaming rate 40
    # Lines 20-22: more than 10 GB extra adds 10, roaming adds 5 more
    # 15 GB used - 3 GB included = 12 GB extra at 40 + 10 + 5 = 55
    assert overage_charge("basic", 15, True, True) == 12 * 55


# ---------- recharge_allowed ----------

def test_recharge_allowed():
    # Line 31: normal user with few pending recharges
    assert recharge_allowed(500, 1, False) is True


def test_recharge_with_kyc_pending_is_capped():
    # Line 28: KYC pending allows small recharges only
    assert recharge_allowed(150, 0, True) is True


def test_recharge_above_limit_is_rejected():
    # Line 30: amounts over 2000 are refused
    assert recharge_allowed(2500, 0, False) is False


# ---------- validity_status ----------

def test_prepaid_plan_with_addon_is_active():
    # Lines 35-36, 39-42: prepaid cutoff 0, addon makes it 2; 5 >= 2
    assert validity_status(5, True, True) == "active"


def test_postpaid_plan_in_grace_period():
    # Lines 37-38, 43-44: postpaid cutoff 3; 0 < 3 but 0 >= 3 - 15
    assert validity_status(0, False, False) == "grace"


def test_plan_expired_after_grace_period():
    # Line 45: prepaid cutoff 0; -20 < 0 - 15
    assert validity_status(-20, True, False) == "expired"
