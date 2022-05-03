import brownie

from scripts.citadel.policy_ops.set_discounts import set_discounts
from scripts.citadel.policy_ops.set_discounts_limits import  set_discounts_limits
from scripts.citadel.policy_ops.set_asset_price_limits import  set_asset_price_limits


def test_set_single_discount_limit():
    set_discounts_limits({'wbtc': (0, 5000)})


def test_set_multiple_discount_limits():
    set_discounts_limits({'wbtc': (1000, 4000), 'cvx': (0, 3000)})


def test_set_multiple_discount_limits_fail():
    with brownie.reverts('maxDiscount >= MAX_BPS'):
        set_discounts_limits({'wbtc': (1000, 4000), 'cvx': (0, 11000)})


def test_set_single_discount():
    set_discounts({'wbtc': 1000})


def test_set_single_discount_fail():
    with brownie.reverts('discount < minDiscount'):
        set_discounts({'wbtc': 500})


def test_set_multiple_discounts():
    set_discounts({'wbtc': 1000, 'cvx': 3000})


def test_set_single_asset_price_limit():
    set_asset_price_limits({'cvx': (10e18, 50e18)})


def test_set_multiple_asset_price_limits():
    set_asset_price_limits({'wbtc': (40_000e8, 169_000e8), 'cvx': (10e18, 50e18)})