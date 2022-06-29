from brownie import Avatar, accounts
from dotmap import DotMap
from gnosis.safe.multi_send import MultiSend, MultiSendOperation, MultiSendTx

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main():
    safe = GreatApeSafe(registry.eth.citadel.treasury_vault)
    cvx = safe.contract(registry.eth.tokens.cvx)
    bvecvx = safe.contract(registry.eth.badger.bvecvx)

    # sim deployment
    avatar = Avatar.deploy({'from': accounts[0]})
    avatar.initialize(registry.eth.citadel.gac, safe, {'from': accounts[0]})
    
    # sim whitelisting
    bvecvx.approveContractAccess(avatar, {'from': bvecvx.governance()})

    print(cvx.balanceOf(safe), cvx.balanceOf(avatar), bvecvx.balanceOf(avatar))

    cvx.transfer(avatar, cvx.balanceOf(safe))

    print(cvx.balanceOf(safe), cvx.balanceOf(avatar), bvecvx.balanceOf(avatar))

    avatar_todo = [
        DotMap({
            'receiver': cvx.address,
            'value': 0,
            'input': cvx.approve.encode_input(bvecvx, cvx.balanceOf(avatar)),
        }),
        DotMap({
            'receiver': bvecvx.address,
            'value': 0,
            'input': bvecvx.depositAll.encode_input()
        })
    ]

    txs = [MultiSendTx(MultiSendOperation.CALL, tx.receiver, tx.value, tx.input) for tx in avatar_todo]
    calldata = MultiSend(safe.multisend, safe.ethereum_client).build_tx_data(txs)
    # calldata = cvx.transfer.encode_input(safe, cvx.balanceOf(avatar))
    # avatar.call(cvx, 0, calldata, {'from': safe.account})
    
    avatar.call(safe.multisend, 0, calldata, {'from': safe.account})

    print(cvx.balanceOf(safe), cvx.balanceOf(avatar), bvecvx.balanceOf(avatar))

    safe.post_safe_tx(skip_preview=True)
