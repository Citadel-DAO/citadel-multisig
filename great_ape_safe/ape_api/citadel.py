import json
import os
import requests
from decimal import Decimal

from brownie import chain, interface, ZERO_ADDRESS
from brownie.exceptions import VirtualMachineError
from eth_abi import encode_abi
# from helpers.constants import AddressZero

from helpers.addresses import registry
from rich.console import Console

class Citadel():
    """
    collection of all contracts and methods needed to interact with the Citadel
    system.
    """

    def __init__(self, safe):
        self.safe = safe
        self.funding_contracts = {}
        self.funding_contracts[registry.eth.tokens.cvx] = interface.IFunding(
                registry.eth.funding.cvx,
                owner=self.safe.account
            )
        self.funding_contracts[registry.eth.tokens.wbtc] = interface.IFunding(
                registry.eth.funding.cvx,
                owner=self.safe.account
            )
    
    def set_discount(self, discount, token):
        self.funding_contracts[token].setDiscount(discount)

    def set_discount_limits(self, min_discount, max_discount, token):
        self.funding_contracts[token].setDiscountLimits(min_discount, max_discount)

    def set_discounts(self, discounts):
        for token, discount in discounts.items():
            self.set_discount(discount, token)
