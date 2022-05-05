from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main(asset="wbtc", weight=100):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()

    safe.citadel.set_funding_pool_weight(asset, weight)

    safe.post_safe_tx()
