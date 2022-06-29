import sys

def test_create_and_withdraw_flow(safe, usdc, payee):
    safe.init_llamapay()

    safe.llamapay.create_pool(usdc)
    safe.llamapay.create_stream(payee, 100, 30, usdc)

    safe.llamapay.deposit_funds(1000, usdc)

    safe.llamapay.withdraw_funds(1000, usdc)
    safe.llamapay.withdraw_funds(0, usdc, all_funds=True)

def test_subgraph(safe):
    safe.init_llamapay()
    assert len(safe.llamapay.streams) > 0

    stream = safe.llamapay.streams[0] 
    assert stream['streamId']
    assert stream['amountPerSec']
    assert stream['payee']['address']

def test_cancel_stream(safe, dai, payee):
    safe.init_llamapay()
    safe.llamapay.cancel_stream(payee, dai, rate=385802469135802469)

def test_cancel_stream_no_rate(safe, dai, payee2):
    # requires user input, only run if called with -s
    if '-s' in sys.argv:
        safe.init_llamapay()
        safe.llamapay.cancel_stream(payee2, dai)
