from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


DISCOUNT = 4000

def main():
    safe = GreatApeSafe(registry.eth.policy_ops)
    safe.init_citadel()
    safe.citadel.set_discount(
        DISCOUNT,
        registry.eth.tokens.cvx
    )
    assert safe.citadel.get_discount() == DISCOUNT
