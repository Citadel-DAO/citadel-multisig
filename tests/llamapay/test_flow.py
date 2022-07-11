import sys
import warnings

def test_create_and_withdraw_flow(safe, usdc, payee):
    safe.llamapay.create_pool(usdc)
    safe.llamapay.create_stream(payee, 100, 30, usdc)

    safe.llamapay.deposit_funds(1000, usdc)

    safe.llamapay.withdraw_funds(1000, usdc)
    safe.llamapay.withdraw_funds(0, usdc, all_funds=True)

def test_cancel_stream(safe, payee, usdc):
    rate = safe.llamapay._get_rate(100, 30)
    safe.llamapay.cancel_stream(payee, usdc, rate=rate, use_subgraph=False)

def test_subgraph(safe):
    assert len(safe.llamapay.streams) > 0

    stream = safe.llamapay.streams[0] 
    assert stream['streamId']
    assert stream['amountPerSec']
    assert stream['payee']['address']

def test_cancel_stream_subgraph(safe, dai, payee):
    streams = safe.llamapay.streams_for(payee, token=dai)
    if len(streams) == 0:
        warnings.warn(f"No active dai streams for {payee}")

    for stream in streams:
        safe.llamapay.cancel_stream(payee, dai, rate=int(stream['amountPerSec']))

def test_cancel_stream_no_rate(safe, dai, payee2):
    # requires user input, only run if called with -s
    if '-s' in sys.argv:
        safe.init_llamapay()
        if len(safe.llamapay.streams_for(payee2, token=dai)) > 0:
            safe.llamapay.cancel_stream(payee2, dai)
        else:
            warnings.warn(f"No active dai streams for {payee2}")

