from great_ape_safe import GreatApeSafe
from helpers.addresses import r
from decimal import Decimal
from brownie import chain, Contract, interface

# constants
CITADEL_LAUNCH_DOLLAR_PRICE = 21
SUPPLY_MULTIPLIER = Decimal(1666666666666666667 / 1e18)
LIQUIDITY_PCT = 0.4
TREASURY_PCT = 0.6
MAX_DISCOUNT = 3000
DISCOUNT = 1050
RATES = [
    593962000000000000000000,
    591445000000000000000000,
    585021000000000000000000,
    574138000000000000000000,
    558275000000000000000000,
    536986000000000000000000,
]
# prices asset limits is going to be 1/3x and 3x
FACTOR_PRICES = 3


def main():
    governance = GreatApeSafe(r.citadel.governance)
    treasury = GreatApeSafe(r.citadel.treasury_vault)
    governance.init_citadel()
    governance.init_curve()

    # tokens involved
    ctdl = governance.contract(r.tokens.citadel)
    xCTDL = governance.contract(r.tokens.xCTDL)
    lp_ctdl_wbtc = governance.contract(r.tokens.crvCtdlWbtc)

    # contracts involved
    balance_checker = interface.IBalanceChecker(
        r.helpers.balance_checker, owner=governance.account
    )
    wbtc_usdc_oracle = interface.IOracle(r.chainlink.btc_usd_feed)
    gac = governance.contract(r.citadel.gac)
    kr_array = [
        interface.IKnightingRound(addr, owner=governance.account)
        for addr in r.citadel.knighting_round.values()
    ]
    kr_array_len = len(kr_array) - 1

    # console snaps
    tokens = [ctdl, xCTDL, lp_ctdl_wbtc]
    # assets in rounds : cvx, renBTC, ibBTC, frax, usdc, badger, bveCVX, weth and wbtc
    tokens_in = [kr.tokenIn() for kr in kr_array]
    tokens += tokens_in
    governance.take_snapshot(tokens)
    treasury.take_snapshot(tokens)

    total_citadel_bought = 0
    citadatel_bougth_per_round = [0] * kr_array_len

    for i in range(kr_array_len):
        total_citadel_bought += kr_array[i].totalTokenOutBought()
        citadatel_bougth_per_round[i] = kr_array[i].totalTokenOutBought()

    # calculate total to be mint
    initial_supply = total_citadel_bought * SUPPLY_MULTIPLIER
    ctdl.mint(governance, initial_supply)

    # approve and depositFor in xCitadel
    ctdl.approve(xCTDL, total_citadel_bought)

    for i in range(kr_array_len):
        xCTDL.depositFor(kr_array[i], citadatel_bougth_per_round[i])
        balance_checker.verifyBalance(xCTDL, kr_array[i], citadatel_bougth_per_round[i])

    remaining_supply = initial_supply - total_citadel_bought - 1e18
    to_liquidity = remaining_supply * LIQUIDITY_PCT
    to_treasury = remaining_supply * TREASURY_PCT

    # seed xCitadel with 1 ctdl
    ctdl.approve(xCTDL, 1e18)
    xCTDL.deposit(1e18)

    # send ctdl to vault
    ctdl.transfer(to_treasury, treasury)
    balance_checker.verifyBalance(ctdl, treasury, to_treasury)

    # add liquidity into curve factory pool prior
    wbtc_amount_per_ctdl = (
        CITADEL_LAUNCH_DOLLAR_PRICE
        / (wbtc_usdc_oracle.latestAnswer() / 10 ** wbtc_usdc_oracle.decimals())
        * 1e18
    )
    wbtc_liquidity = ((to_liquidity * wbtc_amount_per_ctdl) / 1e18) / 1e10
    governance.curve.deposit(lp_ctdl_wbtc, [to_liquidity, wbtc_liquidity])

    balance_checker.verifyBalance(ctdl, 0, to_liquidity)
    balance_checker.verifyBalance(r.tokens.wbtc, 0, wbtc_liquidity)

    # assets transfers to vault from KRs
    for i in range(kr_array_len):
        token_in = governance.contract(tokens_in[i])
        token_in_bal = token_in.balanceOf(governance)
        token_in.transfer(treasury, token_in_bal)

    # ensure all was distributed
    assert ctdl.balanceOf(governance) < 3e18

    # revoke `CITADEL_MINTER_ROLE`
    CITADEL_MINTER_ROLE = gac.CITADEL_MINTER_ROLE()
    gac.revokeRole(CITADEL_MINTER_ROLE, governance)

    # finalised KRs
    for i in range(kr_array_len):
        kr_array[i].finalize()

    # set discount & price limits for funding contracts: wbtc, cvx & badger
    POLICY_OPERATIONS_ROLE = gac.POLICY_OPERATIONS_ROLE()
    gac.grantRole(POLICY_OPERATIONS_ROLE, governance)

    funding_tokens = r.citadel.funding
    for asset in funding_tokens.keys():
        governance.citadel.set_discount_limits(asset, 0, MAX_DISCOUNT)
        governance.citadel.set_discount_manager(asset, r.citadel.discount_manager)
        min_price, max_price = _asset_price_limit_helper(asset)
        governance.citadel.set_asset_price_limits(asset, min_price, max_price)
        governance.citadel.set_discount(asset, DISCOUNT)

        # check if they're paused, then unpaused
        funding_contract = governance.citadel.get_funding_contract(asset)
        if funding_contract.paused():
            funding_contract.unpause()

    # set minting schedules
    for epoch, rate in RATES:
        governance.citadel.set_epoch_rate(epoch, rate)

    governance.citadel.supply_schedule.setMintingStart(chain.time())

    treasury.print_snapshot()
    governance.post_safe_tx()


def _asset_price_limit_helper(asset, factor=FACTOR_PRICES):
    oracle = interface.IOracle(r.chainlink[f"{asset}_usd_feed"])

    price = oracle.latestAnswer() / 10 ** oracle.decimals()

    asset_decimal = Contract(r.tokens[asset]).decimals()

    token_out_per_token_in = _token_out_per_token_in(
        CITADEL_LAUNCH_DOLLAR_PRICE, price, asset_decimal
    )

    min_price = token_out_per_token_in / factor
    max_price = token_out_per_token_in * factor

    return min_price, max_price


def _token_out_per_token_in(desired_price, price_in_usd, decimals):
    return ((desired_price * 1e8) * (10 ** decimals)) / (price_in_usd * 1e8)
