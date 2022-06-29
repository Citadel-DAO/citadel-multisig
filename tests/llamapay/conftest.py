import pytest

from great_ape_safe import GreatApeSafe
from helpers.addresses import r


@pytest.fixture
def safe():
    return GreatApeSafe('ychad.eth')

@pytest.fixture
def dai(safe):
    return safe.contract(r.tokens.dai)

@pytest.fixture
def usdc(safe):
    return safe.contract(r.tokens.usdc)

@pytest.fixture
def payee():
    return "0x8727FF875E070d73B678cCea85BF9FF01c05A785"

@pytest.fixture
def payee2():
    return "0x40A63aDC56B32fdeF389FcB98571EdDC5e53daeD"