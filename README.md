# getEastmoneyReport
GET http://data.eastmoney.com/report/

这个小爬虫可以用来获取东方财富网的股评数据

并保存到mongodb数据库中

基于Phantomjs，去官网了解怎么安装。如果你是Fedora系统，可以直接找我要编译好的可执行文件。

- run.py 爬虫文件
- hello.js 测试phantomjs能否运行
- test.py 本地测试使用，配合index.html
- index.html 为phantomjs获取的文件(部分)

*程序中有代码注释, 不多介绍了, 新学爬虫的同学可以参考下*
