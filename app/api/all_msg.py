# -*- coding:utf-8 -*-
# 1.whois  2.portscan  3.cdn 4.subdomain 5.ping 6.dirsearch
import whois
import time
import requests
import re

from . import api
from ..utils import *
from flask import request
from app.api.portscan import Scanner
from app.api.subdomain import Subdomain
from app.api.get_cdn import Getcdn
from app.api.ping import Ping
from app.api.dirsearch.dirsearch import Program
from app.api.title import Title
from app.api.img import Img

import pymysql



@api.route('/all_msg')
def all_msg():
    t1 = time.time()
    # conn = pymysql.connect(host="127.0.0.1", port=3306, user="precheck", password="JTZ6pzNpHzis6nRL", database="precheck", charset="utf8")
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="mysql", database="precheck", charset="utf8")
    cursor = conn.cursor()
    target = str(request.args.get('target', ''))
    workId = str(request.args.get('workId', ''))
    # print "-------------------------------------", target, workId, "---------------------------------"
    # return success("123")
    if target.startswith('http://') or target.startswith('https://'):
        domain = target.split('/')[2]
    else:
        domain = target.split('/')[0]

    # 0.title
    print("title --->",target)
    try:
        title = Title(target)
        title_data = title.get_title()
        sql = "update sense set title='{}' where id={}".format(title_data, workId)
        cursor.execute(sql)
        conn.commit()
        del title,title_data,sql
    except Exception as e:
        conn.rollback()
        print("title module error xxx")
    finally:
        pass
        #print("title-------------------")

    # 0.1 title
    print("img --->",target)
    try:
        img = Img(target)
        img.get_img()
        img_data = img.img_bs64
        img_tmp = []
        img_tmp.append(img_data)
        sql = "update sense set capture='{}' where id={}".format(listToJson(img_tmp), workId)
        cursor.execute(sql)
        conn.commit()
        del img,img_tmp,img_data,sql
    except Exception as e:
        conn.rollback()
        print("img module error xxx")
    finally:
        pass
        #print("img-------------------")

    try:
        print("whois --->",target)
        # 1.whois
        whois_data = whois.whois(domain)
        sql = "update sense set whois='{}' where id={}".format(str(whois_data), workId)
        cursor.execute(sql)
        conn.commit()
        del whois_data,sql
    except Exception as e:
        whois_data = "error"
        print("whois moduel error XXX")
        conn.rollback()
    finally:
        pass

    try:
        print("ping --->",target)
        # 5.ping
        ping = Ping(target)
        ping.th()
        ping_data = list(set(ping.arr))
        sql = "update sense set ping='{}' where id={}".format(listToJson(ping_data), workId)
        cursor.execute(sql)
        conn.commit()
        del ping,sql
    except Exception as e:
        ping_data = ["error",""]
        print("ping moduel error XXX",e)
        conn.rollback()
    finally:
        pass
    
    try:
        if len(ping_data) > 1:
            port_data = ["cdn"]
            sql = "update sense set port='{}' where id={}".format(listToJson(port_data), workId)
            cursor.execute(sql)
            conn.commit()
        else:
            print("portscan --->",target)
            # 2.portscan
            portscan = Scanner(domain)
            portscan.check_target()
            # if len(portscan.arr) > 100:
            #     portscan.arr = ["端口开放异常,可能存在防火墙！"]
            # else:
	        #     portscan.arr.sort()
            port_data = list(set(portscan.arr))
            port_data.sort()
            sql = "update sense set port='{}' where id={}".format(listToJson(port_data), workId)
            cursor.execute(sql)
            conn.commit()
            del portscan,port_data,sql,ping_data
    except Exception as e:
        conn.rollback()
        print("port module error xxx",e)
    finally:
        pass
        #print("portscan-------------------")
    # 云函数修改前
    # try:
    #     # 3.cdn
    #     getcdn = Getcdn(target)
    #     getcdn.search()
    #     if len(getcdn.arr)>0:
    #         cdn_data = getcdn.arr
    #     else:
    #         cdn_data = ["该网站可能无CDN或未能识别出CDN，需要人工判断"]
    #     sql = "update sense set cdn='{}' where id={}".format(listToJson(cdn_data), workId)
    #     cursor.execute(sql)
    #     conn.commit()
    #     del getcdn,cdn_data,sql
    # except Exception as e:
    #     conn.rollback()
    #     print("cdn module error xxx",e)
    # finally:
    #     pass
        print("cdn --->",target)
    try:
        # 3.cdn
        res = requests.get(url="https://debfcfe205b94108bacf00b08f82ac60.apig.ap-southeast-1.huaweicloudapis.com/get_get?target={}".format(target), timeout=60)
        if res.status_code == 200:
            cdn_data = re.findall("'(.*?)'",res.text)
        else:
            res = requests.get(url="https://debfcfe205b94108bacf00b08f82ac60.apig.ap-southeast-1.huaweicloudapis.com/get_get?target={}".format(target), timeout=60)
            if res.status_code == 200:
                cdn_data = re.findall("'(.*?)'",res.text)

        if len(cdn_data) < 1:
            cdn_data = ["该网站可能无CDN或未能识别出CDN，需要人工判断"]

        sql = "update sense set cdn='{}' where id={}".format(listToJson(cdn_data), workId)
        cursor.execute(sql)
        conn.commit()
        del res,cdn_data,sql
    except Exception as e:
        conn.rollback()
        print("cdn module error xxx",e)
    finally:
        pass
        # print("cdn-------------------")

    try:
        print("subdomain --->",target)
        # 4.subdomain
        domain_data = []
        main_domain=get_maindomain(target)
        subdomain = Subdomain(main_domain)
        if len(subdomain.search())>0:
            domain_data=subdomain.search()
        else:
            domain_data=["该站点无子域名或没有扫描到子域名"]
        # print(domain_data)
        sql = "update sense set subdomain='{}' where id={}".format(listToJson(domain_data), workId)
        cursor.execute(sql)
        conn.commit()
        del main_domain,domain_data,subdomain,sql
    except Exception as e:
        conn.rollback()
        print("subdomain module error xxx")
    finally:
        pass
        # print("subdomain-------------------")


    try:
        # res = requests.get(url = target, timeout = 15, verify=False, headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36"})
        # if True:
        # 6.dirsacan   注释掉了输出 Last request  Starting:
        print("dirsacan --->",target)
        dirscan =Program(target)
        dirscan.output.arr.sort()
        dir_data = []
        for i in dirscan.output.arr:
            if not ('50' in i):
                if len(dir_data) < 200:
                    if (domain in i) == False:
                        i = i + "  ->  " + (target + i[i.index("/"):])
                        dir_data.append(i)
                    else:
                        dir_data.append(i)
        
        sql = "update sense set dir='{}' where id={}".format(listToJson(dir_data), workId)
        # print(sql)
        cursor.execute(sql)
        conn.commit()        
        del dirscan,dir_data,sql
    except Exception as e:
        conn.rollback()
        print("dirsacan module error xxx",e)
    finally:
        #print("dirsacan-------------------")
        pass
    #7.update status
    sql = "update sense set status=1 where id={}".format(workId)
    cursor.execute(sql)
    conn.commit()
    del sql
    print("update status done")

    # msg = {
    #     "title": title_data,
    #     "whois": whois_data,
    #     "port": port_data,
    #     "cdn": cdn_data,
    #     "subdomain": domain_data,
    #     "ping": ping_data,
    #     "dir": dir_data,
    #     "img": img_data,
    # }
    cursor.close()
    conn.close()
    print(target," Running time --> ",round(time.time() - t1, 2))
    return success("msg")