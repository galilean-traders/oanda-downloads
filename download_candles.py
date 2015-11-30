"""download the candles from fxpractice.oanda.com with no time limits, by
chaining multiple requests."""

import datetime
import time
import requests
import json
import sys

import click

duration = {
    "M1": datetime.timedelta(minutes=1),
    "M5": datetime.timedelta(minutes=5),
    "D": datetime.timedelta(days=1),
}

# http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory
granularities = [
    "S5", # 5 seconds
    "S10", # 10 seconds
    "S15", # 15 seconds
    "S30", # 30 seconds
    "M1", # 1 minute
    "M2", # 2 minutes
    "M3", # 3 minutes
    "M4", # 4 minutes
    "M5", # 5 minutes
    "M10", # 10 minutes
    "M15", # 15 minutes
    "M30", # 30 minutes
    "H1", # 1 hour
    "H2", # 2 hours
    "H3", # 3 hours
    "H4", # 4 hours
    "H6", # 6 hours
    "H8", # 8 hours
    "H12", # 12 hours
    "D", # 1 Day
    "W", # 1 Week
    "M", # 1 Month
]

@click.command()
@click.option(
    "--oanda-token",
    default="885ac2b8ad30d2292610ecb707431155-32bf7c56bb3db61696674160b00fa68c",
    help="access token for the oanda fxpractice api"
)
@click.option("--instrument", default="EUR_USD",
              help="request candles for this instrument")
@click.option("--granularity", type=click.Choice(granularities), default="M5")
@click.option("--begin", type=int, default=2013)
@click.option("--end", type=int, default=2015)
def download_candles(oanda_token, instrument, granularity, begin, end):
    """

    :oanda_token: a valid fxpractice token
    :instrument: an oanda instrument e.g. EUR_USD
    :granularity: http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory

    """

    url = "https://api-fxpractice.oanda.com/v1/candles"
    start = datetime.datetime(begin, 1, 1)
    end = datetime.datetime(end - 1, 12, 31, 23, 59, 59)
    headers = {"Authorization": "Bearer " + oanda_token}
    params = {
        "instrument": instrument,
        "granularity": granularity,
    }
    current = start
    delta = 4500 * duration[granularity]
    candles = []
    while current < end:
        params["start"] = current.isoformat()
        params["end"] = (current + delta).isoformat()
        response = requests.get(url, params=params, headers=headers)
        candle = response.json()["candles"]
        print(candle[0]["time"], file=sys.stderr)
        candles.extend(candle)
        time.sleep(0.5)
        current += delta
    print(json.dumps(candles))
