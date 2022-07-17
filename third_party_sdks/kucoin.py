"""Kucoin SDK"""

import base64
import hashlib
import hmac
import time

import requests
from requests.compat import urljoin


class Kucoin:
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

    def authenticate(self):
        ...

    def generate_header(self) -> dict:
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
        }
        return headers

    def generate_signature(self, method: str, url: str) -> None:
        """Generate a new signature based on the method name and URL and time,
        to confirm the request from Kucoin

        Args:
            method (str) : method name like 'GET'
            url (str) : path of the target endpoint like 'api/v1/accounts'
        """

        url = "/" + url.strip("/")  # normalize url

        str_to_sign = str(self.now_as_mili) + method.upper() + url
        print(str_to_sign)
        self.signature = base64.b64encode(
            hmac.new(
                self.secret.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha256
            ).digest()
        )

    def raw_query(
        self, method: str, url: str, parameters: dict = {}
    ) -> requests.Response:
        """Sending a raw request to the endpoint based on the method name and URL path

        Args:
            method (str): the method name : 'GET', 'POST' ...
            url (str): the path of endpoint : 'api/v1/accounts' ...
            parameters (dict, optional): sending some parameters beside the URL . Defaults to {}.

        Returns:
            Respoinse
        """
        self.generate_signature(method, url)

        full_url = urljoin(self.base_url, url)
        print(full_url)
        headers = self.generate_header()
        reqeust = requests.request(method, full_url, headers=headers, params=parameters)
        return reqeust


