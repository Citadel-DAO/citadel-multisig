from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main(stream_id=0):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_sablier()

    safe.sablier.cancel_stream(int(stream_id))

    safe.post_safe_tx()
