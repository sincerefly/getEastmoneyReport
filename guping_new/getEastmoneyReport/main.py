#!/bin/env python
#encoding:utf-8
import re
import time
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
from multiprocessing import Pool

# Settings
PAGE_NUMBER = 283
BASE_URL = "http://data.eastmoney.com/report/#"
ALL_PARAMS = 'tp=1&cg=0&dt=2&page='
# Set Single Process(0) or Multi Process(1)
multi = 1

# Re
pattern = re.compile(r'<tbody>([\s\S]+)</tbody>')

# Connect Mongo 
client = MongoClient('localhost', 27017)
db = client.guping

if db:
   print "Connect MongoDB Sucess"

# Functions
def getUrlList():
    l = []
    for i in range(1, PAGE_NUMBER + 1):
        url = BASE_URL + base64.b64encode(ALL_PARAMS + str(i))
        l.append(url)
    return l

def insertMongo(data):
    result = db.dfcf_index_all.insert(data)
    return 0

def save2file(string, index):

    filepath = 'url/page_%s.txt' % index

    f = open(filepath, 'w+')
    f.write(string)
    f.close()
    
def soupData(string, index):
    l = []
    s = ''
    for row in BeautifulSoup(string, "html.parser")("tr"):
        data = {
            "date": row("td")[1]("span")[0]["title"].encode("utf-8"),
            "code": row("td")[2].text.encode("utf-8"),
            "name": row("td")[3].text.encode("utf-8"),
            "title": row("td")[5].text.encode("utf-8"),
            "article_url": row("td")[5]("a")[0]["href"].encode("utf-8"),
            "suggest": row("td")[6].text.encode("utf-8"),
            "change": row("td")[7].text.encode("utf-8"),
            "company": row("td")[8].text.encode("utf-8"),
            "a1": row("td")[9].text.encode("utf-8"),
            "a2": row("td")[10].text.encode("utf-8"),
            "b1": row("td")[11].text.encode("utf-8"),
            "b2": row("td")[12].text.encode("utf-8"),
        }
        l.append(data)

        article_url = row("td")[5]("a")[0]["href"]
        #detail_url = 'http://data.eastmoney.com' + lasturl
        s = s +  article_url + '\n'

    save2file(s, index)   
    insertMongo(l)
    return 0

def phantomGet(url, index):

    t1 = time.time()

    try:
        driver = webdriver.PhantomJS("./phantomjs")
        driver.set_window_size(1366, 768) # optional
        driver.get(url)

        bodyStr= driver.find_element_by_tag_name("body").get_attribute("innerHTML")

        driver.quit() # Every time you need to quit the driver 
    except:
        print "    |-Some Error -->%s" % url
        pass

    # match the useful data
    try:
        match = pattern.search(bodyStr)
    except:
        print "    |-Some Error -->%s" % url
        print "    |-UnboundLocalError: local variable 'bodyStr' referenced before assignment"
        match = 0
        pass

    if match:
        string = match.group(1)
        soupData(string, index)
    else:
        print "no data"

    t2 = time.time()
    print '(' + str(index+1) + '/' + str(PAGE_NUMBER) + ') ' + url + '\t' + str(t2 - t1)
    return 0


if __name__ == '__main__':

    startTime = int(time.time())
     
    # Get all page(one page have 50 count article)
    urlList = getUrlList()   

    if multi:
        print "Multi Processing..."
        p = Pool()
        for url in urlList:
            index = urlList.index(url)
            p.apply_async(phantomGet, args=(url,index))
        p.close()
        p.join()
    else:
        print "Single Processing..."
        for url in urlList:
            index = urlList.index(url)
            phantomGet(url, index)

    closeTime = time.time()

    print 'All subprocesses done. use %0.2f seconds' % (closeTime - startTime)
    
