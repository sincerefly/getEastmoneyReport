# getEastmoneyReport
GET http://data.eastmoney.com/report/

这个小爬虫可以用来获取东方财富网的股评数据

并保存到mongodb数据库中

基于Phantomjs，去官网了解怎么安装。如果你是Fedora系统，可以直接找我要编译好的可执行文件。 

Email: `kissbug8720@gmail.com`

- run.py 爬虫文件(获取report列表的股评信息)
- run-2.py 爬虫文件(在之前的基础上增加了进入详情页获取作者的功能)
- hello.js 测试phantomjs能否运行(终端phantomjs hello.js)
- test.py 本地测试抓取使用，配合index.html
- ~~index.html~~ 为phantomjs获取的文件(已从github上删除，测试的话自己保存吧)
- test_singleprocessing.py 单进程获取50个详情页的文章标题
- test_multiprocessing.py 多进程的获取50个详情页的文章标题

*程序中有代码注释, 不多介绍了, 新学爬虫的同学可以参考下*
