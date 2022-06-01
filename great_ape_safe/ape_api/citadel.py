from collections import namedtuple

from brownie import interface

from helpers.addresses import registry


Limits = namedtuple("limits", "min max")


class Citadel:
    """
    Collection of all contracts and methods needed to interact with the Citadel
    system.
    """

    def __init__(self, safe):
        self.safe = safe

        # constants
        self.MAX_BPS = 10000
        # contracts
        self.gac = interface.IGlobalAccessControl(
            registry.eth.citadel.gac, owner=self.safe.account
        )
        self.citadel_minter = interface.ICitadelMinter(
            registry.eth.citadel.minter, owner=self.safe.account
        )

    def get_funding_contract(self, asset):
        return interface.IFunding(
            registry.eth.citadel.funding[asset], owner=self.safe.account
        )

    def get_discount(self, asset):
        return self.get_funding_contract(asset).getDiscount()

    def set_discount(self, asset, discount):
        contract = self.get_funding_contract(asset)
        contract.setDiscount(discount)
        assert discount == self.get_discount(asset)

    def get_discount_limits(self, asset):
        contract = self.get_funding_contract(asset)
        return Limits(contract.getFundingParams()[1], contract.getFundingParams()[2])

    def set_discount_limits(self, asset, min_discount, max_discount):
        self.get_funding_contract(asset).setDiscountLimits(min_discount, max_discount)
        assert self.get_discount_limits(asset) == (min_discount, max_discount)

    def get_citadel_price_flag(self, asset):
        funding_pool = self.get_funding_contract(asset)
        return funding_pool.citadelPriceFlag()

    def get_citadel_price_per_asset(self, asset):
        funding_pool = self.get_funding_contract(asset)
        return funding_pool.citadelPriceInAsset()

    def get_asset_price_limits(self, asset):
        contract = self.get_funding_contract(asset)
        return Limits(
            contract.minCitadelPriceInAsset(), contract.maxCitadelPriceInAsset()
        )

    def set_asset_price_limits(self, asset, min_price, max_price):
        self.get_funding_contract(asset).setCitadelAssetPriceBounds(
            min_price, max_price
        )
        assert self.get_asset_price_limits(asset) == (min_price, max_price)

    def mint_and_distribute(self):
        self.citadel_minter.mintAndDistribute()

    def get_citadel_distribution_split(self):
        return {
            "funding": "{:.2%}".format(self.citadel_minter.fundingBps() / self.MAX_BPS),
            "staking": "{:.2%}".format(self.citadel_minter.stakingBps() / self.MAX_BPS),
            "locking": "{:.2%}".format(self.citadel_minter.lockingBps() / self.MAX_BPS),
        }

    def set_citadel_distribution_split(
        self, funding_bps, staking_bps, locking_bps, dao_bps=None
    ):
        if not dao_bps:
            # enforce here so there is not revert at SC level
            assert funding_bps + staking_bps + locking_bps == self.MAX_BPS
            self.citadel_minter.setCitadelDistributionSplit(
                funding_bps, staking_bps, locking_bps
            )
        else:
            # latest version contains a new bps variable `daoBps`
            # https://github.com/Citadel-DAO/citadel-contracts/blob/main/src/CitadelMinter.sol#L338
            assert funding_bps + staking_bps + locking_bps + dao_bps == self.MAX_BPS
            self.citadel_minter.setCitadelDistributionSplit(
                funding_bps, staking_bps, locking_bps, dao_bps
            )
            assert self.citadel_minter.daoBps() == dao_bps

        assert self.citadel_minter.fundingBps() == funding_bps
        assert self.citadel_minter.stakingBps() == staking_bps
        assert self.citadel_minter.lockingBps() == locking_bps

    def get_funding_pool_weight(self, asset):
        funding_pool = self.get_funding_contract(asset)
        return self.citadel_minter.fundingPoolWeights(funding_pool)

    def get_total_funding_pool_weight(self):
        return self.citadel_minter.totalFundingPoolWeight()

    def set_funding_pool_weight(self, asset, weight):
        # enforce here so there is not revert at SC level
        assert weight <= self.MAX_BPS
        funding_pool = self.get_funding_contract(asset)
        self.citadel_minter.setFundingPoolWeight(funding_pool.address, weight)

    def get_pricing_oracle(self, asset):
        funding_pool = self.get_funding_contract(asset)
        return funding_pool.citadelPriceInAssetOracle()

    def get_asset_cap(self, asset):
        funding_pool = self.get_funding_contract(asset)
        return funding_pool.getFundingParams()[5]
