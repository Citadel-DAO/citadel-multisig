from collections import namedtuple

from brownie import interface

from helpers.addresses import registry


Limits = namedtuple("limits", "min max")


class Citadel():
    """
    Collection of all contracts and methods needed to interact with the Citadel
    system.
    """


    def __init__(self, safe):
        self.safe = safe

        # contracts
        self.gac = interface.IGlobalAccessControl(
            registry.eth.citadel.gac, owner=self.safe.account
        )


    def get_funding_contract(self, asset):
        return interface.IFunding(
            registry.eth.citadel.funding[asset],
            owner=self.safe.account
        )


    def get_discount(self, asset):
        return self.get_funding_contract(asset).getDiscount();


    def set_discount(self, asset, discount):
        contract = self.get_funding_contract(asset)
        contract.setDiscount(discount)
        assert discount == self.get_discount(asset)


    def get_discount_limits(self, asset):
        contract = self.get_funding_contract(asset)
        return Limits(
            contract.getFundingParams()[1],
            contract.getFundingParams()[2]
        )


    def set_discount_limits(self, asset, min_discount, max_discount):
        self.get_funding_contract(asset).setDiscountLimits(
            min_discount, max_discount
        )
        assert self.get_discount_limits(asset) == (min_discount, max_discount)


    def get_asset_price_limits(self, asset):
        contract = self.get_funding_contract(asset)
        return Limits(contract.minCitadelPriceInAsset(), contract.maxCitadelPriceInAsset())


    def set_asset_price_limits(self, asset, min_price, max_price):
        self.get_funding_contract(asset).setCitadelAssetPriceBounds(min_price, max_price)
        assert self.get_asset_price_limits(asset) == (min_price, max_price)
