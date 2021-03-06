#coding:utf_8

from bs4 import BeautifulSoup
from urllib.parse import urljoin #python3
import requests
import csv
import time
import random

#上海租房信息地址，价格区间1000-3000，数据源58房源
url = "http://sh.58.com/pinpaigongyu/pn/{page}/?minprice=1000_3000"

#以完成的页面序号，初始为0
page = 0

#打开rent.csv文件
csv_file = open("rent.csv", "w", -1, "UTF-8")

#创建writer对象，指定文件与分隔符
csv_writer = csv.writer(csv_file, delimiter=',')

while True:
	page += 1
	print("fetch: ", url.format(page=page))
	response = requests.get(url.format(page=page))	#抓取目标页面
	#创建一个BeautifulSoup对象
	html = BeautifulSoup(response.text, "html.parser")	#(response.text)获取正文页面
	#获取class=list的元素下所有li元素
	house_list = html.select(".list > li")

	#循环在读不到新的房源时结束
	if not house_list:
		break;

	for house in house_list:
		#得到标签包裹者的文本
		house_title = house.select("h2")[0].string
		house_url = "http://bj.58.com/%s"%(house.select("a")[0]["href"])	#(house.select("a")[0]["href"]) 得到标签内属性的值
		house_info_list = house_title.split()

		#如果第二列是公寓名则取第一列作为地址
		if "公寓" in house_info_list[1] or "青年社区" in house_info_list[1]:
			house_location = house_info_list[0].split("】")[1]
		else:
			house_location = house_info_list[1]

		house_money = house.select(".money")[0].select("b")[0].string.encode("utf8")
		#写一行数据
		csv_writer.writerow([house_title, house_location, house_money, house_url])

	key = random.randint(2, 4)
	if page%key == 0:
		time.sleep(key)

#关闭文件
csv_file.close()
