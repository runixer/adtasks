#!/usr/bin/env python3

import sys
import requests

from checklib import *
from task1_lib import *


class Checker(BaseChecker):
    vulns: int = 1
    timeout: int = 5
    uses_attack_data: bool = True

    def __init__(self, *args, **kwargs):
        super(Checker, self).__init__(*args, **kwargs)
        self.mch = CheckMachine(self)

    def action(self, action, *args, **kwargs):
        try:
            super(Checker, self).action(action, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self.cquit(Status.DOWN, 'Connection error', 'Got requests connection error')

    def check(self):
        session = get_initialized_session()
        flag_value = rnd_string(20)
        self.mch.put_flag(session, flag_value)
        value = self.mch.get_flag(session, flag_value, Status.MUMBLE)
        self.assert_eq(value, flag_value, "Note value is invalid")
        self.cquit(Status.OK)

    def put(self, flag_id: str, flag: str, vuln: str):
        session = get_initialized_session()
        self.mch.put_note(session, flag)
        self.cquit(Status.OK)

    def get(self, flag_id: str, flag: str, vuln: str):
        s = get_initialized_session()
        value = self.mch.get_flag(s, flag, Status.CORRUPT)

        self.assert_eq(value, flag, "Note value is invalid", Status.CORRUPT)

        self.cquit(Status.OK)


if __name__ == '__main__':
    c = Checker(sys.argv[2])

    try:
        c.action(sys.argv[1], *sys.argv[3:])
    except c.get_check_finished_exception():
        cquit(Status(c.status), c.public, c.private)
