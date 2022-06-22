from great_ape_safe import GreatApeSafe
from helpers.addresses import registry

ops_avatar = None
liq_avatar = None
badger_avatar = None
frax_avatar = None
silo_msig = None

DUSTY = 0.98
DEADLINE = 60 * 60 * 24

safe = GreatApeSafe(registry.eth.citadel.governance)
safe.init_cow()

wbtc = safe.contract(registry.eth.tokens.wbtc)
usdc = safe.contract(registry.eth.tokens.usdc)
frax = safe.contract(registry.eth.tokens.frax)
weth = safe.contract(registry.eth.tokens.weth)
badger = safe.contract(registry.eth.tokens.badger)
cvx = safe.contract(registry.eth.tokens.cvx)
renbtc = safe.contract(registry.eth.tokens.renbtc)


def swap_stables():
    safe.cow.allow_relayer(usdc, 15e6 + 58.65e6 + 33.03e6)
    safe.cow.allow_relayer(frax, 34.52e6)

    # Swap $15 USDC -> ETH (urgent for operations)
    safe.cow.market_sell(usdc, weth, 15e6, deadline=DEADLINE)

    # Swap $58.65 USDC -> WBTC (immediately for deployment)
    safe.cow.market_sell(usdc, wbtc, 58.65e6, deadline=DEADLINE)

    # Swap $33.03 USDC -> WBTC (This could be done in a ladder order over 2 weeks)
    safe.cow.market_sell(usdc, wbtc, 33.03e6, deadline=DEADLINE)

    # Swap $34.52 FRAX -> WBTC (This could be done in a ladder order over 2 weeks)
    safe.cow.market_sell(frax, wbtc, 34.52e6, deadline=DEADLINE)
    safe.post_safe_tx()


def distribute_assets():
    safe.take_snapshot(tokens=[
        weth, usdc, wbtc, cvx, renbtc, badger, frax
    ])

    # Deploy $15 in ETH to operations
    weth.transfer(ops_avatar, weth.balanceOf(safe) * DUSTY)

    # Deploy $35 USDC To operations
    usdc.transfer(ops_avatar, 35e6 * DUSTY)

    # Send $51 WBTC -> to Liqudity for CTDL/WBTC liquidity (@jonto need break down here)
    wbtc.transfer(liq_avatar, 0.00173e8 * DUSTY)

    # Send $51 CVX -> to bveCVX Badger Strat
    cvx.transfer(badger_avatar, 7.34e18 * DUSTY)

    # Send $51 renBTC -> to Badger Strat (for ibBTC)
    renbtc.transfer(badger_avatar, 0.00173e8 * DUSTY)

    # Send $51 Badger -> to Badger Strat (for wBTC/Badger LP)
    badger.transfer(badger_avatar, 10.65e18 * DUSTY)

    # Send $51 WBTC -> Badger Strat (for wBTC/Badger LP)
    wbtc.transfer(badger_avatar, 0.00173e8 * DUSTY)

    # Send $61 WBTC -> Frax strategy (leave undeployed)
    wbtc.transfer(frax_avatar, 0.00173e8 * DUSTY)

    # Send $40 FRAX -> Frax Stregy (leave undeployed)
    frax.transfer(frax_avatar, 40e18 * DUSTY)

    # Send resulting BTC to Silo
    wbtc.transfer(silo_msig, wbtc.balanceOf(safe) * DUSTY)

    safe.print_snapshot()
    safe.post_safe_tx()
