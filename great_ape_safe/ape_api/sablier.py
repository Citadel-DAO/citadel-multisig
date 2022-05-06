from brownie import interface, chain

from helpers.addresses import registry

from rich.console import Console
from rich.pretty import pprint

console = Console()


class Sablier:
    """
    Methods needed to interact with Sablier to open stream, cancel stream and read their details.
    """

    def __init__(self, safe):
        self.safe = safe

        self.sablier_v1_1 = interface.ISablier(
            registry.eth.sablier if chain.id == 1 else registry.rinkeby.sablier,
            owner=self.safe.account,
        )

    def get_stream(self, stream_id):
        stream_info = self.sablier_v1_1.getStream(stream_id)

        console.print(f"==== Stream ID [green]{stream_id}[/green] ====\n")
        pprint(stream_info.dict())

    def cancel_stream(self, stream_id):
        assert self.sablier_v1_1.cancelStream(stream_id).return_value

    def create_stream(self, recipient, deposit, token_address, start_time, end_time):
        # interesting "limitation": https://etherscan.io/address/0xCD18eAa163733Da39c232722cBC4E8940b1D8888#code#F6#L199
        self.sablier_v1_1.createStream(
            recipient, deposit, token_address, start_time, end_time
        )
