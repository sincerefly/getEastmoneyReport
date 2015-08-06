#!/usr/bin/python
#encoding:utf-8
from multiprocessing import Pool
from bs4 import BeautifulSoup
import os, time
import requests
import re

# Setting
multi = 0

def get_Data(url,index, listlen):
    start = time.time()
    try: 
        page = requests.get(url).text
    except requests.exceptions.MissingSchema:
        pass

    #soup = BeautifulSoup(page, from_encoding='gb2312')
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find_all('div', class_='report-title')[0]("h1")[0].text
    end = time.time()
    print '(%s/%s)%s runs %0.2f seconds.' % (index+1, listlen, title, (end - start))
    
    name_code = soup.find_all('div', class_='tit')[0]("a")[0].text
    l = re.split('\(|\)', name_code)
    name = l[0]
    code = l[1]
    date = soup.find_all('div', class_='report-infos')[0]("span")[1].text
    company = soup.find_all('div', class_='report-infos')[0]("span")[2].text
    author = soup.find_all('div', class_='report-infos')[0]("span")[3].text
    print '    -> %s' % name  
    print '    -> %s' % code 
    print '    -> %s' % date 
    print '    -> %s' % company  
    print '    -> %s' % author 

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
        
    print len(all_list)
    listlen = len(all_list)

    all_list = [
        'http://data.eastmoney.com/report/20150715/APPGNQdhDeWrASearchReport.html',
        'http://data.eastmoney.com/report/20150715/APPGNQdhDeTlASearchReport.html',
        'http://data.eastmoney.com/report/20150715/APPGNQdhDea3ASearchReport.html',
        'http://data.eastmoney.com/report/20150324/APPGLqwaaLtSASearchReport.html'
    ]

    for url in all_list:
        index = all_list.index(url)
        if multi:
            p.apply_async(get_Data, args=(url,index,listlen))
        else:
            get_Data(url, index, listlen)

    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()



    t2 = time.time()
	
    print 'All subprocesses done. use %0.2f seconds' % (t2-t1)
