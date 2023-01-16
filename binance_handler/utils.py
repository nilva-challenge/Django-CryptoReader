import time
from binance import Client


def binance_api_list_of_open_positions(key, secret):
    client = Client(key, secret)
    return client.futures_account()['positions']