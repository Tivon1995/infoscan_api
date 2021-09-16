# -*- coding:utf-8 -*-
import requests
import base64
import random
import string
import os

from . import api
from ..utils import *
from flask import request


@api.route('/img')
def get_img():
    target = str(request.args.get('target', ''))
    img = Img("https://www.baidu.com")
    img_data = img.get_img()
    return success(img_data)



class Img(object):
    def __init__(self, target):
        self.img_bs64 = "http://pic.soutu123.cn/element_origin_min_pic/16/12/20/b956c5dbba7221df44f281882d5ac80b.jpg"
        self.target = target
        self.headers = {
            "POST":"/tools/api/webjietu.html HTTP/1.1",
            "Host":"api.toolnb.com",
            "Connection":"keep-alive",
            "Content-Length":"69",
            "Pragma":"no-cache",
            "sec-ch-ua":'"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "sec-ch-ua-mobile":"?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Origin":"https://www.toolnb.com",
            "Sec-Fetch-Site":"same-site",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Dest":"empty",
            "Referer":"https://www.toolnb.com",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9"
        }


    def get_img(self):
        try:
            data = {
                "url":self.target,
                "w":"1280",
                "type":"base64",
                "h":"720",
                "useragent":"pc"
            }
            res = requests.post('https://api.toolnb.com/tools/api/webjietu.html', data=data, headers=self.headers, timeout=60).json()
            if  res['msg'] == 'ok':
                if 'jpg' in res['data']:
                    tmp = ''.join(random.sample(string.digits, 8))
                    # tmp_bs4 = base64.decode(res['data'])
                    f = open(tmp + '.jpg', 'wb')
                    f.write(base64.b64decode(res['data'].split(',')[1]))
                    f.close()
                    if os.path.getsize(tmp + '.jpg') > 51200:
                        self.img_bs64 = res['data']
                        # return res['data']
                    else:
                        self.get_img2()
                    os.remove(tmp + '.jpg')
                elif 'png' in res['data']:
                    tmp = ''.join(random.sample(string.digits, 8))
                    f = open(tmp + '.png', 'wb')
                    f.write(base64.b64decode(res['data'].split(',')[1]))
                    f.close()
                    if os.path.getsize(tmp + '.png') > 51200:
                        self.img_bs64 = res['data']
                    else:
                        self.get_img2()
                    os.remove(tmp + '.png')
            else:
                data = {"url":self.target,"w":"1280","type":"file","h":"720","useragent":"pc"}
                res0 = requests.post('https://api.toolnb.com/tools/api/webjietu.html', data=data, headers=self.headers, timeout=60)
                res = res0.json()
                if res['msg'] == 'ok':
                    # print(res['data'])
                    link = res['data']
                    res = requests.get(url=link, timeout=30)
                    if '.png' in link:
                        tmp = ''.join(random.sample(string.digits, 8))
                        f = open(tmp+'.png', 'wb')
                        f.write(res.content)
                        f.close
                        if os.path.getsize(tmp+'.png') < 51200:
                            self.get_img2()
                        else:
                            self.img_bs64 = "data:image/png;base64," + base64.b64encode(res.content).decode('utf-8')
                        os.remove(tmp + 'png')
                    elif '.jpg' in link:
                        tmp = ''.join(random.sample(string.digits, 8))
                        f = open(tmp+'.jpg', 'wb')
                        f.write(res.content)
                        f.close
                        if os.path.getsize(tmp+'.jpg') < 51200:
                            self.get_img2()
                        else:
                            self.img_bs64 = "data:image/jpg;base64," + base64.b64encode(res.content).decode('utf-8')
                        os.remove(tmp + 'jpg')
        except Exception as e:
            self.get_img2()
        finally:
            pass

    def get_img2(self):
        data = {"url": self.target,"emulator":"PC"}
        res = requests.post("https://api.tool.dute.me/tool/webpageScreenshot", data=data, timeout=60).json()
        if res['code'] == 200:
            link = res['data']['thumbnail']
            res = requests.get(url=link, timeout=30)
            if '.jpg' in link:
                img_bs64 = "data:image/png;base64," + base64.b64encode(res.content).decode('utf-8')
            elif '.png' in link:
                img_bs64 = "data:image/jpg;base64," + base64.b64encode(res.content).decode('utf-8')
            # print(img_bs64)
            self.img_bs64 = img_bs64
            return

