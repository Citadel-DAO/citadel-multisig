from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def set_discounts(discounts):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()
    changed = 0
    for funding_token, discount in discounts.items():
        current = safe.citadel.get_discount(funding_token)
        if current != discount:
            safe.citadel.set_discount(funding_token, discount)
            changed += 1
    if changed > 0:
        return safe


def main(discounts={
    'wbtc': 4000,
    'cvx': 3000,
}):
    safe = set_discounts(discounts)
    if not safe is None:
        safe.post_safe_tx(call_trace=True)
