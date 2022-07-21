import base64
import time
import hmac
import requests
import hashlib

# fetch data from kucoin 
def api_kucoin(api_key, api_secret, api_passphrase, endpoint):
    api_key = api_key
    api_secret = api_secret
    api_passphrase = api_passphrase
    url = 'https://api.kucoin.com' + endpoint
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + endpoint
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request('get', url, headers=headers)
    return response.status_code, response.json()
