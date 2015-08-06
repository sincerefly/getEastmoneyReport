#!/usr/bin/python
#encoding:utf-8
from multiprocessing import Pool
from bs4 import BeautifulSoup
import os, time
import requests
import re
from pymongo import MongoClient

# Setting
multi = 0

# Connect Mongo
client = MongoClient('localhost', 27017)
db = client.guping

if db:
   print "Connect MongoDB Sucess"

# Function
#def insert2mongo(data):
#    return 0

def get_Data(url,index, listlen):
    start = time.time()
    try:
        page = requests.get(url).text
    except requests.exceptions.MissingSchema:
        print "Ignore: requests.exceptions.MissingSchema"
        page = 0
        pass
    except UnboundLocalError:
        print "Ignore: UnboundLocalError"
        page = 0
        pass
    except:
        print "Ignore: some error"
        page = 0
        pass

    if page == 0:
        return 0

    #soup = BeautifulSoup(page, from_encoding='gb2312')
    soup = BeautifulSoup(page, "html.parser")
    try:
        title = soup.find_all('div', class_='report-title')[0]("h1")[0].text
        #print '(%s/%s)%s runs %0.2f seconds.' % (index+1, listlen, title, (end - start))

        name_code = soup.find_all('div', class_='tit')[0]("a")[0].text
        l = re.split('\(|\)', name_code)
        name = l[0]
        code = l[1]
        date = soup.find_all('div', class_='report-infos')[0]("span")[1].text
        date = date[0:4] + date[5:7] + date[8:10]
        company = soup.find_all('div', class_='report-infos')[0]("span")[2].text
        author = soup.find_all('div', class_='report-infos')[0]("span")[3].text
        author = author.split(',')
    except:
        print "some error..."
        return 0
    #print '    -> %s' % url
    #print '    -> %s' % name
    #print '    -> %s' % code
    #print '    -> %s' % date
    #print '    -> %s' % company
    #print '    -> %s' % author

    one = {
        "name": name,
        "code": code,
        "date": date,
        "company": company,
        "author": author,
        "url": url
    }

    result = db.dfcf_article_all.update({'date':date, 'code':code, 'company':company}, {'$set':one}, upsert = True)
    #insert2mongo(one)

    end = time.time()

    print '(%s/%s)%s runs %0.2f seconds.' % (index+1, listlen, title, (end - start))



if __name__=='__main__':

    t1 = time.time()
    print 'Parent process %s.' % os.getpid()
    p = Pool()

    fileList = os.listdir('./url')
    #print fileList

    all_list = []
    for f in fileList:

        fp = open('./url/'+f, 'r+')
        urls = fp.read()
        url_list = urls.split('\n')[0:-1]

        all_list += url_list
    #fp = open('./url/all.txt', 'r+')
    #urls = fp.read()
    #all_list = urls.split('\n')[0:-1]

    print len(all_list)
    listlen = len(all_list)

    for url in all_list:
        index = all_list.index(url)
        url = "http://data.eastmoney.com/report" + url
        if multi:
            p.apply_async(get_Data, args=(url,index,listlen))
        else:
            get_Data(url, index, listlen)

    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()



    t2 = time.time()

    print 'All subprocesses done. use %0.2f seconds' % (t2-t1)
