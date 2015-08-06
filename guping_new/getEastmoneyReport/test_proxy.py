#!/usr/bin/python
#encoding:utf-8
from multiprocessing import Pool
from bs4 import BeautifulSoup
import os, time
import requests

def get_Data(url,index, listlen):
    start = time.time()
    page = requests.get(url).text
    #soup = BeautifulSoup(page, from_encoding='gb2312')
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find_all('div', class_='report-title')[0]("h1")[0].text
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
        
    print len(all_list)
    listlen = len(all_list)

    for url in all_list:
        index = all_list.index(url)
        p.apply_async(get_Data, args=(url,index,listlen))

    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()



    t2 = time.time()
	
    print 'All subprocesses done. use %0.2f seconds' % (t2-t1)
