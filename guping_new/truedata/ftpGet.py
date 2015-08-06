#!/usr/bin/env python
#encoding:utf-8
import os
import ftplib
import shutil
import patoolib
import datetime

def isWorkDay():

    today = datetime.datetime.now().strftime("%w")
    if today in [6, 0]: # 如果周六周日则退出脚本
        exit(0)

    nowDate = datetime.datetime.now()
    yesterday = nowDate + datetime.timedelta(days=-1)
    yesterdayYmd = yesterday.strftime("%Y%m%d")
    return yesterdayYmd


def getFileFromFTP(date):

    filename = date
    path = '.'
    filename = filename + '.rar'

    ftp = ftplib.FTP("xx.xx.xx.xx")
    ftp.login("xxxxxx", "xxxxxx")
    ftp.cwd(path)
    ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
    ftp.quit()

def unpackRAR(date):

    filename = date + '.rar'
    patoolib.extract_archive(filename, outdir=".")

    # 将原文件移动到新的目录‘newdata’中
    oldfilepath = "./ProcessFile/Stk_Day/Stk_Day_Idx_Daily/%s.csv" % date
    newfilepath = "./newdata/"
    shutil.move(oldfilepath, newfilepath)

    # 删除rar归档及ProcessFile
    shutil.rmtree("./ProcessFile")
    os.remove(filename)


if __name__ == '__main__':

    # 获取脚本运行时上一天的日期
    date = isWorkDay()

    # 从FTP上获取更新文件
    getFileFromFTP(date)

    # 解包rar数据
    unpackRAR(date)

