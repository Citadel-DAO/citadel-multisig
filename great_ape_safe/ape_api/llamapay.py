from decimal import Decimal
from brownie import interface

from helpers.addresses import r
from great_ape_safe.ape_api.helpers.llamapay.queries import construct_query

from datetime import timedelta
import requests
from rich.console import Console
import click

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
        self.PRECISION = Decimal(10 ** 20)
        self.subgraph = "https://api.thegraph.com/subgraphs/name/nemusonaneko/llamapay-mainnet"
        self.streams = self.get_safe_streams()

    def get_safe_streams(self):
        # get all streams from safe from subgraph
        res = requests.post(self.subgraph, json={"query": construct_query(self.safe.address)})
        streams = res.json()["data"]["user"]["streams"]
        streams = [x for x in streams if x["active"]]
        return streams

    def _get_rate(self, amount, stream_days_duration):
        seconds = int(timedelta(days=stream_days_duration).total_seconds())
        # https://github.com/LlamaPay/llamapay/blob/master/contracts/LlamaPay.sol#L16
        return int((amount * self.PRECISION) / seconds)

    def get_pool(self, token_address):
        pool_address, is_deployed = self.factory.getLlamaPayContractByToken(
            token_address
        )
        assert is_deployed, f"Pool not deployed for token: {token_address}"

        return interface.IPoolLlama(pool_address, owner=self.safe.account)
 
    def create_pool(self, token_address):
        pool_address, is_deployed = self.factory.getLlamaPayContractByToken(
            token_address
        )
        if not is_deployed:
            self.factory.createLlamaPayContract(token_address)
        else:
            console.print(
                f" === Pool exist already, address: {pool_address} === \n")

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

    def cancel_stream(self, recipient, token_address, rate=None, update_streams=False):
        if update_streams:
            self.streams = self.get_safe_streams()

        assert len(self.streams) > 0, "No streams to cancel"

        pool = self.get_pool(token_address)
        recipient = recipient.lower()

        num_recipient_streams = [x["payee"]["address"] for x in self.streams].count(recipient)
        assert num_recipient_streams > 0, "No streams to cancel"
    
        has_multiple_streams = num_recipient_streams > 1

        # a "unique" stream for pool is derived from payer, payee and rate
        # so rate has to be provided if there are multiple streams for recipient
        # https://etherscan.io/address/0x60c7B0c5B3a4Dc8C690b074727a17fF7aA287Ff2#code#F1#L59
        if has_multiple_streams and not rate:
            def monthly_rate(amount_per_sec):
                return (Decimal(amount_per_sec["amountPerSec"]) * Decimal(2.628e6)) / self.PRECISION

            rates = [monthly_rate(x) for x in self.streams if x["payee"]["address"] == recipient]

            rate = click.prompt(
                    "Select monthly rate:",
                    type=click.Choice(
                        rates
                    ),
                    show_default=False,
                    value_proc=lambda x: int((Decimal(x) / Decimal(2.628e6)) * self.PRECISION)
                )

        for stream in self.streams:
            if stream["payee"]["address"] == recipient:
                queried_rate = int(stream["amountPerSec"])
                if not rate:
                    pool.cancelStream(recipient, queried_rate)
                    return
                if rate == queried_rate:
                    pool.cancelStream(recipient, rate)
                    return
    
        raise Exception(f"No stream found for {recipient}")
