#!/bin/env python
#encoding:utf-8
from pymongo import MongoClient
import datetime

# Settings
mongopath = "localhost" # 数据库地址
startDate = "20150104"  # 检索数据开始日期
endDate = "20150529"    # 检索数据结束日期
#endDate = "20150227"    # 检索数据结束日期
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
    return db.dfcf_article_all.find({
               "date":{
                   "$gte": startDate,
                   "$lte": endDate
               }
           }).sort("date")

def filterList(art_list, db):

    d = {}
    i = 0
    all_list = db.dfcf_true.find({}).sort("code")
    for art in all_list:
        i = i + 1
        codeStartDate= art["date"]
        code_u = art["code"].encode("utf-8")

        if code_u not in d:
            d[code_u[2:]] = {}
            d[code_u[2:]]["codeStartDate"] = codeStartDate

    #print d
    #print d["000099"]

    resu = []
    o = 0
    for art in art_list:
        o = o + 1

        postDate = art["date"]
        postCode = art["code"].encode("utf-8")
        try:
            codeStartDate = d[postCode]["codeStartDate"]

            d1 = datetime.datetime.strptime(postDate, "%Y%m%d")
            d2 = datetime.datetime.strptime(codeStartDate, "%Y-%m-%d")
        except:
            continue

        print postCode + ' ' + str((d1-d2).days)
        if (d1 - d2).days > 90:
            resu.append(art)

    print i
    print "len d: " + str(len(d))
    print o
    print "len r: " + str(len(resu))

    return resu

def codeUp(art_list, db):

    i = 0
    ignore = 0
    ignore_index = 0
    data_list = []
    for art in art_list:
        i = i + 1

        if art["company"] == '':
            ignore = ignore + 1
            continue

        d1 = datetime.datetime.strptime(art["date"], "%Y%m%d")
        d1 = datetime.datetime.strptime("20150227", "%Y%m%d")
        d1_Ymd = d1.strftime("%Y-%m-%d")
        d2 = d1 + datetime.timedelta(days=91)
        d2_Ymd = d2.strftime("%Y-%m-%d")

        #print "------"
        #print d1_Ymd
        #print d2_Ymd
        #print art["code"]
        #print art["company"]
        #print "------"

        data1 = db.dfcf_true.find({"date": d1_Ymd, "code":{"$regex":art["code"]}})
        data2 = db.dfcf_true.find({"date": d2_Ymd, "code":{"$regex":art["code"]}})
        SH1 = db.dfcf_true_sh300.find({"date": d1_Ymd})
        SH2 = db.dfcf_true_sh300.find({"date": d2_Ymd})
        try:
            p1, p2 = data1[0]["startPrice"], data2[0]["startPrice"]
            sh1, sh2 = SH1[0]["startPrice"], SH2[0]["startPrice"]
            p1p2up = round((p2-p1)/p1, 4)*100
            sh1sh2up = round((sh2-sh1)/sh1, 4)*100
            #print p1p2up, sh1sh2up, (p1p2up-sh1sh2up), abs(p1p2up), (p1p2up - sh1sh2up)/abs(p1p2up)
            grow = round((p1p2up - sh1sh2up), 4)
            print art["date"], art["code"], art["company"], p1, p2, \
                  str(p1p2up)+"%", str(sh1sh2up)+"%", str(grow)

            j = {
                    "date": art["date"],
                    "code": art["code"],
                    "company": art["company"],
                    "author": art["author"],
                    "startPrice_code": p1,
                    "endPrice_code": p2,
                    "startPrice_300": sh1,
                    "endPrice_300": sh2,
                    "p1p2up": p1p2up,
                    "sh1sh2up": sh1sh2up,
                    "grow": grow
            }
            data_list.append(j)

        except IndexError:
            ignore_index = ignore_index + 1
            continue

        if len(data_list) == 1000:
            #db.dfcf_company_test.insert(data_list)
            db.dfcf_company.update({'date':date, 'code':code, 'company':company}, {'$set':data_list}, upsert = True)
            data_list = []

    #db.dfcf_company_test.insert(data_list)
    db.dfcf_company.update({'date':date, 'code':code, 'company':company}, {'$set':data_list}, upsert = True)
    print "all" + ": " + str(i)
    print "ignore" + ": " + str(ignore)
    print "ignore_index" + ": " + str(ignore_index)

    return 0


def code300Up(art_list):
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

    # 过滤新股
    article_list = filterList(article_list, db)

    # 获取日期区间内股票涨幅情况
    codeup_list = codeUp(article_list, db)

    # 获取日期区间内SH000300的涨幅情况
    #code300up_list = code300Up(article_list)























