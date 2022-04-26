from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


MIN = 100
MAX = 200

def main():
    safe = GreatApeSafe(registry.eth.policy_ops)
    safe.init_citadel()
    safe.citadel.set_asset_limits(
        MIN, MAX
        registry.eth.tokens.cvx
    )
    asset_limits = safe.citadel.get_asset_limits(registry.eth.tokens.cvx)
    assert asset_limits.min == MIN
    assert asset_limits.max == MAX

