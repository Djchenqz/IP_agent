# -*- coding:utf-8 -*-
import requests
import time
from lxml import etree
# 引入UserAgent库随机生成请求头
from fake_useragent import UserAgent
import random
"""
1.爬取前三页的所有ip
2.验证所有ip是否有效
3.存储有效的ip
"""
def crawl(url):
	headers = {
		"User-Agent": UserAgent().random
	}
	try:
		response = requests.get(url=url, headers=headers)
		time.sleep(random.random())
		return response.text
	except Exception as e:
		print(e)

def parse(response, ips):
	try:
		htmlData = etree.HTML(response)
		# 提取所有的tr
		trTags = htmlData.xpath("//table[@id='ip_list']//tr")[1:]
		for eachItem in trTags:
			host = eachItem.xpath("./td[2]/text()")[0]
			port = eachItem.xpath("./td[3]/text()")[0]
			ip = host + ":" + port
			ips.append(ip)
	except Exception as e:
		print(e)

def varify(varifyUrl, ips):
	# 创建列表存放有效的ip
	usefulIp = []
	for ip in ips:
		print("正在验证ip: ", ip)
		try:
			# 设置代理访问http://www.baidu.com/验证ip的有效性
			res = requests.get(url=varifyUrl, proxies={"http": ip}, timeout=2)
			print(res.status_code)
			if res.status_code == requests.codes.ok:
				print("%s验证ok，可以正常使用。" % ip)
				usefulIp.append(ip)
		except:
			continue
	print("所有ip都已验证完毕，可使用ip有 %s 个，已存入列表。" % len(usefulIp))

def main():
	# 创建空列表存放爬取的ip
	ips =[]
	baseUrl = "https://www.xicidaili.com/nn/{}"
	varifyUrl = "http://www.baidu.com/"
	# 只爬取前三页数据
	for page in range(1, 4):
		url = baseUrl.format(page)
		response = crawl(url)
		parse(response, ips)
	varify(varifyUrl, ips)	

if __name__ == '__main__':
	main()