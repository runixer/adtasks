#!/usr/bin/env python3

import sys
import requests

ip = sys.argv[1]

url = f"http://{ip}:1337/get_flag"

r = requests.post(url)

print(r.json()["flag"], flush=True)
