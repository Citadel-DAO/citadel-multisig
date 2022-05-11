from great_ape_safe import GreatApeSafe
from helpers.addresses import registry
from helpers.constants import MaxUint256

from brownie.convert import to_string

from rich.console import Console
from rich.table import Table
from rich.pretty import pprint

C = Console()

# TO UPDATE: accordingly to new funding contracts deployed with diff assets
assets = ["cvx", "wbtc"]

column_names = [
    "Pool Weight",
    "Global Weight (%)",
    "Discount",
    "Discount Limits",
    "Asset Cap",
    "CTDL Balance",
    "Flag Status",
    "Price",
    "Price Limit",
]


def main():
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_citadel()

    ctdl = safe.contract(registry.eth.tokens.citadel)

    C.print("[bold yellow] ==== Mint distribution split ==== [/bold yellow]\n")
    pprint(safe.citadel.get_citadel_distribution_split(), expand_all=True)

    for asset in assets:
        erc20 = safe.contract(registry.eth.tokens[asset])
        discount_limit = safe.citadel.get_discount_limits(asset)
        price_limit = safe.citadel.get_asset_price_limits(asset)

        price_limit = price_limit._replace(
            max="MAX_UINT256" if price_limit.max == MaxUint256 else price_limit.max
        )

        table = Table(title=f"{asset.upper()} funding pool information")

        for name in column_names:
            table.add_column(name)

        table.add_row(
            to_string(safe.citadel.get_funding_pool_weight(asset)),
            "{:.2%}".format(
                safe.citadel.get_funding_pool_weight(asset)
                / safe.citadel.get_total_funding_pool_weight()
            ),
            to_string(safe.citadel.get_discount(asset)),
            f"[{discount_limit.min}, {discount_limit.max}]",
            to_string(safe.citadel.get_asset_cap(asset) / 10 ** erc20.decimals()),
            to_string(
                ctdl.balanceOf(safe.citadel.get_funding_contract(asset)).to("ether")
            ),
            to_string(safe.citadel.get_citadel_price_flag(asset)),
            to_string(safe.citadel.get_citadel_price_per_asset(asset) / 1e18), # price always on 18 decimals denomination
            f"[{price_limit.min}, {price_limit.max}]",
        )

        C.print(table)
