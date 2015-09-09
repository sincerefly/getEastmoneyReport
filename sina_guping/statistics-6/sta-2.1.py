#!/bin/python
#encoding:utf-8
from pymongo import MongoClient
import datetime

mongopath = "localhost"
nowDate =  datetime.datetime.now().strftime("%Y-%m-%d") # 当前日期
startDate = (datetime.datetime.now() + datetime.timedelta(days=-180)).strftime("%Y-%m-%d")
endDate = nowDate

def clientMongo():
    client = MongoClient(mongopath, 27017)
    db = client.guping
    return db if db else False

def set_company_suggest_in6m_flag(db):

    # 获取公司列表
    company_list = []
    data = db.sina_company_fs.find()
    for d in data:
        company_list.append(d["company"])

    print company_list

    # 查询公司六个月之内有无推荐
    print startDate, endDate

    for company in company_list:

        print "---"
        print company

        suggest = db.sina_article_alls.find({
                    "date": {
                        "$gte": startDate,
                        "$lte": endDate
                    },
                    "company": company
                }).count()
        print suggest

        up = {
                "in6m": suggest
        }

        #db.sina_company_fs.update({'company': company}, {'$set': up}, upsert = True)






if __name__ == '__main__':

    db = clientMongo()
    if db:
        print "client mongo success"
    else:
        print "client mongo failed"

    set_company_suggest_in6m_flag(db)



