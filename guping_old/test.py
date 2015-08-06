#!/bin/env python
#encoding:utf-8
import re
import json
#import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup

# read file
f = open('index.html', 'r')
html = f.read()
#print html

# re
#pattern = re.compile(r'firstInit\(([\s\S]+)\);'?)
#pattern = re.compile(r'firstInit\(([\s\S]+?)\);')
pattern = re.compile(r'<tbody>([\s\S]+)</tbody>')
match = pattern.search(html)

if match:
    print 'yes'
    string = match.group(1)
    print string
    #json = json.loads(string)
    #data = json['data']
else:
    print 'no'

# mongodb
#client = MongoClient('localhost', 27017)

#db = client.guping

#db.dfcf.insert(data)


for row in BeautifulSoup(string)("tr"):
    print row("td")[1]("span")[0]["title"]
    print '-'*6
    for i in row("td"):
        #print i.text
        print i

    print "!!!!"
    data = {
        "date": row("td")[1]("span")[0]["title"],
        "code": row("td")[2].text,
        "name": row("td")[3].text,
        "title": row("td")[5].text,
        "suggest": row("td")[6].text,
        "change": row("td")[7].text,
        "author": row("td")[8].text,
        "a1": row("td")[9].text,
        "a2": row("td")[10].text,
        "b1": row("td")[11].text,
        "b2": row("td")[12].text,
    }
    print data
