# -*- coding:utf-8 -*-
from . import api
from ..utils import *
from flask import request
import re
import json
import requests
import threadpool


@api.route('/ping')
def ping():
    target = str(request.args.get('target', ''))
    ping = Ping(target)
    ping.th()
    arr = list(set(ping.arr))
    print(arr)
    return success(arr)



class Ping(object):
    def __init__(self, target):
        self.target = target
        self.arr = []
    
    def get_ip(self, node):
        header = {
            "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        data = "node={}&host={}".format(node, self.target)
        res = requests.post("https://www.wepcc.com/check-ping.html", headers=header, data=data, timeout=60)
        tmp = json.loads(res.text)
        if tmp['msg'] == 'ok':
            self.arr.append(tmp['data']['Ip'] + "  " + tmp['data']['ipAddress'])
        else:
            self.arr = ['1.无效的域名','2.站点可能已关闭']
    
    def th(self):
        header = {
            "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }
        data = "host={}&node=1,2,3,4,5,6".format(self.target)
        res = requests.post("https://www.wepcc.com", headers=header, data=data, timeout=60)
        tmp = re.findall('data-id="(.*?)"',res.text)
        pool = threadpool.ThreadPool(len(tmp)) 
        req = threadpool.makeRequests(self.get_ip, tmp)  
        for r in req:
            pool.putRequest(r)
        pool.wait()