import pytest

from helpers.addresses import r

from scripts.citadel.launch.mint_post_kr import mint_launch


@pytest.fixture(scope="module", autouse=True)
def config_distributor(gov, cvx, interface):
    kr_guest = interface.IKnightingRoundGuestList(r.citadel.knighting_round_guest_list)
    kr_guest.setGuests([gov.address], [True], {"from": r.citadel.deployer})

    kr = interface.IKnightingRound(r.citadel.knighting_round.cvx, owner=gov.account)
    cvx.approve(kr, 10e18, {"from": gov.address})
    kr.buy(10e18, 0, [])


def test_launch():
    mint_launch()
