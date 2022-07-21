import requests
from checklib import *

PORT = 1338

class CheckMachine:
    @property
    def url(self):
        return f'http://{self.c.host}:{self.port}'

    def __init__(self, checker: BaseChecker):
        self.c = checker
        self.port = PORT

    def put_flag(self, session: requests.Session, flag_value: str):
        url = f'{self.url}/put_flag'

        response = session.post(url, json={
            "flag": flag_value,
        })

        data = self.c.get_json(response, "Invalid response on put_flag")
        self.c.assert_eq(type(data), dict, "Invalid response on put_flag")
        self.c.assert_in("ok", data, "Invalid response on put_flag")
        self.c.assert_eq(data["ok"], True, "Can't put flag")

    def get_flag(self, session: requests.Session, status: Status) -> str:
        url = f'{self.url}/get_flag'

        response = session.post(url)

        data = self.c.get_json(response, "Invalid response on get_flag", status)
        self.c.assert_eq(type(data), dict, "Invalid response on get_flag", status)
        self.c.assert_in("ok", data, "Invalid response on get_flag", status)
        self.c.assert_in("flag", data, "Invalid response on get_flag", status)
        self.c.assert_eq(type(data["flag"]), str, "Invalid response on get_flag", status)
        self.c.assert_eq(data["ok"], True, "Can't get flag", status)

        return data["flag"]
