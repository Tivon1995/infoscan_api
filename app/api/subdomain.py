from . import api
from flask import request
import requests
from pyquery import PyQuery as pq
from app.utils import *


@api.route('/subdomain')
def get_subdomain():
    target = str(request.args.get('target', ''))
    main_domain=get_maindomain(target)
    # data=search(main_domain)
    subdomain = Subdomain(main_domain)
    data = subdomain.search()
    # print(data)
    return success(data)


class Subdomain(object):
    def __init__(self, target):
        self.target = target
        self.search()

    def search(self):
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Host": "www.virustotal.com",
            "Connection": "close",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "X-Tool": "vt-ui-main",
            "sec-ch-ua-mobile": "?0",
            "content-type": "application/json",
            "x-app-version": "v1x9x2",
            "accept": "application/json",
            "Accept-Ianguage": "en-US,en;q=0.9,es;q=0.8",
            "X-VT-Anti-Abuse-Header": "MTI3MjgwOTI3OTMtWkc5dWRDQmlaU0JsZG1scy0xNjE2NzUyMzQ2Ljk4Nw==",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.virustotal.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "_ga=GA1.2.408148319.1616745730; _gid=GA1.2.1068117866.-1616745730"
        }
        url = "https://www.virustotal.com/ui/domains/" + self.target + "/subdomains?relationships=resolutions&limit=40"
        res = requests.get(url, headers=header, timeout=30).json()
        arr = []
        for i in res["data"]:
            arr.append(i["id"])
        # print arr
        return arr



