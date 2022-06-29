import json

from brownie import chain
import pandas as pd
from dotmap import DotMap
from web3 import Web3


ADDRESSES_ETH = {
    "tokens": {
        "aave": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
        "stkaave": "0x4da27a545c0c5B758a6BA100e3a049001de870f5",
        "badger": "0x3472A5A71965499acd81997a54BBA8D852C6E53d",
        "citadel": "0x353a38c269A24aafb78Cd214c6E0668847Bb58FD",
        "xCTDL": "0x62624eB2BA4f60A7188214B88542F5772703D551",
        "frax": "0x853d955aCEf822Db058eb8505911ED77F175b99e",
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "weth": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "wbtc": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "comp": "0xc00e94Cb662C3520282E6f5717214004A7f26888",
        "cvx": "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",
        "cvxcrv": "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7",
        "crv": "0xD533a949740bb3306d119CC777fa900bA034cd52",
        "b_crv_ibbtc": "0xaE96fF08771a109dc6650a1BdCa62F2d558E40af",
        "crvCtdlWbtc": "0xE2b11613bBe8E09F73fA81B4A09F0dadB20F5Df6",
        "dai": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    },
    "aave": {
        "incentives_controller": "0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5",
        "aave_lending_pool_v2": "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
        "data_provider": "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d",
    },
    "badger": {
        "tree": "0x660802Fc641b154aBA66a62137e71f331B6d787A",
    },
    "citadel": {
        "deployer": "0xa967ba66fb284ec18bbe59f65bcf42dd11ba8128",
        "governance": "0xa95ecbDc51082ED2a2D078a5dE5275777dD73347",
        "policy_ops": "0x7426e8987f8d388e731Dec452D8B0a1710d8E416",
        "treasury_vault": "0x38724146C8dc1Aa49c3395091cf86B789c37F52c",
        "treasury_ops": "0x7426e8987f8d388e731Dec452D8B0a1710d8E416",  # TODO
        "discount_manager": "0x7426e8987f8d388e731Dec452D8B0a1710d8E416",  # TODO
        "gac": "0xC936098217b987b9D7c24fAC7252f27CdC16c377",
        "minter": "0xB61979B68f6978FD3ab25ae1c8d54456EC37A39f",
        "staked_citadel_locker": "0x9f2819D2D9DE18e96c5d19cBe906d9E490E2dA5b",
        "supply_schedule": "0xDC17DBDb91E874e40158984606BD308213c99803",
        "funding": {
            "wbtc": "0x2559F79Ffd2b705083A5a23f1fAB4bB03C491435",
            "cvx": "0x40927b7bc37380b73DBB60b75d6D5EA308Ec2590",
            "badger": "0x40927b7bc37380b73DBB60b75d6D5EA308Ec2590",  # TODO
        },
        "knighting_round_guest_list": "0x1Ca6d03F372Cc9F2AfB750D17092D71A0d953b57",
        "knighting_round": {
            "wbtc": "0x722D0951E299656AFbA70aC50cc3C42855d44EbB",
            "cvx": "0x7bB5288abd71C9771aF8F94414dC711D31ed7B70",
            "renBTC": "0xa7eFeb1313e6cE6bfFDAe83c3705A62534725aec",
            "ibBTC": "0x680156ab9655f74dc80a0f5ac553564ab914bb12",
            "frax": "0x11b57bE19Dbb4e8918EC77AF7e27849325320d75",
            "usdc": "0x85E4b536568786894dD5Ef5D75220789230095ea",
            "badger": "0xA8bA9ccd4f1aDF8B8aACA177aC13f87f76c5552D",
            "bveCVX": "0xA613175C21cF66EFca7Ab17F6F1E2A1119c02d59",
            "weth": "0xf12a18e985EAD24EB054324d20F81b0EAbA09e57",
        },
        "oracles": {
            "median_oracle_wbtc": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",  # TODO
            "median_oracle_cvx": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",  # TODO
            "median_oracle_badger": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",  # TODO
        },
        "atomic_launch_pool": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",  # TODO
    },
    "chainlink": {
        "wbtc_usd_feed": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
        "cvx_usd_feed": "0xd962fC30A72A84cE50161031391756Bf2876Af5D",
        "badger_usd_feed": "0x66a47b7206130e6FF64854EF0E1EDfa237E65339",
    },
    "compound": {
        "comptroller": "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B",
    },
    "convex": {
        "cvxcrv_rewards": "0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",
        "crv_depositor": "0x8014595F2AB54cD7c604B00E9fb932176fDc86Ae",
        "vlcvx_extra_rewards": "0xDecc7d761496d30F30b92Bdf764fb8803c79360D",
        "booster": "0xF403C135812408BFbE8713b5A23a04b3D48AAE31",
        "claim_zap": "0x92Cf9E5e4D1Dfbf7dA0d2BB3e884a68416a65070",
        "vlcvx": "0xD18140b4B819b895A3dba5442F959fA44994AF50",
    },
    "cow": {
        "vault_relayer": "0xC92E8bdf79f0507f65a392b0ab4667716BFE0110",
        "settlement": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41",
    },
    "curve": {
        "provider": "0x0000000022D53366457F9d5E68Ec105046FC4383",
        "factory": "0x0959158b6040D32d04c301A72CBFD6b39E21c9AE",
        "factory_not_peg_tokens": "0xF18056Bbd320E96A48e3Fbf8bC061322531aac99",
        "zap_sbtc": "0x7AbDBAf29929e7F8621B757D2a7c04d78d633834",
        "zap_3pool": "0xA79828DF1850E8a3A3064576f380D90aECDD3359",
        "zap_ibbtc": "0xbba4b444FD10302251d9F5797E763b0d912286A1",
        "zap_pbtc": "0x11F419AdAbbFF8d595E7d5b223eee3863Bb3902C",
        "zap_obtc": "0xd5BCf53e2C81e1991570f33Fa881c49EEa570C8D",
    },
    "crv_pools": {"crvCtdlWbtc": "0x3c42B0f384D2912661C940d46cfFE1CD10F1c66F"},
    "rari": {
        "unitroller": "0xe3952d770FB26CC61877CD34Fbc3A3750881e9A1",
    },
    "sushiswap": {
        "router_v2": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
        "factory_v2": "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac",
    },
    "uniswap": {
        "router_v2": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
        "factory_v2": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
        "nfp_manager": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
        "factory_v3": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
        "v3pool_wbtc_badger": "0xe15e6583425700993bd08F51bF6e7B73cd5da91B",
    },
    "sablier": "0xCD18eAa163733Da39c232722cBC4E8940b1D8888",
    "helpers": {
        "balance_checker": "0xe92261c2D64C363109c36a754A87107142e61b72",
    },
    "llamapay": {"factory": "0xde1C04855c2828431ba637675B6929A684f84C7F"},
}
ADDRESSES_BSC = {
    "pancakeswap": {
        "router_v1": "0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F",
        "router_v2": "0x10ED43C718714eb63d5aA57B78B54704E256024E",
        "factory_v2": "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
    },
}
ADDRESSES_FANTOM = {
    "solidly": {
        "router": "0xa38cd27185a464914D3046f0AB9d43356B34829D",
        "factory": "0x3fAaB499b519fdC5819e3D7ed0C26111904cbc28",
    },
    "spookyswap": {
        "router": "0xF491e7B69E4244ad4002BC14e878a34207E38c29",
        "factory": "0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3",
    },
}
ADDRESSES_RINKEBY = {"sablier": "0xC1f3af5DC05b0C51955804b2afc80eF8FeED67b9"}


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


with open("helpers/chaindata.json") as chaindata:
    chain_ids = json.load(chaindata)

registry = DotMap(
    {
        "eth": checksum_address_dict(ADDRESSES_ETH),
        "bsc": checksum_address_dict(ADDRESSES_BSC),
        "ftm": checksum_address_dict(ADDRESSES_FANTOM),
        "rin": checksum_address_dict(ADDRESSES_RINKEBY),
    }
)


def get_registry():
    if chain.id == 1:
        return registry.eth
    elif chain.id == 137:
        return registry.poly
    elif chain.id == 56:
        return registry.bsc
    elif chain.id == 42161:
        return registry.arbitrum
    elif chain.id == 250:
        return registry.ftm


try:
    r = get_registry()
except AttributeError as e:
    if str(e) == "'NoneType' object has no attribute 'request_func'":
        # probably running brownie test where `chain.id` is not available yet
        r = registry.eth

# flatten nested dicts and invert the resulting key <-> value
# this allows for reversed lookup of an address
df = pd.json_normalize(registry, sep="_")
reverse = df.T.reset_index().set_index(0)["index"].to_dict()
