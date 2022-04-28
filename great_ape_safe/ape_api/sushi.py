from great_ape_safe.ape_api.uni_v2 import UniV2
from helpers.addresses import registry


class Sushi(UniV2):
    def __init__(self, safe):
        self.safe = safe
        self.router = self.safe.contract(registry.eth.sushiswap.router_v2)
        self.factory = self.safe.contract(registry.eth.sushiswap.factory_v2)
