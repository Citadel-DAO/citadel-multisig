from rich.console import Console

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


console = Console()


def set_discounts(discounts):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()
    changed = 0
    for asset, discount in discounts.items():
        current = safe.citadel.get_discount(asset)
        if current != discount:
            console.print(f"Setting {asset}'s current discount of {current} to {discount} (diff of {discount - current})...")
            safe.citadel.set_discount(asset, discount)
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
