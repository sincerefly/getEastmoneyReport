#!/bin/env python
#encoding:utf-8
from selenium import webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import re
import json
import base64

# -----------------------------------------------------------------
# 这个程序可以爬取http://data.eastmoney.com/report/ 网站的股评数据
# -----------------------------------------------------------------

# static
MAX_NUMBER = 156
startTime = int(time.time())

client = MongoClient('localhost', 27017)
db = client.guping

# 匹配网站的数据
pattern = re.compile(r'<tbody>([\s\S]+)</tbody>')

print "-"*6 + ' start ' + '-'*6
for page in range(1, MAX_NUMBER + 1):

    # 拼接网站的URL
    params = 'tp=1&cg=0&dt=2&page=' + str(page)
    base64encode = base64.b64encode(params)

    URL = 'http://data.eastmoney.com/report/#' + base64encode

    driver = webdriver.PhantomJS("./phantomjs")
    driver.set_window_size(1366, 768) # optional
    driver.get(URL)

    bodyStr= driver.find_element_by_tag_name("body").get_attribute("innerHTML")
    #print bodyStr

    driver.quit() # 每一次抓取URL都需要关闭driver，重新建立，否则无法循环使用

    match = pattern.search(bodyStr)

    if match:
        string = match.group(1)
    else:
        print 'Error: ' + str(page) + '/' + str(MAX_NUMBER) + 'No data'

    # 将数据每页数据拼接,保存到mongodb数据库中
    l = []
    for row in BeautifulSoup(string)("tr"):
        #print row("td")[1]("span")[0]["title"]
        #print '-'*6
        #for i in row("td"):
            #print i.text
            #print i

        data = {
            "date": row("td")[1]("span")[0]["title"],
            "code": row("td")[2].text,
            "name": row("td")[3].text,
            "title": row("td")[5].text,
            "suggest": row("td")[6].text,
            "change": row("td")[7].text,
            "author": row("td")[8].text,
            "a1": row("td")[9].text,
            "a2": row("td")[10].text,
            "b1": row("td")[11].text,
            "b2": row("td")[12].text,
        }
        #print data
        l.append(data)

    db.dfcf_up.insert(l)
    useSeconds = str(int(time.time()) - startTime)
    print 'Success: ' + str(page) + '/' + str(MAX_NUMBER) + '\t' + base64encode +  '\tTotalUseTime: ' + useSeconds + 's'

print "-"*6 + ' end ' + '-'*6

























