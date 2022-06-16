from brownie import interface, exceptions, chain

from helpers.addresses import r
from great_ape_safe.ape_api.helpers.llamapay.queries import stream_query

from datetime import timedelta
import requests
import json
from rich.console import Console

console = Console()

class LlamaPay:
    """
    Collection of methods to interact with LlamaPay
    repo: https://github.com/LlamaPay/llamapay
    """

    def __init__(self, safe):
        self.safe = safe

        self.factory = interface.IFactoryLlama(
            r.llamapay.factory, owner=self.safe.account
        )

        # https://docs.llamapay.io/llamapay/features/precision
        self.PRECISION = 10 ** 20

        self.subgraph = "https://api.thegraph.com/subgraphs/name/nemusonaneko/llamapay-mainnet"

    def get_safe_streams(self, update_cache=False):
        # get all streams from safe from subgraph
        if update_cache:
            res = requests.post(self.subgraph, json={'query': stream_query.format(safe=self.safe.address)})
            streams = res.json()['data']['user']['streams']

            with open('great_ape_safe/ape_api/helpers/llamapay/streams.json') as f:
                safe_streams = json.load(f)
                safe_streams['safes'][self.safe.address] = streams

            with open('great_ape_safe/ape_api/helpers/llamapay/streams.json', 'w') as f:
                json.dump(safe_streams, f, indent=4)

            return streams

        with open('great_ape_safe/ape_api/helpers/llamapay/streams.json') as f:
            try:
                return json.load(f)['safes'][self.safe.address]
            except KeyError:
                raise Exception("Safe has no outgoing streams")

    def _get_rate(self, amount, stream_days_duration):
        seconds = int(timedelta(days=stream_days_duration).total_seconds())
        # https://github.com/LlamaPay/llamapay/blob/master/contracts/LlamaPay.sol#L16
        return int((amount * self.PRECISION) / seconds)

    def get_pool(self, token_address):
        pool_address, is_deployed = self.factory.getLlamaPayContractByToken(
            token_address
        )
        if is_deployed:
            return interface.IPoolLlama(pool_address, owner=self.safe.account)
        else:
            console.print(
                f" === Pool for token ({token_address}) has not being deployed === \n"
            )

    def create_pool(self, token_address):
        try:
            # deterministic: https://github.com/LlamaPay/llamapay/blob/master/contracts/LlamaPayFactory.sol#L26
            self.factory.createLlamaPayContract(token_address)
        except exceptions.VirtualMachineError:
            # avoid revert GS013, if `createLlamaPayContract` cause pool already exist
            chain.reset()
            console.print(
                f" === Pool exist already, address: {self.get_pool(token_address).address} === \n"
            )

    def deposit_funds(self, amount, token_address):
        pool = self.get_pool(token_address)

        token = interface.ERC20(token_address, owner=self.safe.account)

        amount_mantissa = amount * 10 ** token.decimals()

        token.approve(pool, amount_mantissa)

        pool.deposit(amount_mantissa)

    def withdraw_funds(self, amount, token_address, all_funds=False):
        pool = self.get_pool(token_address)

        if all_funds:
            pool.withdrawPayerAll()
        else:
            token = interface.ERC20(token_address, owner=self.safe.account)
            amount_mantissa = amount * 10 ** token.decimals()
            pool.withdrawPayer(amount_mantissa)

    def create_stream(self, recipient, amount, stream_days_duration, token_address):
        pool = self.get_pool(token_address)

        amount_per_sec = self._get_rate(amount, stream_days_duration)

        # https://github.com/LlamaPay/llamapay/blob/master/contracts/LlamaPay.sol#L91
        pool.createStream(recipient, amount_per_sec)

    def cancel_stream(self, recipient, token_address, rate=None):
        pool = self.get_pool(token_address)
        streams = self.get_safe_streams()
        has_multiple_streams = [x['payee']['address'] for x in streams].count(recipient) > 1

        # a 'unique' stream is derived from payer, payee and rate
        # so rate has to be provided if there are multiple streams for recipient
        # https://etherscan.io/address/0x60c7B0c5B3a4Dc8C690b074727a17fF7aA287Ff2#code#F1#L59
        if has_multiple_streams and not rate:
            # print recipient streams & rates
            console.print(f"{recipient} streams:")
            for stream in [x['payee']['address'] for x in streams if x['payee']['address'] == recipient]:
                console.print(f"{stream['streamId']}: {stream['amountPerSec']}")

            raise Exception(f'Multiple streams for {recipient} but rate not provided')

        for stream in streams:
            if stream['payee']['address'] == recipient:
                queried_rate = stream['amountPerSec']
                if not rate:
                    pool.cancelStream(recipient, queried_rate)
                    return
                if rate == queried_rate:
                    pool.cancelStream(recipient, rate)
                    return

        raise Exception(f'No stream found for {recipient}')
