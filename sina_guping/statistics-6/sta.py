#!/bin/env python2.7
#encoding:utf-8
from pymongo import MongoClient
import pymongo
import datetime
import sys

# Settings
mongopath = "localhost" # 数据库地址
#startDate = "20150104"  # 检索数据开始日期
#endDate = "20150529"    # 检索数据结束日期
#endDate = "20150227"    # 检索数据结束日期
nowDate =  datetime.datetime.now().strftime("%Y%m%d") # 当前日期
startDate = (datetime.datetime.now() + datetime.timedelta(days=-720)).strftime("%Y%m%d")
endDate = (datetime.datetime.now() + datetime.timedelta(days=-180)).strftime("%Y%m%d")
startDate_ = (datetime.datetime.now() + datetime.timedelta(days=-720)).strftime("%Y-%m-%d")
endDate_ = (datetime.datetime.now() + datetime.timedelta(days=-180)).strftime("%Y-%m-%d")

print startDate, endDate

# Functions
# 本方法主要用来判断脚本是否需要执行
def isNotWorkDay():
    today = datetime.datetime.now().strftime("%w")
    if today in [6, 0]: # 如果周六周日则退出脚本
        exit(0)
    print "今天是星期: " + str(today)

def the_useful_workday(d2):
    d2_w = d2.strftime("%w")
    if d2_w == "6":
        offset = -1
    elif d2_w == "0":
        offset = -2
    else:
        offset = 0

    return d2 + datetime.timedelta(days=offset)

def the_useful_workday_after(d1):
    d1_w = d1.strftime("%w")
    if d1_w == "6":
        offset = 2
    elif d1_w == "0":
        offset = 1
    else:
        offset = 0

    return d1 + datetime.timedelta(days=offset)

def clientMongo():
    client = MongoClient(mongopath, 27017)
    db = client.guping
    return db if db else False

def getArticleInfo(db):
    return db.sina_article_alls.find({
               "date":{
                   "$gte": startDate_,
                   "$lte": endDate_
               }
           }).sort("date")

def filterList(art_list, db):

    print "进入filter"

    d = {}
    i = 0
    #all_list = db.dfcf_true.find({}).sort("code", -1)
    #all_list = db.dfcf_true.find({}).sort("code", pymongo.ASCENDING)
    print "db.dfcf_true.find({})"
    all_list = db.dfcf_true.find({})

    print "db.dfcf_true.find({}) finish ..."

    print "进入循环，判断股票的上市时间"

    for art in all_list:
        i = i + 1
        codeStartDate = art["date"]
        code = art["code"][2:]

        if code in d:
            if art["date"] < d[code]["codeStartDate"]:
                d[code]["codeStartDate"] = art["date"]
        else:
            d[code] = {}
            d[code]["codeStartDate"] = art["date"]

        print i

    #for art in all_list:
    #    i = i + 1
    #    codeStartDate= art["date"]
    #    code_u = art["code"].encode("utf-8")

    #    if code_u not in d:
    #        d[code_u[2:]] = {}
    #        d[code_u[2:]]["codeStartDate"] = codeStartDate

    #print d
    print d["000099"]
    print d["002304"]
    print len(d)

    resu = []
    o = 0
    for art in art_list:
        print "in"
        o = o + 1

        postDate = art["date"]
        postCode = art["code"].encode("utf-8")
        try:
            codeStartDate = d[postCode]["codeStartDate"]

            d1 = datetime.datetime.strptime(postDate, "%Y-%m-%d")
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

    print "================="
    for aa in resu:
        if  aa["code"] == "002304":
            print aa

    return resu

def codeUp(art_list, db):


    print "= = = = = = = = = = = = = = = = ="
    for aa in art_list:
        if  aa["code"] == "002304":
            print aa




    print "进入codeUp"
    print "清空数据库数据..."
    db.sina_company_ls.remove({})

    i = 0
    ignore = 0
    ignore_index = 0
    data_list = []
    for art in art_list:
        i = i + 1

        if art["company"] == '':
            ignore = ignore + 1
            continue

        # 因为查询的股票是在一定区间的，所以需要把文章的发布日期当作股票评测的起始日期
        # 因为文章的发布日期可能为周六或者周日，所以也应该进行offset，我们这里使用
        # the_useful_workday_after 对日期后移
        d1 = datetime.datetime.strptime(art["date"], "%Y-%m-%d")
        d1_new = the_useful_workday_after(d1)
        d1_Ymd = d1_new.strftime("%Y-%m-%d")

        # FIXME
        # 这将导致一个bug，三个月的时间区间，这个91数字定死会导致结尾可能是周六或周日
        # 所以这个需要一个判断，如果是周六或者周日，那么结束日期应定在前面的周五

        # 使用the_useful_workday函数获取了结束日期为周六周日的情况
        d2 = d1 + datetime.timedelta(days=180)
        d2_new = the_useful_workday(d2)
        d2_Ymd = d2_new.strftime("%Y-%m-%d")

        print "--- --- --- ---"
        print d1_Ymd, d2.strftime("%Y-%m-%d"), d2_Ymd




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
            print d2_Ymd

            date = art["date"]
            code = art["code"]
            company = art["company"]

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
            #data_list.append(j)
            # 看看是不是方法用错了
            #db.dfcf_company_ls.update({'date':date, 'code':code, 'company':company}, {'$set':j}, upsert = True)
            if art["code"]=="002353" and art["date"]=="20150401":
                print j
            db.sina_company_ls.insert(j)

        except IndexError:
            ignore_index = ignore_index + 1
            print d1_Ymd, d2_Ymd
            continue

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

    sys.exit(0)










