from datetime import datetime, timezone, timedelta
import hmac, hashlib
import requests
import json

spot_base_url = "https://testnet.binance.vision"
key = "VWYU5oZL950Wshm8VPLSYyFh5tlqEtMvWbbHYWipQdOVSCzV62RH2N2Z7dVzAUEq"
secret = "JK2IWqNsHxaimzbIN1GO8w2LzeWcC9A2qQrGQo2bBEH2SJ63MHJSStNly7iTJN7X"


def create_query_string():
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000
    queryString = "&timestamp=" + str(posix_timestamp_millis) + "&symbol=BTC"
    return queryString


def create_signature():
    queryString = create_query_string()
    print(secret)
    signature = hmac.new(secret.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    return signature


def features_binance_account_data():
    query_string = create_query_string()
    signature = create_signature()
    end_point = "/sapi/v1/sub-account/list"
    url = spot_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"
    return requests.get(url, headers={'X-MBX-APIKEY': key}).content


print(features_binance_account_data())
