from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def set_asset_price_limits(limits):
    safe = GreatApeSafe(registry.eth.citadel.governance)
    safe.init_citadel()
    changed = 0
    for asset, (min_price, max_price) in limits.items():
        if safe.citadel.get_asset_price_limits(asset) != (min_price, max_price):
            safe.citadel.set_asset_price_limits(
                asset, min_price, max_price
            )
            changed += 1
    if changed > 0:
        return safe


def main(limits={
    'wbtc': (0, 5000),
    'cvx': (1000, 4000)
}):
    safe = set_asset_price_limits(limits)
    if not safe is None:
        safe.post_safe_tx(call_trace=True)
