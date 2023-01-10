# -*- coding: utf-8 -*-
# @Author: Tuomas Aaltonen <ttumeh>
# @Date: 08.01.2023
#!/usr/bin/ python3
import requests
import json


def veikkaus_login (username, password, headers):
    """Sisäänkirjautuminen Veikkauksen tilille palauttaa sessio-objektin"""
    s = requests.Session()
    login_req = {"type":"STANDARD_LOGIN","login":username,"password":password}
    r = s.post("https://www.veikkaus.fi/api/bff/v1/sessions", data=json.dumps(login_req), headers=headers)
    if r.status_code == 200:
        return s
    else:
        raise Exception("Authentication failed", r.status_code)