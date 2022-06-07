from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main(funding_bps=5000, staking_bps=2500, locking_bps=1000, dao_bps=1500):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()

    safe.citadel.set_citadel_distribution_split(
        int(funding_bps), int(staking_bps), int(locking_bps), int(dao_bps)
    )

    safe.post_safe_tx()
