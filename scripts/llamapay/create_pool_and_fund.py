from great_ape_safe import GreatApeSafe
from helpers.addresses import r


def main(token="usdc", amount=20):
    governance = GreatApeSafe(r.citadel.governance)
    governance.init_llamapay()

    governance.llamapay.create_pool(r.tokens[token])

    governance.llamapay.deposit_funds(int(amount), r.tokens[token])

    governance.post_safe_tx()
