#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests

from Cheese.cheese import CheeseBurger
from Cheese.appSettings import Settings

"""
File generated by Cheese Framework

main file of Cheese Application
"""

if __name__ == "__main__":
    CheeseBurger.init()

    i = 0
    while i < 1:
        try:
            req = {
                "name": Settings.name,
                "port": Settings.port,
                "icon": "/favicon.png",
                "color": "FF0000"
            }
            requests.post(f"http://localhost/services/doYouKnowMe", json=req)
            break
        except:
            i += 1
            time.sleep(1)

    CheeseBurger.serveForever()