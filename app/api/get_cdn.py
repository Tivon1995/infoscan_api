from . import api
from ..utils import *
from flask import request
import json
import re
import requests
requests.packages.urllib3.disable_warnings()


@api.route('/get_cdn')
def get_cdn():
    target = str(request.args.get('target', ''))
    # print(target)
    getcdn = Getcdn(target)
    getcdn.search()
    return success(getcdn.arr)



class Getcdn(object):
    def __init__(self, target):
        self.target = target
        self.token = []
        self.arr = []
        self.search()

    def search(self):
        self.token = self.GetcdnToken()
        self.GetCdnName(self.token, self.target)


    def GetcdnToken(self):
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'Sec-Fetch-Site': 'none',
              'Sec-Fetch-Mode': 'navigate',
              'Sec-Fetch-User': '?1',
              'Sec-Fetch-Dest': 'document',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Cookie': '__cfduid=d4faa9dd5daf90b9b78aad4d612671cc81617262245;',
              'Host': 'www.cdnplanet.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
              }
        resp = requests.get("https://www.cdnplanet.com/tools/cdnfinder/", verify=False, headers=header, timeout = 15).text
        pattern = re.compile(r'_cdnpToken = "(.*?)"')
        result1 = pattern.findall(resp)
        return result1


    def GetCdnName(self, recvToken,url):
        print(recvToken)
        token = recvToken[0]
        proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
        header = {
              'Accept': 'application/json',
              'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
              'Authorization': token,
              'sec-ch-ua-mobile': '?0',
              'Origin': 'https://www.cdnplanet.com',
              'Sec-Fetch-Site': 'same-site',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Dest': 'empty',
              'Referer': 'https://www.cdnplanet.com/tools/cdnfinder/',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Content-Type': 'application/json',
              'Host': 'api.cdnplanet.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
              }

        data = '{"query":"%s"}'%(url) 
        dataResult = requests.post("https://api.cdnplanet.com/tools/cdnfinder?lookup=website", headers=header,data=data,verify=False, timeout = 15)
        data2 = json.loads(dataResult.text)
        Projectid = data2['id']
        header = {
              'Host': 'api.cdnplanet.com',
              'Connection': 'close',
              'Pragma': 'no-cache',
              'Cache-Control': 'no-cache',
              'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
              'Accept': 'application/json',
              'sec-ch-ua-mobile': '?0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
              'Content-Type': 'application/json',
              'Origin': 'https://www.cdnplanet.com',
              'Sec-Fetch-Site': 'same-site',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Dest': 'empty',
              'Referer': 'https://www.cdnplanet.com/tools/cdnfinder/',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              }
        while True:
            resp1 = requests.get("https://api.cdnplanet.com/tools/results?source=website&service=cdnfinder&id="+str(Projectid),verify=False,headers=header)
            data3 = json.loads(resp1.text)
            if 'results' in data3:
                for i in range(0,len(data3['results'])):
                    ccc = (data3['results'][i]['hostname']+ "," +data3['results'][i]['cdn'])
                    # print ccc
                    self.arr.append(str(ccc))
                break
        self.arr = list(set(self.arr))
