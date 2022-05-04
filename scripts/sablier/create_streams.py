from datetime import datetime
from datetime import timezone
import os
import pandas as pd

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main(csv_file="stream_recipients_example"):
    safe = GreatApeSafe(registry.eth.citadel.policy_ops)
    safe.init_sablier()

    df = pd.read_csv(f"{os.path.dirname(__file__)}/{csv_file}.csv")

    total_approval_amts = df.groupby("token_address")["stream_amount"].sum()

    for addr, amt in total_approval_amts.items():
        erc20 = safe.contract(addr)
        erc20.approve(safe.sablier.sablier_v1_1, amt * 10 ** erc20.decimals())

    for _, row in df.iterrows():
        starting_time_ts = datetime.strptime(row["start_time"], "%Y-%m-%d")
        ending_time_ts = datetime.strptime(row["ending_time"], "%Y-%m-%d")

        erc20 = safe.contract(row["token_address"])
        safe.sablier.create_stream(
            row["recipient"],
            row["stream_amount"] * 10 ** erc20.decimals(),
            row["token_address"],
            int(starting_time_ts.replace(tzinfo=timezone.utc).timestamp()),
            int(ending_time_ts.replace(tzinfo=timezone.utc).timestamp()),
        )

    safe.post_safe_tx()
