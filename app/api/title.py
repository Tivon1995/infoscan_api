# -*- coding:utf-8 -*-
from . import api
from ..utils import *
from flask import request
import requests
import re
import chardet


@api.route('/title')
def title():
    target = str(request.args.get('target', ''))
    title = Title(target)
    flag = title.get_title()
    return success(flag)


class Title(object):
    def __init__(self, target):
        self.target = target


    def get_title(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }
        res = 0
        try:
            res = requests.get(self.target, headers=headers,timeout=15, verify=False)
        except:
            res = requests.get(self.target, headers=headers,timeout=15, verify=False)
        finally:
            if res:
                if res.status_code == 200:
                    char = chardet.detect(res.content).get('encoding')
                    if char == 'GB2312':
                        char = 'GBK'
                    flag = re.findall('<title>(.*?)</title>', res.content.decode(char))[0]
                    # print(flag)
                    if flag:
                        return flag
                    else:
                        return "未知标题,网页可能重定向到其他网页或域名不可访问"
                else:
                    return "未知标题,网页可能重定向到其他网页或域名不可访问"
            else:
                return "未知标题,网页可能重定向到其他网页或域名不可访问"

