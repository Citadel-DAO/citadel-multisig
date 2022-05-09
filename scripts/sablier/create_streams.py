import os
import numpy as np
import pandas as pd

from great_ape_safe import GreatApeSafe
from helpers.addresses import registry


def main(csv_file="stream_recipients_example"):
    safe = GreatApeSafe(registry.eth.citadel.treasury_ops) # vault?
    safe.init_sablier()

    df = pd.read_csv(
        f"{os.path.dirname(__file__)}/{csv_file}.csv",
        parse_dates=['start_time', 'end_time']
    )

    df["ts_start"] = df['start_time'].astype(np.int64) // 10 ** 9
    df["ts_end"] = df['end_time'].astype(np.int64) // 10 ** 9
    df["interval"] = df["ts_end"] - df["ts_start"]

    df["streamable_mantissa"] = df.apply(
        lambda row: row["stream_amount"]
        * 10 ** safe.contract(row["token_address"]).decimals(),
        axis=1,
    )
    df["streamable_mantissa"] = df["streamable_mantissa"].mask(
        df["streamable_mantissa"] % df["interval"] != 0,
        df["streamable_mantissa"] - (df["streamable_mantissa"] % df["interval"])
    )

    total_approval_amts = df.groupby("token_address")["streamable_mantissa"].sum()
    for addr, amt in total_approval_amts.items():
        erc20 = safe.contract(addr)
        erc20.approve(safe.sablier.sablier_v1_1, amt)

    df.to_csv(f"{os.path.dirname(__file__)}/{csv_file}_processed.csv", index=False)

    for _, row in df.iterrows():
        safe.sablier.create_stream(
            row["recipient"],
            row["streamable_mantissa"],
            row["token_address"],
            row["ts_start"],
            row["ts_end"]
        )

    safe.post_safe_tx()
