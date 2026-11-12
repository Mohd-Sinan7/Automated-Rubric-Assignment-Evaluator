"""Branch coverage tests for mobile_data_plan.py.

Every if / elif / else decision is driven both ways, including the branch the
line coverage suite leaves untaken (line 21 False: extra > 10 while not
roaming). Boundary values are tested on each side of every comparison, and
both parts of the compound condition on line 10 are tested separately.
"""
import pytest
from mobile_data_plan import (
    INCLUDED_GB,
    overage_charge,
    recharge_allowed,
    validity_status,
)


# =====================================================================
# overage_charge(plan, data_gb, is_roaming, is_loyal)
# =====================================================================

# ---- Line 5: plan not in INCLUDED_GB (True -> raise, False -> continue) ----

@pytest.mark.parametrize("plan", ["gold", "Basic", "", None])
def test_unknown_plan_raises_error(plan):
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge(plan, 5, False, False)


@pytest.mark.parametrize("plan", ["basic", "standard", "premium"])
def test_every_known_plan_is_accepted(plan):
    assert overage_charge(plan, 0, False, False) == 0


# ---- Line 7: data_gb < 0 (True -> raise, False -> continue) ----

@pytest.mark.parametrize("data_gb", [-1, -0.5, -100])
def test_negative_data_usage_raises_error(data_gb):
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", data_gb, False, False)


def test_plan_is_checked_before_data_usage():
    # Both inputs are bad: the plan check on line 5 runs first
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", -1, False, False)


def test_zero_data_usage_is_valid():
    assert overage_charge("premium", 0, True, True) == 0


# ---- Line 10: is_loyal and plan != "premium" ----

@pytest.mark.parametrize("plan", ["basic", "standard"])
def test_loyal_user_on_non_premium_plan_gets_bonus_gb(plan):
    # True: one extra GB, so usage of included + 1 is still free
    bonus_quota = INCLUDED_GB[plan] + 1
    assert overage_charge(plan, bonus_quota, False, True) == 0
    assert overage_charge(plan, bonus_quota + 1, False, True) == 15


def test_loyal_user_on_premium_plan_gets_no_bonus_gb():
    # False because plan == "premium" (is_loyal is True)
    assert overage_charge("premium", 11, False, True) == 1 * 15


@pytest.mark.parametrize("plan", ["basic", "standard", "premium"])
def test_non_loyal_user_gets_no_bonus_gb(plan):
    # False because is_loyal is False
    quota = INCLUDED_GB[plan]
    assert overage_charge(plan, quota + 1, False, False) == 1 * 15


# ---- Line 13: extra <= 0 (True -> return 0, False -> charge) ----

@pytest.mark.parametrize(
    "plan, data_gb",
    [("basic", 1), ("basic", 2), ("standard", 5), ("premium", 10)],
)
def test_usage_up_to_quota_is_free(plan, data_gb):
    assert overage_charge(plan, data_gb, True, False) == 0


def test_usage_just_over_quota_is_charged():
    assert overage_charge("basic", 2.5, False, False) == pytest.approx(0.5 * 15)


# ---- Lines 15 and 19-21: rate selection ----
#   is_roaming  extra > 10   rate
#   False       False        15
#   False       True         15 + 10      = 25   (line 21 False -> 23)
#   True        False        40
#   True        True         40 + 10 + 5  = 55   (line 21 True -> 22)

def test_home_user_small_overage_rate_15():
    assert overage_charge("standard", 8, False, False) == 3 * 15


def test_home_user_exactly_10_gb_extra_stays_at_rate_15():
    # Boundary: extra == 10 is not > 10
    assert overage_charge("standard", 15, False, False) == 10 * 15


def test_home_user_heavy_overage_rate_25():
    # extra > 10 and not roaming: the branch the line coverage suite missed
    assert overage_charge("standard", 16, False, False) == 11 * 25


def test_roaming_user_small_overage_rate_40():
    assert overage_charge("premium", 12, True, False) == 2 * 40


def test_roaming_user_exactly_10_gb_extra_stays_at_rate_40():
    assert overage_charge("premium", 20, True, False) == 10 * 40


def test_roaming_user_heavy_overage_rate_55():
    assert overage_charge("premium", 21, True, False) == 11 * 55


def test_loyal_roaming_heavy_user():
    # Loyalty bonus and the highest rate together: 15 - (2 + 1) = 12 GB extra
    assert overage_charge("basic", 15, True, True) == 12 * 55


def test_loyal_home_heavy_user():
    # 20 - (5 + 1) = 14 GB extra at 15 + 10
    assert overage_charge("standard", 20, False, True) == 14 * 25


# =====================================================================
# recharge_allowed(amount, pending_recharges, is_kyc_pending)
# =====================================================================

# ---- Line 27: is_kyc_pending True -> return amount <= 200 ----

@pytest.mark.parametrize(
    "amount, expected",
    [(0, True), (199, True), (200, True), (201, False), (2500, False)],
)
def test_kyc_pending_limits_recharge_to_200(amount, expected):
    assert recharge_allowed(amount, 0, True) is expected


def test_kyc_pending_ignores_pending_recharge_count():
    # The KYC branch returns before pending_recharges is checked
    assert recharge_allowed(100, 10, True) is True


# ---- Line 29: amount > 2000 (True -> False, False -> line 31) ----

@pytest.mark.parametrize("amount", [2001, 5000])
def test_recharge_above_2000_is_rejected(amount):
    assert recharge_allowed(amount, 0, False) is False


def test_recharge_of_exactly_2000_is_allowed():
    assert recharge_allowed(2000, 0, False) is True


# ---- Line 31: return pending_recharges <= 2 ----

@pytest.mark.parametrize(
    "pending, expected",
    [(0, True), (1, True), (2, True), (3, False), (7, False)],
)
def test_pending_recharge_limit(pending, expected):
    assert recharge_allowed(500, pending, False) is expected


def test_large_amount_with_too_many_pending_is_rejected():
    assert recharge_allowed(2000, 3, False) is False


# =====================================================================
# validity_status(days_left, is_prepaid, has_addon)
# =====================================================================
# Line 35 (is_prepaid) and line 39 (has_addon) give four cutoffs:
#   prepaid, no addon   -> 0
#   prepaid, addon      -> 2
#   postpaid, no addon  -> 3
#   postpaid, addon     -> 5
# Line 41 (days_left >= cutoff) and line 43 (days_left >= cutoff - 15)
# are tested at each boundary for every cutoff.

CUTOFFS = [
    (True, False, 0),
    (True, True, 2),
    (False, False, 3),
    (False, True, 5),
]


@pytest.mark.parametrize("is_prepaid, has_addon, cutoff", CUTOFFS)
def test_active_on_or_after_cutoff(is_prepaid, has_addon, cutoff):
    assert validity_status(cutoff, is_prepaid, has_addon) == "active"
    assert validity_status(cutoff + 30, is_prepaid, has_addon) == "active"


@pytest.mark.parametrize("is_prepaid, has_addon, cutoff", CUTOFFS)
def test_grace_between_cutoff_minus_15_and_cutoff(is_prepaid, has_addon, cutoff):
    assert validity_status(cutoff - 1, is_prepaid, has_addon) == "grace"
    assert validity_status(cutoff - 15, is_prepaid, has_addon) == "grace"


@pytest.mark.parametrize("is_prepaid, has_addon, cutoff", CUTOFFS)
def test_expired_before_grace_window(is_prepaid, has_addon, cutoff):
    assert validity_status(cutoff - 16, is_prepaid, has_addon) == "expired"
    assert validity_status(cutoff - 100, is_prepaid, has_addon) == "expired"
