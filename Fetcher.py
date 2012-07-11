#!/usr/bin/env python
#!coding=utf-8

# 系统模块
from BeautifulSoup import BeautifulSoup
from lxml import etree
from Queue import Queue
from threading import Lock,Thread,current_thread
from urlparse import urljoin

import urllib2
import time
import re
import sys

# 自定义模块
import configure

# crawler会不断的把待爬取链接push到Fetcher实例
# Fetcher实例创建多个线程对待爬取链接进行解析

class Fetcher:
  # 初始化数据
  def __init__(self,thread_number = 3):
    self.thread_number = thread_number
    self.lock = Lock()
    self.links = Queue()
    self.exist = set()
    self.running = 0

    self.patterns = configure.config['patterns']
    self.contents = configure.config['contents']
    self.depth = configure.config['depth']
    self.seeds = configure.config['seeds']

  #解构的时候不必等待队列完成
  def __del__(self):
    #self.links.join()
    pass

  #启动线程
  def start(self):
    for i in range(self.thread_number):
      t = Thread(target = self.run)
      t.setDaemon(True)
      t.start()

    for seed in self.seeds:
      self.push(seed)

  #终止所有线程
  def stop(self):
    pass

  #增加任务数据
  def push(self,link):
    if link['url'] not in self.exist:
      self.links.put(link)
      self.exist.add(link['url'])

  #获得当前运行的线程数
  def get_running_count(self):
    return self.running

  #多线程主函数
  def run(self):
    with self.lock:
      self.running += 1
    while True:
      link = self.links.get()

      thread_name = current_thread().name
      print 'thread = %s,link = %s' % (thread_name,link['url'])
      response = self.openUrl(link['url'])
      html = response.read()
      self.extractContent(html)
      self.extractLinks(link['url'],html,link['depth'])

      self.links.task_done()

  #过滤不需要的url链接，配置文件中的正则条件使用"or"模式
  def filterUrl(self,url):
    if url in self.exist:
      return False
    match = False
    for p in self.patterns:
      p = re.compile(p)
      if p.findall(url):
        match = True
    return match

  #打开url链接，返回数据流
  def openUrl(self,url):
    headers = {
            'User-Agent':'Mozilla/5.0 \
                (Macintosh; Intel Mac OS X 10_6_8) \
                AppleWebKit/536.5 (KHTML, like Gecko) \
                Chrome/19.0.1084.56 Safari/536.5'
    }
    req = urllib2.Request(
            url = url,
            data = None,
            headers = headers)
    c = urllib2.urlopen(req)
    return c

  #从某个网页解析出所以符合条件的下一层链接
  def extractLinks(self,referer,html,depth):
    soup = BeautifulSoup(html)
    tags = soup('a')
    for l in tags:
      if ('href' in dict(l.attrs)):
        url = urljoin(referer,l['href'])
        url = url.split('#')[0]
        if (depth+1) <= self.depth and self.filterUrl(url):
          link = {'url':'%s' % url,'parsed':False,'depth':depth+1}
          self.push(link)
          self.exist.add(url)

  #从某个网页解析出需要的内容 
  def extractContent(self,html):
    parser = etree.XMLParser(ns_clean=True, recover=True)
    tree = etree.fromstring(html,parser)
    for c in self.contents:
      m = tree.xpath(c['xpath'])
      if len(m) == 1:
        print c['name'] + ' : ' + m[0].text
