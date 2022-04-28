import json
import requests

from brownie import interface

from helpers.addresses import registry
from rich.console import Console


C = Console()


class Badger():
    """
    collection of all contracts and methods needed to interact with the badger
    system.
    """


    def __init__(self, safe):
        self.safe = safe

        # tokens
        self.badger = interface.IBadger(
            registry.eth.tokens.badger,
            owner=self.safe.account
        )

        # contracts
        self.tree = interface.IBadgerTreeV2(
            registry.eth.badger.tree,
            owner=self.safe.account
        )

        # misc
        self.api_url = 'https://api.badger.finance/v2/'


    def claim_all(self, json_file_path=None):
        """
        note: badger tree checks if `cycle` passed is equal to latest cycle,
        if not it will revert. therefore call is very time-sensitive!
        """

        if not json_file_path:
            url = self.api_url + 'reward/tree/' + self.safe.address

            # grab args from api endpoint
            response = requests.get(url)
            json_data = response.json()
        else:
            file = open(json_file_path)
            json_data = json.load(file)['claims'][self.safe.address]

        if 'message' in json_data.keys():
            if json_data['message'] == f'{self.safe.address} does not have claimable rewards.':
                return

        amounts_claimable = self.tree.getClaimableFor(
            self.safe.address,
            json_data['tokens'],
            json_data['cumulativeAmounts'],
        )[1]

        self.tree.claim(
            json_data['tokens'],
            json_data['cumulativeAmounts'],
            json_data['index'],
            json_data['cycle'],
            json_data['proof'],
            amounts_claimable,
        )
