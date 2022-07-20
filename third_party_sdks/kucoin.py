"""Kucoin SDK"""

import base64
import hashlib
import hmac
import json
import time
from urllib import response
from urllib.parse import urlencode, urljoin
from uuid import uuid4

import requests

from sdk import SDK


class Kucoin(SDK):
    key: str
    secret: str
    passphrase: str
    signature: str

    def __init__(self, sand_box=False) -> None:
        if sand_box:
            self.base_url: str = "https://openapi-sandbox.kucoin.com/"
        else:
            self.base_url: str = "https://api.kucoin.com/"

    @property
    def now_as_mili(self) -> int:
        """Get time as miliseconds"""

        return int(time.time() * 1000)

    def set_key(self, key: str) -> None:
        self.key = key

    def set_secret(self, secret: str) -> None:
        self.secret = secret

    def set_passphrase(self, passphrase: str) -> None:
        self.passphrase = base64.b64encode(
            hmac.new(
                self.secret.encode("utf-8"),
                passphrase.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        )

    def dict_to_json(self, data) -> str:
        return json.dumps(data)

    def _generate_header(self) -> dict:
        """Generating header for request, based on the instance data

        Returns:
            dict: headers
        """

        headers: dict = {
            "KC-API-KEY": self.key,
            "KC-API-SIGN": self.signature,
            "KC-API-TIMESTAMP": str(self.now_as_mili),
            "KC-API-PASSPHRASE": self.passphrase,
            "KC-API-KEY-VERSION": "2",
            "Content-Type": "application/json",
        }
        return headers

    def _generate_signature(self, method: str, url: str, body="") -> None:
        """Generate a new signature based on the method name and URL and time,
        to confirm the request from Kucoin,
        [RUN BEFORE generate_header MEHTOD]

        Args:
            method (str) : method name like 'GET'
            url (str) : path of the target endpoint like '/api/v1/accounts'
            body (str) : body of request
        """

        url = "/" + url.strip().strip("/")  # normalize url
        str_to_sign = str(self.now_as_mili) + method.upper() + url + body

        self.signature = base64.b64encode(
            hmac.new(
                self.secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
            ).digest()
        )

    def post_query(self, url: str, **data: dict) -> requests.Response:
        """Send POST query to the API

        Args:
            url (str): path of endpoint
            data (dict, optional): body of request. Defaults to {}.

        Returns:
            requests.Response: result of query
        """

        method = "POST"
        data = self.dict_to_json(data)

        self._generate_signature(method, url, data)
        headers = self._generate_header()

        return self.raw_query(
            method,
            url,
            headers=headers,
            data=data,
        )

    def get_query(self, url: str, **parameters: dict) -> requests.Response:
        """Send GET Query to the API

        Args:
            url (str): path of endpoint
            parameters (dict, optional): parameters of url. Defaults to {}.

        Returns:
            requests.Response: result of query
        """

        method = "GET"
        if parameters != {}:
        # parameters should have the character "?" at the beginning of themself
            data = "?" + urlencode(parameters)
        else:
            data = ""

        self._generate_signature(method, url, data)

        headers = self._generate_header()
        return self.raw_query(
            method,
            url,
            headers=headers,
            parameters=parameters,
        )

    def raw_query(
        self,
        method: str,
        url: str,
        headers: dict = {},
        data: dict = {},
        parameters: dict = {},
    ) -> requests.Response:
        """Sending a raw request to the endpoint based on the method name and URL path

        Args:
            method (str): the method name : 'GET', 'POST' ...
            url (str): the path of endpoint : 'api/v1/accounts' ...
            header (dict, optional): headers of reqeust . Defaults to {}.
            data (dict, optional): sending some pyload beside the URL with Post, Put methods . Defaults to {}.
            parameters (dict, optional): sending some parameters beside the URL . Defaults to {}.

        Returns:
            Respoinse
        """

        full_url = urljoin(self.base_url, url)
        response = requests.request(
            method,
            full_url,
            headers=headers,
            data=data,
            params=parameters,
        )

        return response

    def get_account(self, accountID: str = None):
        """get all accounts or get a specified account with the id of that

        Args:
            accountID (str, optional): ID of account. Defaults is None.

        Returns:
            list : a list of accounts
            dict : details of account
        """

        path = "/api/v1/accounts"

        if accountID:
            path = path + "/" + accountID
            print(path)
            response = self.get_query(path)
            result = response.json()

        else:
            response = self.get_query(path)
            result = response.json()["data"]

        return result

    def new_position(self, **kwargs: dict):
        """apply for new positions

            Args :
                side (str) : buy or sell
                symbol (str) : a valid trading symbol code. e.g. ETH-BTC
                clientOid (str)	[Optional] : Unique order id created by users to identify their orders, e.g. UUID.
                type (str) [Optional] : limit or market (default is limit)
                remark (str) [Optional] : remark for the order, length cannot exceed 100 utf8 characters
                stp	(str) [Optional]: self trade prevention , CN, CO, CB or DC
                tradeType (str)	[Optional] : The type of trading : TRADE（Spot Trade） Default is TRADE.

            Addistional args based on type :
                type : market
                    size (str) [Optional] : Desired amount in base currency
                    funds (str) [Optional] : The desired amount of quote currency to use

                type : limit
                    price (str) : price per base currency
                    size (str) : amount of base currency to buy or sell
                    timeInForce	(str) [Optional] : GTC, GTT, IOC, or FOK (default is GTC), read Time In Force.
                    cancelAfter	(int) [Optional] : cancel after n seconds, requires timeInForce to be GTT
                    postOnly (bool) [Optional] : Post only flag, invalid when timeInForce is IOC or FOK
                    hidden (bool) [Optional] : Order will not be displayed in the order book
                    iceberg	(bool) [Optional] : Only aportion of the order is displayed in the order book
                    visibleSize	(str [Optional] : The maximum visible size of an iceberg order
        Raises:
            ValueError: pass invalid args or not passed requierd data
        """

        if not kwargs:
            raise ValueError(
                "See this link for more info : https://docs.kucoin.com/#place-a-new-order"
            )

        kwargs.setdefault("clientOid", str(uuid4()))
        path = "/api/v1/orders"
        response = self.post_query(path, **kwargs)
        print(response.json())



