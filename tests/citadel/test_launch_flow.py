import pytest
from brownie_tokens import MintableForkToken
from brownie import Contract

from helpers.addresses import r

from scripts.citadel.launch.mint_post_kr import mint_launch

BUY_KR_AMOUNT = 10e18


@pytest.fixture(scope="module", autouse=True)
def config_distributor(gov, interface, chain):
    kr_guest = interface.IKnightingRoundGuestList(r.citadel.knighting_round_guest_list)
    kr_guest.setGuests([gov.address], [True], {"from": r.citadel.deployer})

    kr_array = [
        interface.IKnightingRound(addr, owner=gov.account)
        for addr in r.citadel.knighting_round.values()
    ]
    kr_array_len = len(kr_array) - 1

    for i in range(kr_array_len):
        addr = kr_array[i].tokenIn()
        # getting ugly reverts with these 2 tokens, leave in out for smoothing testing for now
        if addr != r.tokens.frax and addr != r.tokens.badger:
            Contract.from_explorer(addr)
            token_in = MintableForkToken(addr)
            token_in._mint_for_testing(gov, BUY_KR_AMOUNT)
            token_in.approve(kr_array[i], BUY_KR_AMOUNT, {"from": gov.address})
            kr_array[i].buy(BUY_KR_AMOUNT, 0, [])

    # get chain on status that kr's contract had finalised
    # reason: https://github.com/Citadel-DAO/citadel-contracts/blob/main/src/KnightingRound.sol#L279
    duration = kr_array[0].saleDuration()
    chain.mine(timedelta=duration)


def test_launch():
    mint_launch()
