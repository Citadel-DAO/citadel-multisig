from great_ape_safe import GreatApeSafe
from helpers.addresses import registry
from brownie import interface


def main(
    round_address=registry.eth.citadel.knighting_round,
    new_price_ether=1
    ):

    safe = GreatApeSafe(registry.eth.citadel.governance)
    knighting_round = interface.IKnightingRound(round_address, owner=safe.address)

    new_price = new_price_ether * 1e18
    current_price = knighting_round.tokenOutPrice()
    assert current_price != new_price

    knighting_round.setTokenOutPrice(new_price)
    assert knighting_round.tokenOutPrice() == new_price

    safe.post_safe_tx()