import time
import base64
import hashlib
import hmac
import time
import urllib.parse
import requests
from account.utils.utility import encrypt_message


class CallAPI():
    """ 
    every thing base on this documentation:
    https://www.kucoin.com/support/900006465403-KuCoin-API-key-upgrade-operation-guide
    """

    def __init__(self, user, endpoint, http_method, query_params, sandbox):
        self.user = user
        self.endpoint = endpoint
        self.http_method = http_method
        self.query_params = query_params
        self.sandbox = sandbox

    def create_signature(self):
        """
        Use API-Secret to encrypt the prehash string 
        {timestamp + method + endpoint + body} with sha256 HMAC.
        The request body is a JSON string and needs to be the same as the parameters passed by the API
        """
        api_secret = encrypt_message(self.user.get('kucoin_api_secret'))
        str_to_sign = str(time.time() * 1000) + self.method + \
            self.endpoint + '?' + urllib.parse.urlencode(self.params)
        signature = base64.b64encode(
            hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        return signature

    def create_header(self):
        """
        All private REST requests must contain the following headers: 
        KC-API-KEY The API key as a string. 
        KC-API-SIGN The base64-encoded signature (see Signing a Message). 
        KC-API-TIMESTAMP A timestamp for your request. 
        KC-API-PASSPHRASE The passphrase you specified when creating the API key. 
        KC-API-KEY-VERSION You can check the version of API key on the page of API Management

        """
        return {
            "KC-API-SIGN": self.create_signature(),
            "KC-API-TIMESTAMP": str(int(time.time() * 1000)),
            "KC-API-KEY": encrypt_message(self.user.get('kucoin_api_key')),
            "KC-API-PASSPHRASE": encrypt_message(self.user.get('kucoin_pass_pharese')),
            "KC-API-KEY-VERSION": "2"
        }

    def create_request(self):
        if self.sandbox:
            base_url = "https://openapi-sandbox.kucoin.com" + self.endpoint
        base_url = "https://api.kucoin.com" + self.endpoint

        response = requests.request(
            self.http_method, base_url, headers=self.create_header(), params=self.params)
        if response.status_code != 200:
            raise Exception('Error Happned')
        return response.json()
