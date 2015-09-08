#!/bin/env python
#encoding:utf-8
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.guping

def getDict():
    content = requests.get("http://quote.eastmoney.com/stocklist.html").content

    #print content

    soup = BeautifulSoup(content.decode('gb2312', 'ignore'), "html.parser")

    indexlist = soup.find(class_='quotebody').find_all('li')

    thedict = {}
    for item in indexlist:
        text = item.text

        print text
        t = text.split('(')
        name, code = t[0], t[1][0:-1]
        thedict[code] = name

    for key in thedict.keys():
        print key, thedict[key]

    return thedict


def getArticleList():

    artlist = db.sina_article_alls.find({})

    return artlist



if __name__ == "__main__":

    thedict = getDict()

    art_list = getArticleList()

    i = 0
    for art in art_list:
        i = i + 1

        code = art["code"]
        company = art["company"]
        date = art["date"]

        try:
            name2 = thedict[code]
        except:
            continue

        up = {
                "name2": name2
        }

        print code, name2, company

        db.sina_article_alls.update({"company": company, "date": date, "code": code}, {"$set": up}, upsert = True)


    print i









