#!/bin/env python
#encoding:utf-8
from pymongo import MongoClient
import datetime

# Settings
mongopath = "localhost" # 数据库地址
startDate = "20150104"  # 检索数据开始日期
endDate = "20150529"    # 检索数据结束日期
#endDate = "20150227"    # 检索数据结束日期(三个月预留)
nowDate =  datetime.datetime.now().strftime("%Y%m%d") # 当前日期

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
    return db.dfcf_company.find({})

def startSta(art_list, db):

    i = 0
    company_dict = {}
    for art in art_list:
        company = art["company"].encode("utf-8")
        grow = art["grow"]
        if company_dict.has_key(company):
            company_dict[company]["count"] +=1
            company_dict[company]["grow"].append(grow)
        else:
            company_dict[company] = {}
            company_dict[company]["count"] = 1
            company_dict[company]["grow"] = []
            company_dict[company]["grow"].append(grow)
    #print company_dict

    for key in company_dict:

        count = company_dict[key]["count"]
        grow_list = company_dict[key]["grow"]
        avgUP = round(sum(grow_list) / len(grow_list), 4)

        print key + "\t" + str(count) + "\t" + str(avgUP)

        d = {
                "company": key,
                "count": count,
                "avgUp": avgUP
        }

        #db.dfcf_company_f_test.insert(d)
        db.dfcf_company_f.update({'company': company}, {'$set':d}, upsert = True)
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

























