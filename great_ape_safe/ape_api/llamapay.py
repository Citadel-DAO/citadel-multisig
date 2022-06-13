from brownie import interface, exceptions, chain

from helpers.addresses import r

from datetime import timedelta


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
            print(
                f" === Pool for token ({token_address}) has not being deployed === \n"
            )

    def create_pool(self, token_address):
        try:
            # deterministic: https://github.com/LlamaPay/llamapay/blob/master/contracts/LlamaPayFactory.sol#L26
            self.factory.createLlamaPayContract(token_address)
        except exceptions.VirtualMachineError:
            # avoid revert GS013, if `createLlamaPayContract` cause pool already exist
            chain.reset()
            print(
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

    def cancel_stream(self, recipient, rate, token_address):
        pool = self.get_pool(token_address)

        # here we should have either a json saving events emitted by the stream creation
        # to grab the rate. similar for pausing and modifying...
        # https://github.com/LlamaPay/llamapay/blob/master/contracts/LlamaPay.sol#L93
        pool.cancelStream(recipient, rate)
