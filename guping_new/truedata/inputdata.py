#!/bin/env python
#encoding:utf-8
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.guping

#f = open('data.csv', 'r')
f = open('SH000300/SH000300.csv', 'r')
row = f.readline()

l = []
i = 0
while row:
    i = i + 1
    row = row.split(',')
    j = {
            'code': str(row[0]),
            'date': str(row[1]),
            'startPrice': float(row[2]),
            'maxPrice': float(row[3]),
            'lowPrice': float(row[4]),
            'endPrice': float(row[5]),
            'counts': int(row[6]),
            'volume': row[7][0:-1]
    }

    l.append(j)

    if i % 1000 == 0:
        #db.dfcf_true_sh300.insert(l)
        db.dfcf_true_sh300.update({'code':code, 'date':date}, {'$set':l}, upsert = True)
        l = []
        print i

    row = f.readline()

#db.dfcf_true_sh300.insert(l)
db.dfcf_true_sh300.update({'code':code, 'date':date}, {'$set':l}, upsert = True)
print len(l)

