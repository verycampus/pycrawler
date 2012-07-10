#!/usr/bin/env python
#!coding=utf-8

# system deps
from BeautifulSoup import *
import re
import lxml
from lxml import etree
import sys
import urllib2
from urlparse import urljoin

# user deps
import configure

# 已经抓取到的链接，用来保证单个链接只需要抓取一次
existLinks = set()
# 抓取链接队列，包含链接的基本信息：{url,parsed,depth}
links = []

class Crawler:
  # init class
  def __init__(self):
    global links
    self.seeds = configure.config['seeds']
    self.depth = configure.config['depth']
    self.patterns = configure.config['patterns']
    self.contents = configure.config['contents']
    links = self.seeds

  # execute crawler
  def crawl(self):
    global links
    print 'start crawling'

    for i in range(self.depth):
      newUrls = []
      for link in links:
        print 'link = %s ' % link['url']
        try:
          c = self.openUrl(link['url'])
        except:
          print 'Could not open %s' % link['url']
          print 'Error Info : %s ' % sys.exc_info()[1]
          continue
        html = c.read()
        self.extractContent(html)
        extractLinks = self.extractLinks(link['url'],html,i)
        newUrls.extend(extractLinks)
      links = newUrls

  # regrex patterns use "or".
  def filterUrl(self,url):
    if url in existLinks:
      return False
    match = False
    for p in self.patterns:
      p = re.compile(p)
      if p.findall(url):
        match = True
    return match

  # open a url with browser headers
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

  #extract links from a web page
  def extractLinks(self,referer,html,depth):
    links = []
    soup = BeautifulSoup(html)
    tags = soup('a')
    for l in tags:
      if ('href' in dict(l.attrs)):
        url = urljoin(referer,l['href'])
        url = url.split('#')[0]
        if(self.filterUrl(url)):
          links.append({'url':'%s' % url,'parsed':False,'depth':depth+1})
          existLinks.add(url)
    return links

  # extract content from html using xpath
  def extractContent(self,html):
    parser = etree.XMLParser(ns_clean=True, recover=True)
    tree = etree.fromstring(html,parser)
    for c in self.contents:
      m = tree.xpath(c['xpath'])
      if len(m) == 1:
        print c['name'] + ' : ' + m[0].text
