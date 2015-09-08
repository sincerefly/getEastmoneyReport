#!/usr/bin/python
#encoding:utf-8
from multiprocessing import Pool
from bs4 import BeautifulSoup
import shutil
import os, time
import requests
import re
import sys
from pymongo import MongoClient
import chardet
import urllib

# Setting
multi = 0
StartPage = 0
EndPage = 3671

# Connect Mongo
client = MongoClient('localhost', 27017)
db = client.guping

# 测试编码
rawdata = urllib.urlopen('http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/lastest/index.phtml?p=1').read()
print '原始网页的编码为' + str(chardet.detect(rawdata)["encoding"]) + '的可能性为' + str(chardet.detect(rawdata)["confidence"])


if db:
   print "Connect MongoDB Sucess"

def getTheArticleList(pageid, page_url):

    global EndPage

    try:
        page = requests.get(page_url, timeout=10).content
    except:
        page = 0

    if page == 0:
        return art_list


    #soup = BeautifulSoup(page.decode('gb2312', 'ignore'), from_encoding="GB2312")
    soup = BeautifulSoup(page.decode('gb2312', 'ignore'), "html.parser")
    try:
        content = soup.find_all('div', class_='main')[0]('table')[0]('tr')
    except:
        content = []
        print "some error..."

    order = 0
    count = 0
    for one in content:

        # 因为原始网页非语义化，此处判断用于过滤掉前面两个无用td标签
        if order in [0,1]:
            order = order + 1
            continue

        count = count + 1

        # 获取所有的
        try:
            tds = one.find_all('td')

            title = tds[1]('a')[0]['title']
            url = tds[1]('a')[0]['href']
            date = tds[3].text
            company = tds[4]('a')[0]('span')[0].text
            author = tds[5].text
        except:
            print "pass 0: get page error"
            continue

        # 使用url获取文章的详情, 获取股票code
        try:
            article = requests.get(url).content
        except:
            print "pass 1: get url error"
            continue

        # 解析文章链接
        article_soup = BeautifulSoup(article.decode('gb2312', 'ignore'), "html.parser")
        try:
            article_content = article_soup.find(id='stocks')
        except:
            print "pass 2: soup find error"
            continue

        try:
            code = article_content('tr')[1]('td')[0].text
        except:
            print "pass 3: no code"
            continue

        info = {
                "name": title,
                "code": code,
                "date": date,
                "company": company,
                "author": author,
                "url": url
        }
        db.sina_article_alls.update({'date': date, 'code': code, 'company': company}, {'$set': info}, upsert=True)
        print '(%s/%s)(%s/%s) %s %s %s %s %s' % (str(pageid), str(EndPage), str(count), '40', code, date, title, company, author)


if __name__=='__main__':

    t1 = time.time()

    for pageid in range(StartPage, EndPage+1):

        url = 'http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/lastest/index.phtml?p=' + str(pageid)
        getTheArticleList(pageid, url)


    sys.exit(0)
