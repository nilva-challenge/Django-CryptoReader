import time
import base64
import hashlib
import hmac
import time
import requests
from accounts.encryption import decrypt


def kucoin_api(key, secret, passphrase, endpoint, params) -> tuple:
    '''
        Get data from kucoin with specefic header
    '''

    url = 'https://api.kucoin.com' + endpoint

    # decrypt data
    key = decrypt(key)
    secret = decrypt(secret)
    passphrase = decrypt(passphrase)

    # create signature
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + endpoint + '?' + params
    signature = base64.b64encode(
        hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(secret.encode('utf-8'),
                 passphrase.encode('utf-8'),
                 hashlib.sha256).digest())

    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }

    response = requests.request('get', url, headers=headers, params=params)
    return response.status_code, response.json()
