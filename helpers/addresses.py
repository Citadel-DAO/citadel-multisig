import pandas as pd

from dotmap import DotMap
from web3 import Web3
import json

ADDRESSES_ETH = {
    "badger_vaults": {
        "bBADGER": "0x19D97D8fA813EE2f51aD4B4e04EA08bAf4DFfC28",
        "bDIGG": "0x7e7E112A68d8D2E221E11047a72fFC1065c38e1a",
        "bcrvRenBTC": "0x6dEf55d2e18486B9dDfaA075bc4e4EE0B28c1545",
        "bcrvSBTC": "0xd04c48A53c111300aD41190D63681ed3dAd998eC",
        "bcrvTBTC": "0xb9D076fDe463dbc9f915E5392F807315Bf940334",
        "bharvestcrvRenBTC": "0xAf5A1DECfa95BAF63E0084a35c62592B774A2A87",
        "buniWbtcBadger": "0x235c9e24D3FB2FAFd58a2E49D454Fdcd2DBf7FF1",
        "bslpWbtcBadger": "0x1862A18181346EBd9EdAf800804f89190DeF24a5",
        "bslpWbtcibBTC": "0x8a8FFec8f4A0C8c9585Da95D9D97e8Cd6de273DE",
        "buniWbtcDigg": "0xC17078FDd324CC473F8175Dc5290fae5f2E84714",
        "bslpWbtcDigg": "0x88128580ACdD9c04Ce47AFcE196875747bF2A9f6",
        "bslpWbtcEth": "0x758A43EE2BFf8230eeb784879CdcFF4828F2544D",
        "bcrvHBTC": "0x8c76970747afd5398e958bdfada4cf0b9fca16c4",
        "bcrvPBTC": "0x55912d0cf83b75c492e761932abc4db4a5cb1b17",
        "bcrvOBTC": "0xf349c0faa80fc1870306ac093f75934078e28991",
        "bcrvBBTC": "0x5dce29e92b1b939f8e8c60dcf15bde82a85be4a9",
        "bcrvIbBTC": "0xaE96fF08771a109dc6650a1BdCa62F2d558E40af",
        "bcrvTricrypto": "0xBE08Ef12e4a553666291E9fFC24fCCFd354F2Dd2",
        "bcrvTricrypto2": "0x27E98fC7d05f54E544d16F58C194C2D7ba71e3B5",
        "bcvxCRV": "0x2B5455aac8d64C14786c3a29858E43b5945819C0",
        "bCVX": "0x53c8e199eb2cb7c01543c137078a038937a68e40",
        # "bbCVX": "0xE143aA25Eec81B4Fc952b38b6Bca8D2395481377",
        "bveCVX": "0xfd05D3C7fe2924020620A8bE4961bBaA747e6305",
        "bimBTC": "0x599D92B453C010b1050d31C364f6ee17E819f193",
        "bFpMbtcHbtc": "0x26B8efa69603537AC8ab55768b6740b67664D518",
        "bbveCVX-CVX-f": "0x937B8E917d0F36eDEBBA8E459C5FB16F3b315551",
        "remBADGER": "0x6aF7377b5009d7d154F36FE9e235aE1DA27Aea22",
        "remDIGG": "0x99F39D495C6A5237f43602f3Ab5F49786E46c9B0",
        "bcrvBadger": "0xeC1c717A3b02582A4Aa2275260C583095536b613"
    },
    "compound": {
        "comptroller": "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B",
    },
    "aave": {
        "incentives_controller": "0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5",
        "aave_lending_pool_v2": "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
        "data_provider": "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d",
    },
    "cow": {
        "vault_relayer": "0xC92E8bdf79f0507f65a392b0ab4667716BFE0110",
        "settlement": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    },
    "ibBTC": {
        "core": "0x2A8facc9D49fBc3ecFf569847833C380A13418a8",
    },
    "convex": {
        "cvxCRV_rewards": "0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",
        "crv_depositor": "0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae",
        "vlCvxExtraRewardDistribution": "0xDecc7d761496d30F30b92Bdf764fb8803c79360D",
        "booster": "0xF403C135812408BFbE8713b5A23a04b3D48AAE31",
        "claim_zap": "0x92Cf9E5e4D1Dfbf7dA0d2BB3e884a68416a65070",
        "vlCVX": "0xD18140b4B819b895A3dba5442F959fA44994AF50",
    },
    "votium": {
        "multiMerkleStash": "0x378Ba9B73309bE80BF4C2c027aAD799766a7ED5A",
    },
    "uniswap": {
        "factoryV3": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
        "v3pool_wbtc_badger": "0xe15e6583425700993bd08F51bF6e7B73cd5da91B",
        "NonfungiblePositionManager": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
        "routerV2": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
        "factoryV2": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    },
    "sushiswap": {
        "routerV2": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
        "factoryV2": "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac",
    },
    "curve": {
        "provider": "0x0000000022D53366457F9d5E68Ec105046FC4383",
        "factory": "0x0959158b6040D32d04c301A72CBFD6b39E21c9AE",
        "zap_sbtc": "0x7AbDBAf29929e7F8621B757D2a7c04d78d633834",
        "zap_3pool": "0xA79828DF1850E8a3A3064576f380D90aECDD3359",
        "zap_ibbtc": "0xbba4b444FD10302251d9F5797E763b0d912286A1",
        "zap_pbtc": "0x11F419AdAbbFF8d595E7d5b223eee3863Bb3902C",
        "zap_obtc": "0xd5BCf53e2C81e1991570f33Fa881c49EEa570C8D",
    },
    "uma": {
        "DIGG_LongShortPair": "0x65DCcd928C71ef98e6eC887FEA24d116765c8A8D",
    },
    "nft": {
        "badger_jersey": "0xe1e546e25A5eD890DFf8b8D005537c0d373497F8"
    },
    "arbitrum": {
        "outbox": "0x760723CD2e632826c38Fef8CD438A4CC7E7E1A40",
    },
    "governance": "0xa95ecbDc51082ED2a2D078a5dE5275777dD73347",
    "treasuryVault": "0x38724146C8dc1Aa49c3395091cf86B789c37F52c",
    "policyOps": "0x7426e8987f8d388e731Dec452D8B0a1710d8E416"
}


def checksum_address_dict(addresses):
    """
    convert addresses to their checksum variant taken from a (nested) dict
    """
    checksummed = {}
    for k, v in addresses.items():
        if isinstance(v, str):
            checksummed[k] = Web3.toChecksumAddress(v)
        elif isinstance(v, dict):
            checksummed[k] = checksum_address_dict(v)
        else:
            print(k, v, "formatted incorrectly")
    return checksummed


with open('helpers/chaindata.json') as chaindata:
    chain_ids = json.load(chaindata)


registry = DotMap({
    "eth": checksum_address_dict(ADDRESSES_ETH),
})

# flatten nested dicts and invert the resulting key <-> value
# this allows for reversed lookup of an address
df = pd.json_normalize(registry, sep="_")
reverse = df.T.reset_index().set_index(0)["index"].to_dict()
