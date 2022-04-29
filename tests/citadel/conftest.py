import pytest

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


@pytest.fixture
def gov():
    gov = GreatApeSafe(registry.eth.citadel.governance)
    gov.init_citadel()
    return gov


@pytest.fixture(autouse=True)
def confirm_access(gov):
    if gov.citadel.gac.paused() == True:
        gov.citadel.gac.unpause()

    if not gov.citadel.gac.hasRole(
        gov.citadel.gac.CONTRACT_GOVERNANCE_ROLE(),
        registry.eth.citadel.governance
    ):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.CONTRACT_GOVERNANCE_ROLE(),
            registry.eth.citadel.governance,
            {'from': registry.eth.citadel.deployer}
        )

    if not gov.citadel.gac.hasRole(
        gov.citadel.gac.POLICY_OPERATIONS_ROLE(),
        registry.eth.citadel.policy_ops
    ):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.POLICY_OPERATIONS_ROLE(),
            registry.eth.citadel.policy_ops,
            {'from': registry.eth.citadel.deployer}
        )
