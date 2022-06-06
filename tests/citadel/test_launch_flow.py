import pytest
from brownie import chain

from helpers.addresses import r

from scripts.citadel.launch.mint_post_kr import mint_launch


@pytest.fixture(scope="module", autouse=True)
def config_distributor(gov, cvx, interface):
    kr_guest = interface.IKnightingRoundGuestList(r.citadel.knighting_round_guest_list)
    kr_guest.setGuests([gov.address], [True], {"from": r.citadel.deployer})

    kr = interface.IKnightingRound(r.citadel.knighting_round.cvx, owner=gov.account)
    cvx.approve(kr, 10e18, {"from": gov.address})
    kr.buy(10e18, 0, [])

    # get chain on status that kr's contract had finalised
    # reason: https://github.com/Citadel-DAO/citadel-contracts/blob/main/src/KnightingRound.sol#L279
    duration = kr.saleDuration()
    chain.mine(timedelta=duration)


def test_launch():
    mint_launch()
