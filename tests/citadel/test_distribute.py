import pytest
from brownie import ZERO_ADDRESS

from scripts.citadel.policy_ops.distribute_yield import distribute_yield


@pytest.fixture(scope='module', autouse=True)
def config_distributor(gov, cvx, treasury_vault):
    if gov.citadel.staked_citadel_locker.gac() == ZERO_ADDRESS:
        gov.citadel.staked_citadel_locker.__GlobalAccessControlManaged_init(
            gov.citadel.gac
        )
    gov.citadel.staked_citadel_locker.addReward(
        cvx, treasury_vault, False
    )
    gov.citadel.staked_citadel_locker.approveRewardDistributor(
        cvx, treasury_vault, True
    )


def test_distribute(cvx):
    distribute_yield(cvx.address, 123e18)
