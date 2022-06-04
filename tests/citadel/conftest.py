import pytest
from brownie import Contract
from brownie_tokens import MintableForkToken

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


@pytest.fixture(scope="module")
def cvx(treasury_vault, gov):
    """Airdrop some CVX to the treasury vault & governance"""
    addr = registry.eth.tokens.cvx
    Contract.from_explorer(addr)
    cvx = MintableForkToken(addr)
    cvx._mint_for_testing(treasury_vault, 12345e18)
    cvx._mint_for_testing(gov, 12345e18)
    return Contract(addr)


@pytest.fixture(scope="module")
def wbtc(treasury_vault, gov):
    """Airdrop some WBTC to the treasury vault & governance"""
    addr = registry.eth.tokens.wbtc
    Contract.from_explorer(addr)
    wbtc = MintableForkToken(addr)
    wbtc._mint_for_testing(treasury_vault, 12345e8)
    wbtc._mint_for_testing(gov, 12345e8)
    return Contract(addr)


@pytest.fixture(autouse=True, scope="module")
def confirm_access(gov, policy_ops):
    if gov.citadel.gac.paused() == True:
        gov.citadel.gac.unpause()

    if not gov.citadel.gac.hasRole(gov.citadel.gac.CONTRACT_GOVERNANCE_ROLE(), gov):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.CONTRACT_GOVERNANCE_ROLE(),
            registry.eth.citadel.governance,
            {"from": registry.eth.citadel.deployer},
        )

    if not gov.citadel.gac.hasRole(
        gov.citadel.gac.POLICY_OPERATIONS_ROLE(), policy_ops
    ):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.POLICY_OPERATIONS_ROLE(),
            policy_ops,
            {"from": registry.eth.citadel.deployer},
        )

    if not gov.citadel.gac.hasRole(gov.citadel.gac.CITADEL_MINTER_ROLE(), gov):
        gov.citadel.gac.grantRole(
            gov.citadel.gac.CITADEL_MINTER_ROLE(),
            r.citadel.governance,
            {"from": r.citadel.deployer},
        )
