# coding=utf-8
'''
全端口扫描
'''
import sys
import socket
import requests
import dns.resolver
import threadpool
from time import time
from . import api
from app.utils import *
from flask import  request

@api.route('/all_portscan')
def all_portscan():
    target = str(request.args.get('target', ''))
    if target.startswith('http://') or target.startswith('https://'):
        domain = target.split('/')[2]
    else:
        domain = target.split('/')[0]
    portscan = Scanner(domain)               
    portscan.check_target()
    arr = list(set(portscan.arr))
    arr.sort()
    return success(arr)

class Scanner(object):
    	# def __init__(self, target, start, end):
	def __init__(self, target):
		self.target = target
		self.result = []
		self.arr = []


	def check_cdn(self):
		#目标域名cdn检测
		myResolver = dns.resolver.Resolver()
		myResolver.lifetime = myResolver.timeout = 5.0
		dnsserver = [['114.114.114.114'],['8.8.8.8'],['223.6.6.6']]
		try:
			for i in dnsserver:
				myResolver.nameservers = i
				record = myResolver.query(self.target)
				self.result.append(record[0].address)
			# print(self.result)
		except Exception as e:
			pass
		finally:
			return True if len(set(list(self.result))) > 1 else False

	def scan_port(self, port):
		#端口扫描
		try:
			socket.setdefaulttimeout(0.5)
			s = socket.socket()
			s.connect((self.result[1], port))
			self.arr.append(port)
		except Exception as e:
			pass
		finally:
			s.close()



	def _start(self, arr, thnum):
		try:
			#线程数
			pool = threadpool.ThreadPool(thnum)
			req = threadpool.makeRequests(self.scan_port, arr)
			for r in req:
    				pool.putRequest(r)
			pool.wait()
			# get传递超时时间，用于捕捉ctrl+c
		except Exception as e:
			print(e)
		except KeyboardInterrupt:
			print('[-] 用户终止扫描...')
			sys.exit(1)

	def check_target(self):
		#判断目标是域名还是还是ip地址
		flag = self.target.split('.')[-1]
		faqp = [21,22,23,25,53,69,80,83,81-89,110,135,139,143,443,445,465,993,995,1080,1158,1433,1521,1863,2100,3128,3306,3389,7001,8080,8888,9080,9090,888,9999,6666,4444,5555,7777,2222,3333] + list(range(8080, 8101))
		try:
			#ip地址
			if int(flag) >= 0:
				self._start(faqp, 20)
				self._start(range(1,1001), 100)
				if len(self.arr) > 100:
					self.arr = ["端口开放异常,可能存在防火墙！"]
				else:
					self._start(range(1002,10001), 200)
					self._start(range(10002,65536), 500)
					# self._start(range(20002,65536), 2000)
		except:
			#域名地址
			if not self.check_cdn():
				self._start(faqp, 20)
				self._start(range(1,1001), 100)
				if len(self.arr) > 100:
					self.arr = ["端口开放异常,可能存在防火墙！"]
				else:
					self._start(range(1002,10001), 200)
					self._start(range(10002,65536), 500)
					# self._start(range(20002,65536), 2000)
			else:
				self.arr.append("存在CDN,无法探测！")
				print('[-] 目标使用了CDN技术,停止扫描')
