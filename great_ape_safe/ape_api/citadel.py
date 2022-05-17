from collections import namedtuple

from brownie import interface, web3

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
        self.staked_citadel_locker = interface.IStakedCitadelLocker(
            registry.eth.citadel.staked_citadel_locker, owner=self.safe.account
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

    def set_citadel_distribution_split(self, funding_bps, staking_bps, locking_bps):
        # enforce here so there is not revert at SC level
        assert funding_bps + staking_bps + locking_bps == self.MAX_BPS
        self.citadel_minter.setCitadelDistributionSplit(
            funding_bps, staking_bps, locking_bps
        )
        assert self.citadel_minter.fundingBps() == funding_bps
        assert self.citadel_minter.stakingBps() == staking_bps
        assert self.citadel_minter.lockingBps() == locking_bps

    def set_funding_pool_weight(self, asset, weight):
        # enforce here so there is not revert at SC level
        assert weight <= self.MAX_BPS
        funding_pool = self.get_funding_contract(asset)
        self.citadel_minter.setFundingPoolWeight(funding_pool.address, weight)

    def distribute_yield(self, asset, mantissa):
        assert mantissa > 0
        asset = interface.ERC20(asset, owner=self.safe.account)
        asset.approve(self.staked_citadel_locker, mantissa)
        self.staked_citadel_locker.notifyRewardAmount(
            asset,
            mantissa,
            web3.solidityKeccak(['bytes32'], [b'treasury-yield']).hex()
        )
