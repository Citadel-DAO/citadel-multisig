from brownie import interface
from helpers.addresses import registry

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

    def set_asset_price_bounds(self, min_price, max_price, token):
        self.funding_contracts[token].setCitadelAssetPriceBounds(min_price, max_price)
