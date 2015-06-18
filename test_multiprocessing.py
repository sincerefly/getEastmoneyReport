from multiprocessing import Pool
from bs4 import BeautifulSoup
import os, time, random
import requests

def get_Data(url):
    start = time.time()
    page = requests.get(url).text
    soup = BeautifulSoup(page, from_encoding='gb2312')
    title = soup.find_all('div', class_='report-title')[0]("h1")[0].text
    end = time.time()
    print '%s runs %0.2f seconds.' % (title, (end - start))
#    print 'Run task %s (%s)...' % (name, os.getpid())
#    start = time.time()
#    time.sleep(random.random() * 3)
#    end = time.time()
#    print 'Task %s runs %0.2f seconds.' % (name, (end - start))


def long_time_task(name):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (name, (end - start))

if __name__=='__main__':
    t1 = time.time()
    print 'Parent process %s.' % os.getpid()
    p = Pool()
    url_list = [
        'http://data.eastmoney.com/report/20150430/APPGMH5GQzzLASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GQzpUASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GQzzHASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GQzzRASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GQzzIASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GR2ILASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GR2bKASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GR2beASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GR33EASearchReport.html',
        'http://data.eastmoney.com/report/20150430/APPGMH5GR35UASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulMpASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulMBASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulU5ASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulYxASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulVEASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulbKASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SuleSASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulhqASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulndASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SultcASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8Sum4AASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SulzuASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8Sum9nASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumHqASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumIsASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumIgASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumIhASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumJwASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumLNASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumNdASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumPCASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEpcGASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumQeASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumS1ASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumTrASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumUZASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumbJASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumjDASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumjGASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SumwVASearchReport.html',
        'http://data.eastmoney.com/report/20141218/APPFjG8SunBJASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEnnUASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEnqMASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEnmZASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEnrgASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEp7YASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEp7TASearchReport.html',
        'http://data.eastmoney.com/report/20150616/APPGN2AwEpI1ASearchReport.html',
        'http://data.eastmoney.com/report/20150615/APPGN1vwyGuYASearchReport.html',
        'http://data.eastmoney.com/report/20150615/APPGN1vwyGwaASearchReport.html'
    ]
	
    for url in url_list:
        #p.apply_async(long_time_task, args=(i,))
        p.apply_async(get_Data, args=(url,))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    t2 = time.time()
	
    print 'All subprocesses done. use %0.2f seconds' % (t2-t1)
