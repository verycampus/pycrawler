#!/usr/bin/env python
#!coding=utf-8

import time
import fetcher

try:
  import BeautifulSoup
except:
  print '请先下载安装Python BeautifulSoup模块,可以使用easy_install BeautifulSoup命令'

try:
  import lxml
except:
  print '请先下载安装Python lxml模块，可以使用easy_install lxml命令'

class Crawler:

  #启动爬虫 
  def crawl(self,config):
    print 'start crawling'
    #实例化多线程抓取模块，指定3个线程
    f = fetcher.Fetcher(config)
    f.start()

    while f.get_running_count() > 0:
      print '------------ running threads : %s ------------' % f.get_running_count()
      time.sleep(5)

    f.printFinishLog()
      
