import pytest

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


@pytest.fixture(scope="module")
def gov():
    gov = GreatApeSafe(registry.eth.citadel.governance)
    gov.init_citadel()
    return gov


@pytest.fixture(scope="module")
def treasury_vault():
    treasury_vault = GreatApeSafe(registry.eth.citadel.treasury_vault)
    treasury_vault.init_citadel()
    return treasury_vault


@pytest.fixture(scope="module")
def policy_ops():
    policy_ops = GreatApeSafe(registry.eth.citadel.policy_ops)
    policy_ops.init_citadel()
    return policy_ops


@pytest.fixture(autouse=True)
def confirm_access(gov):
    if gov.citadel.gac.paused() == True:
        gov.citadel.gac.unpause()

    if not gov.citadel.gac.hasRole(
        gov.citadel.gac.CONTRACT_GOVERNANCE_ROLE(), registry.eth.citadel.governance
    ):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.CONTRACT_GOVERNANCE_ROLE(),
            registry.eth.citadel.governance,
            {"from": registry.eth.citadel.deployer},
        )

    if not gov.citadel.gac.hasRole(
        gov.citadel.gac.POLICY_OPERATIONS_ROLE(), registry.eth.citadel.policy_ops
    ):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.POLICY_OPERATIONS_ROLE(),
            registry.eth.citadel.policy_ops,
            {"from": registry.eth.citadel.deployer},
        )
