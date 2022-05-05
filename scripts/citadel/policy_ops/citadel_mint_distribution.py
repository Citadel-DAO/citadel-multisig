from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main(funding_bps=4000, staking_bps=3000, locking_bps=3000):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()

    safe.citadel.set_citadel_distribution_split(
        int(funding_bps), int(staking_bps), int(locking_bps)
    )

    safe.post_safe_tx()
