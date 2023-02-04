from datetime import datetime, timezone, timedelta
import hmac, hashlib
import requests
import json

spot_base_url = "https://testnet.binance.vision"
key = "rtesypEYwMiiSAeeiWRoYik7vSp66lUprbKoD788Z6vvSQNqj4EVXHNvtU0Xqsfi"
secret = "rLtP7i2JNmYEouOfj84kLO9V3esiuUojLq7DA2fHBxlQkBIK12H89I4OR6xFeUgz"


def create_query_string():
    now = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    posix_timestamp_micros = (now - epoch) // timedelta(microseconds=1)
    posix_timestamp_millis = posix_timestamp_micros // 1000
    queryString = "&timestamp=" + str(posix_timestamp_millis)
    return queryString


def create_signature():
    queryString = create_query_string()
    signature = hmac.new(secret.encode(), queryString.encode(), hashlib.sha256).hexdigest()
    return signature


def features_binance_account_data():
    query_string = create_query_string()
    signature = create_signature()
    end_point = "/fapi/v2/balance"
    url = spot_base_url + end_point
    url = url + f"?{query_string}&signature={signature}"
    data = requests.get(url, headers={'X-MBX-APIKEY': key}).json()
    return data

print(features_binance_account_data())
