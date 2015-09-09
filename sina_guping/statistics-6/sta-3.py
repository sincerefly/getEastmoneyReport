#!/bin/env python
#encoding:utf-8
from pymongo import MongoClient
import sys
import datetime

# Settings
mongopath = "localhost" # 数据库地址
startDate = "20150104"  # 检索数据开始日期
endDate = "20150529"    # 检索数据结束日期
#endDate = "20150227"    # 检索数据结束日期(三个月预留)
nowDate =  datetime.datetime.now().strftime("%Y%m%d") # 当前日期
startDate = (datetime.datetime.now() + datetime.timedelta(days=-720)).strftime("%Y%m%d")
endDate = (datetime.datetime.now() + datetime.timedelta(days=-180)).strftime("%Y%m%d")


# Functions
def isNotWorkDay():
    today = datetime.datetime.now().strftime("%w")
    if today in [6, 0]: # 如果周六周日则退出脚本
        exit(0)
    print today

def clientMongo():
    client = MongoClient(mongopath, 27017)
    db = client.guping
    return db if db else False

def getArticleInfo(db):
    return db.sina_company_ls.find({})

def startSta(art_list, db):

    # 作者排序
    print "移除作者数据"
    db.sina_author_fs.remove({})

    i = 0
    author_dict = {}
    for art in art_list:
        company = art["company"].encode("utf-8")
        author_list = art["author"]
        #print author_list
        for au in author_list:
            au = au.encode("utf-8")
            grow = art["grow"]
            if author_dict.has_key(au):
                author_dict[au]["count"] +=1
                author_dict[au]["grow"].append(grow)
            else:
                author_dict[au] = {}
                author_dict[au]["count"] = 1
                author_dict[au]["grow"] = []
                author_dict[au]["grow"].append(grow)
                author_dict[au]["company"] = company
    #print author_dict

    for key in author_dict:

        count = author_dict[key]["count"]
        grow_list = author_dict[key]["grow"]
        avgUp = round(sum(grow_list) / len(grow_list), 4)
        company = author_dict[key]["company"]

        print key + "\t" + str(count) + "\t" + str(avgUp) + "\t" + company


        author = key
        d = {
                "author": key,
                "count": count,
                "avgUp": avgUp,
                "company": company
        }

        #db.dfcf_author_f_test.insert(d)
        db.sina_author_fs.update({'author':author}, {'$set':d}, upsert = True)
    return 0


# main function
if __name__ == "__main__":

    if isNotWorkDay():
        exit(0)

    db = clientMongo()
    if db:
        print "Client Mongo Success"
    else:
        print "Client Mongo failed"
        exit(0)

    article_list = getArticleInfo(db)

    # 获取日期区间内股票涨幅情况
    startSta(article_list, db)

    sys.exit(0)























