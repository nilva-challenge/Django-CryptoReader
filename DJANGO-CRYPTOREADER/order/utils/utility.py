import time

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
            # "KC-API-SIGN": 
            "KC-API-TIMESTAMP": str(int(time.time() * 1000)),
            "KC-API-KEY": self.user.get('kucoin_api_key'),
            "KC-API-PASSPHRASE": self.user.get('kucoin_pass_pharese'),
            "KC-API-KEY-VERSION": "2"
        }

    def create_request(self):
        if self.sandbox:
            return "https://openapi-sandbox.kucoin.com" + self.endpoint
        return "https://api.kucoin.com" + self.endpoint
