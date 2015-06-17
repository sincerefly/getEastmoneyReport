#!/bin/env python
#encoding:utf-8
from selenium import webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import re
import json
import base64
import urllib2
import requests
import chardet
#print chardet.detect('我是中文')

# -----------------------------------------------------------------
# This tools can get info from 'http://data.eastmoney.com/report'
# -----------------------------------------------------------------

# Static variable
MAX_NUMBER = 157
startTime = int(time.time())

client = MongoClient('localhost', 27017)
db = client.guping

# re. used by webdriver
pattern = re.compile(r'<tbody>([\s\S]+)</tbody>')

# Loop for get page list
print "-"*6 + ' start ' + '-'*6
for page in range(92, MAX_NUMBER + 1):

    # The Page list URL
    params = 'tp=1&cg=0&dt=2&page=' + str(page)
    base64encode = base64.b64encode(params)

    URL = 'http://data.eastmoney.com/report/#' + base64encode
    print URL

    driver = webdriver.PhantomJS("./phantomjs")
    driver.set_window_size(1366, 768) # optional
    driver.get(URL)

    bodyStr= driver.find_element_by_tag_name("body").get_attribute("innerHTML")

    driver.quit() # Every time you need to quit the driver 

    # match the useful data
    match = pattern.search(bodyStr)

    if match:
        string = match.group(1)
    else:
        print 'Error: ' + str(page) + '/' + str(MAX_NUMBER) + 'No data'

    # insert into mongodb per page 
    l = []
    count = 0
		
    for row in BeautifulSoup(string)("tr"):

        count = count + 1
        # ------ Get the detail page to get the author ------
        lasturl = row("td")[5]("a")[0]["href"]
        detail_url = 'http://data.eastmoney.com' + lasturl
        #detail_url = 'http://data.eastmoney.com/report/20150615/APPGN1vwyH6mASearchReport.html'
        print '\t -> ' + str(count) + '. '+ lasturl

#       detail_page = urllib2.urlopen(detail_url)
        try:
            detail_page = requests.get(detail_url).text
            soup = BeautifulSoup(detail_page, from_encoding='gb2312')
        except:
            print '\t -> ' + str(count) + '. '+ 'The Urllib3 err, Try ...'
            time.sleep(3)
            detail_page = requests.get(detail_url).text
            soup = BeautifulSoup(detail_page, from_encoding='gb2312')

        try:
            author2 = soup.find_all('div', class_='report-infos')[0]("span")[3].text
        except IndexError:
            print '\t -> ' + str(count) + '. '+ 'The IndexError, Try ...'
            time.sleep(3)
            soup = BeautifulSoup(detail_page, from_encoding='gb2312')
            author2 = soup.find_all('div', class_='report-infos')[0]("span")[3].text
   
        author2_list = author2.split(',')
#       print map(lambda x: type(x), author2_list)
        author2_utf8 = map(lambda x: x.encode('utf-8', 'replace'), author2_list)

        # ---------------------------------------------------

        data = {
            "date": row("td")[1]("span")[0]["title"].encode('utf-8'),
            "code": row("td")[2].text.encode('utf-8'),
            "name": row("td")[3].text.encode('utf-8'),
            "title": row("td")[5].text.encode('utf-8'),
            "suggest": row("td")[6].text.encode('utf-8'),
            "change": row("td")[7].text.encode('utf-8'),
            "author": row("td")[8].text.encode('utf-8'),
            "author2": author2_utf8,
            "a1": row("td")[9].text.encode('utf-8'),
            "a2": row("td")[10].text.encode('utf-8'),
            "b1": row("td")[11].text.encode('utf-8'),
            "b2": row("td")[12].text.encode('utf-8'),
        }
        l.append(data)

    db.dfcf_up2.insert(l)
    useSeconds = str(int(time.time()) - startTime)
    print 'Success: ' + str(page) + '/' + str(MAX_NUMBER) + '\t' + base64encode +  '\tTotalUseTime: ' + useSeconds + 's'

print "-"*6 + ' end ' + '-'*6

























