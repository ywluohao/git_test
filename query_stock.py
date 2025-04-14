#!/Users/haoluo/venv/stock/bin/python3
import argparse

# avoid the confusing warning message
import logging
import math
import os
import time
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pretty_errors
import yagmail
import yfinance as yf
from emoji import emojize
from tabulate import tabulate
import humanize
from tqdm import tqdm
from pprint import pprint as pp
import shutil


def download_stock_price(ticker, absolute_date=False, a1="", a2="", r1=5, r2=3, full=False, format="series"):
    if absolute_date:
        start_date = a1
        end_date = a2
    else:
        start_date = data_d - timedelta(days=r1)
        end_date = data_d + timedelta(days=r2)

    df = yf.Ticker(ticker).history(start=start_date, end=end_date).rename(columns={"Close": "adjclose", "Open": "open", "High": "high", "Low": "low"})
    df.index.name = "date"
    df.index = df.index.tz_localize(None)

    if full:
        return df
    df_series = df["adjclose"].round(2)
    if format == "list":
        return df_series.tolist()
    elif format == "df":
        return df_series.to_frame()
    elif format == "series":
        return df_series
    else:
        raise ValueError(f"result_format {format} is not supported")


def query_price(t):
    if "-" in t:
        ticker, _, price = t.partition("-")
        price = float(price)
    else:
        ticker = t

    data_raw = download_stock_price(ticker=ticker, r1=370, r2=3, full=True).round(2).sort_index(ascending=False).reset_index()
    data_30d_full = data_raw[["date", "low", "high", "adjclose"]].head(30).copy()

    if "-" not in t:
        price = data_30d_full["adjclose"].iloc[0]

    global_high = max(price, data_30d_full["high"].max())
    global_low = min(price, data_30d_full["low"].min())

    data_30d_full["range"] = data_30d_full.apply(
        lambda r: price_indicator_with_ranges(price, r["low"], r["high"], global_low, global_high, r["adjclose"], width=30), axis=1
    )

    data_30d_full["daily"] = (data_30d_full["adjclose"] / data_30d_full["adjclose"].shift(-1) - 1).apply(
        lambda x: "{:+.2%}".format(x) if pd.notnull(x) else x
    )
    data_30d_full["cul"] = price / data_30d_full["adjclose"] - 1
    data_30d_full.loc[1:, "avg"] = data_30d_full.loc[1:, "cul"] / data_30d_full.index[1:]
    data_30d_full["cul"] = data_30d_full["cul"].apply(lambda x: "{:+.2%}".format(x))
    data_30d_full["avg"] = data_30d_full["avg"].apply(lambda x: "{:+.2%}".format(x))

    past_n_days = data_30d_full[["date"]].head(3)
    past_n_days["print"] = past_n_days["date"].dt.strftime("%a_%m%d") + f"_{price}"

    def comment(d, c):
        c = float(c.replace("%", ""))
        if c > 0:
            c = math.floor(c)
            a = "up"
        else:
            c = -math.ceil(c)
            a = "down"
        return f"{d}-day {a} {c}%"

    for i in range(past_n_days.shape[0]):
        data_30d_full[past_n_days.iloc[i, 1]] = ""

    index_cul = data_30d_full.columns.get_loc("cul")
    index_last = data_30d_full.columns.get_loc("avg")

    for i in range(past_n_days.shape[0]):
        for j in range(data_30d_full.shape[0] - 1):
            if j >= i:

                data_30d_full.iloc[j, i + index_last + 1] = comment(j + 1 - i, data_30d_full.iloc[j + 1, index_cul])

    print(data_30d_full)

    prices = data_raw["adjclose"]
    n_price = prices.shape[0]

    periods = [3, 5, 10, 20, 60, 120, 250]
    periods = [p for p in periods if p < n_price]
    metrics = pd.DataFrame(index=periods, columns=["price", "price ratio", "avg", "avg ratio", "barrier", "barrier ratio"])

    def format_digits(value, digit):
        return f"{value:.{digit-1}f}"[:digit]

    for p in periods:
        end_price = prices.loc[p - 1]
        avg_price = prices.head(p).mean()
        metrics.loc[p, "price"] = f"{p}-d end: {format_digits(end_price, 4)}"
        metrics.loc[p, "price ratio"] = f"{p}-d end: {format_digits(price/end_price* 100, 3)}%"
        metrics.loc[p, "avg"] = f"{p}-d avg: {format_digits(avg_price, 4)}"
        metrics.loc[p, "avg ratio"] = f"{p}-d avg: {format_digits(price / avg_price* 100, 3)}%"
        metrics.loc[p, "barrier"] = f"{p}-d bar: {sum(pp <= price for pp in prices.head(p)) -1: <3} "
        metrics.loc[p, "barrier ratio"] = f"{p}-d bar: {(format_digits((sum(pp <= price for pp in prices.head(p)) -1)/ (p-1)* 100, 3))}%"

    for row in metrics.T.values.tolist():
        print("     ".join(row))


def price_indicator_with_ranges(current_price, local_min, local_max, global_min, global_max, local_close, width=30):
    # Scale positions to the global range and ensure they are within bounds
    global_start = int((local_min - global_min) / (global_max - global_min) * width)
    global_end = int((local_max - global_min) / (global_max - global_min) * width)
    current_position = int((current_price - global_min) / (global_max - global_min) * width)
    local_close_position = int((local_close - global_min) / (global_max - global_min) * width)

    # Clamp the positions to the range [0, width-1]
    global_start = max(0, min(global_start, width - 1))
    global_end = max(0, min(global_end, width - 1))
    current_position = max(0, min(current_position, width - 1))
    local_close_position = max(0, min(local_close_position, width - 1))

    # Create the global bar (initialize with spaces)
    bar = [" "] * width

    # Fill the local range with '='
    for i in range(global_start, global_end + 1):
        bar[i] = "-"

    # Mark the local close with '*'
    bar[local_close_position] = "="

    # Mark the current price with '|'
    bar[current_position] = "|"

    # Construct the output
    return f"[{''.join(bar)}]"


data_d = (datetime.now() + timedelta(days=1)) if datetime.now().hour > 15 else datetime.now()


parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=35))
parser.add_argument("stock")
args = parser.parse_args()


query_price(args.stock.upper())
