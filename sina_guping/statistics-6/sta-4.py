#!/bin/env python2.7
#encoding:utf-8
from pymongo import MongoClient
import datetime

mongopath = "localhost"
nowDate =  datetime.datetime.now().strftime("%Y%m%d") # 当前日期
startDate = (datetime.datetime.now() + datetime.timedelta(days=-720)).strftime("%Y%m%d")
endDate = (datetime.datetime.now() + datetime.timedelta(days=-180)).strftime("%Y%m%d")

# Functions
def clientMongo():
    client = MongoClient(mongopath, 27017)
    db = client.guping
    return db if db else False

def addUptoArticle(db):

    # 获取article原始表的数据
    article_all = db.sina_article_alls.find({
            "date":{
                "$gte": startDate,
                "$lte": endDate
            }
        })

    count = 0
    db.sina_article_with_ups.remove()
    for art in article_all:
        count = count + 1
        if art["company"] == '':
            continue
        print art["code"], art["company"], art["date"]

        code = art["code"]
        company = art["company"]
        date = art["date"]
        date = date[0:4] + date[5:7] + date[8:10]
        cdata = db.sina_company_ls.find({"code": code, "company": company, "date": date})
        try:
            art["p1p2up"] = cdata[0]["p1p2up"]

        except:
            art["p1p2up"] = -1

        db.sina_article_with_ups.insert(art)


if __name__ == "__main__":

    db = clientMongo()

    if db:
        print "client mongo success"
    else:
        print "client mongo failed"

    addUptoArticle(db)

