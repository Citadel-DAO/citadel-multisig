from dis import disco
from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


MIN_DISCOUNT = 100
MAX_DISCOUNT = 200

def main():
    safe = GreatApeSafe(registry.eth.policy_ops)
    safe.init_citadel()
    safe.citadel.set_discount_limits(
        MIN_DISCOUNT, MAX_DISCOUNT
        registry.eth.tokens.cvx
    )
    discount_limits = safe.citadel.get_discount_limits(registry.eth.tokens.cvx)
    assert discount_limits.min == MIN_DISCOUNT
    assert discount_limits.max == MAX_DISCOUNT

