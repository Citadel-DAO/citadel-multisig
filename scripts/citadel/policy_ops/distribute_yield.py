'''
The treasury ops multisig will need a script that will distribute the treasury
yield from the badger vaults it deposits in to staked citadel holders. 
This can be done through the staked citadel locker contract. 

We will also need the ability to claim badger rewards on behalf of the treasury
and sell those tokens for whatever tokens that are required

https://github.com/Citadel-DAO/staked-citadel-locker/blob/main/src/StakedCitadelLocker.sol#L1066

call notifyRewardAmount() for the specified token and amount on the StakedCitadelLocker using
dataTypeHash = keccak256(treasury-yield) = 0xaf388c3c3157dbb1999fecd2348a129dd286852ceddb9352feabbffbac7ca99b

token and amount should be parameters of the script
'''

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry

def main():
    pass


def distribute_yield(asset, mantissa):
    safe = GreatApeSafe(registry.eth.citadel.treasury_vault)
    safe.init_citadel()
    safe.citadel.distribute_yield(asset, mantissa)
