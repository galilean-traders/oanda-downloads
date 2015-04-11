"""download the candles from fxpractice.oanda.com with no time limits, by
chaining multiple requests."""

import datetime
import time
import requests
import json

import click

duration = {
    "M5": datetime.timedelta(minutes=5),
    "D": datetime.timedelta(days=1),
}

@click.command()
@click.option(
    "--oanda-token",
    default="885ac2b8ad30d2292610ecb707431155-32bf7c56bb3db61696674160b00fa68c",
    help="access token for the oanda fxpractice api"
)
@click.option("--instrument", default="EUR_USD",
              help="request candles for this instrument")
@click.option("--granularity", type=click.Choice(["M5", "D"]), default="M5")
def download_candles(oanda_token, instrument, granularity):
    """

    :oanda_token: a valid fxpractice token
    :instrument: an oanda instrument e.g. EUR_USD
    :granularity: http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory

    """

    url = "https://api-fxpractice.oanda.com/v1/candles"
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2014, 12, 31, 23, 59, 59)
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
        candles.extend(response.json()["candles"])
        time.sleep(0.5)
        current += delta
    print(json.dumps(candles))
