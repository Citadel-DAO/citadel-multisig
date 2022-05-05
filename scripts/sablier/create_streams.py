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

    df["stream_amount"] = df.apply(
        lambda row: row["stream_amount"]
        * 10 ** safe.contract(row["token_address"]).decimals(),
        axis=1,
    )
    df["stream_amount"].mask(
        df["stream_amount"]
        % (
            df["ending_time"].apply(lambda x: _date_to_ts(x))
            - df["start_time"].apply(lambda x: _date_to_ts(x))
        )
        != 0,
        _acceptable_amount(
            df["stream_amount"],
            df["ending_time"].apply(lambda x: _date_to_ts(x))
            - df["start_time"].apply(lambda x: _date_to_ts(x)),
        ),
        inplace=True,
    )

    total_approval_amts = df.groupby("token_address")["stream_amount"].sum()
    for addr, amt in total_approval_amts.items():
        erc20 = safe.contract(addr)
        erc20.approve(safe.sablier.sablier_v1_1, amt)

    for _, row in df.iterrows():
        safe.sablier.create_stream(
            row["recipient"],
            row["stream_amount"],
            row["token_address"],
            _date_to_ts(row["starting_time"]),
            _date_to_ts(row["ending_time"]),
        )

    safe.post_safe_tx()


def _date_to_ts(str_date):
    dt = datetime.strptime(str_date, "%Y-%m-%d")
    return int(dt.replace(tzinfo=timezone.utc).timestamp())


def _acceptable_amount(amount, interval):
    return amount - (amount % interval)
