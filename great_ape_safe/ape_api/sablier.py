from brownie import interface

from helpers.addresses import registry
from great_ape_safe.ape_api.helpers.miscellaneous_methods import closest_number

from rich.console import Console
from rich.pretty import pprint

console = Console()


class Sablier:
    """
    Methods needed to interact with Sablier to open streams and read their details.
    """

    def __init__(self, safe):
        self.safe = safe

        self.sablier_v1_1 = interface.ISablier(
            registry.eth.sablier, owner=self.safe.account
        )

    def get_stream(self, stream_id):
        stream_info = self.sablier_v1_1.getStream(stream_id)

        console.print(f"==== Stream ID [green]{stream_id}[/green] ====\n")
        pprint(stream_info.dict())

    def create_stream(self, recipient, deposit, token_address, start_time, end_time):
        duration = end_time - start_time
        if deposit % duration == 0:
            self.sablier_v1_1.createStream(
                recipient, deposit, token_address, start_time, end_time
            )
        else:
            # "limitation": https://etherscan.io/address/0xCD18eAa163733Da39c232722cBC4E8940b1D8888#code#F6#L199
            deposit_suitable = closest_number(deposit, duration)
            self.sablier_v1_1.createStream(
                recipient, deposit_suitable, token_address, start_time, end_time
            )
