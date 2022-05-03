from great_ape_safe import GreatApeSafe
from helpers.addresses import registry

def main():
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()

    safe.citadel.mint_and_distribute()

    safe.post_safe_tx()