from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests


class InternalException(Exception):
    pass


class RequestsUtil:
    value: int

    @classmethod
    def bind(cls, value: int):
        cls.value = value

    @classmethod
    def get(cls, url: str, **kwargs) -> requests.Response:
        try:
            print(cls.value)
            return requests.get(url, kwargs)
        except requests.exceptions.RequestException as e:
            raise InternalException()

    @classmethod
    def json(cls, response: requests.Response) -> dict:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise InternalException()


class RequestsTest(TestCase):

    @patch("requests.get", side_effect=requests.exceptions.ConnectionError())
    def test_get(self, get_mock: MagicMock):
        with self.assertRaises(InternalException):
            RequestsUtil.bind(10)
            print(RequestsUtil.get(
                "https://www.naver.com"
            ))
