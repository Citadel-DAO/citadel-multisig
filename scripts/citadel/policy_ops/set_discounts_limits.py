from rich.console import Console

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


console = Console()


def set_discounts_limits(limits):
    safe = GreatApeSafe(registry.eth.citadel.governance)
    safe.init_citadel()
    changed = 0
    for asset, limit in limits.items():
        current = safe.citadel.get_discount_limits(asset)
        if current != limit:
            console.print(f"Setting {asset}'s current discount limit of {(current.min, current.max)} to {limit}...")
            safe.citadel.set_discount_limits(
                asset, limit[0], limit[1]
            )
            changed += 1
    if changed > 0:
        return safe


def main(limits={
    'wbtc': (0, 5000),
    'cvx': (1000, 4000)
}):
    safe = set_discounts_limits(limits)
    if not safe is None:
        safe.post_safe_tx(call_trace=True)
