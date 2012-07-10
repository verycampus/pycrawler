#!/usr/bin/env python

from BeautifulSoup import *
import re
import lxml
from lxml import etree
import sys
import urllib2
from urlparse import urljoin

config = {
    'seeds':['http://movie.douban.com'],
    'depth':3,
    'patterns':[r'http://movie.douban.com/subject/\d+/$',r'http://movie.douban.com$'],
    'contents':[
                {'name':'name','xpath':'//span[@property="v:itemreviewed"]'},
                {'name':'year','xpath':'//span[@class="year"]'}
               ]
    }

class Crawler:
  # init class
  def __init__(self):
    self.seeds = config['seeds']
    self.depth = config['depth']

  # execute crawler
  def crawl(self):
    print 'start crawling'
    links = self.seeds

    for i in range(self.depth):
      newUrls = set()
      for link in links:
        print 'link = %s ' % link
        try:
          c = self.openUrl(link)
        except:
          print 'Could not open %s' % link
          print 'Error Info : %s ' % sys.exc_info()[1]
          continue
        html = c.read()
        self.extractContent(html)
        extractLinks = self.extractLinks(link,html)
        newUrls = newUrls.union(extractLinks)
      links = newUrls

  # regrex patterns use "or".
  def filterUrl(self,url):
    match = False
    for p in config['patterns']:
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
  def extractLinks(self,referer,html):
    links = set()
    soup = BeautifulSoup(html)
    tags = soup('a')
    for l in tags:
      if ('href' in dict(l.attrs)):
        url = urljoin(referer,l['href'])
        url = url.split('#')[0]
        if(self.filterUrl(url)):
          links.add(url)
    return links

  # extract content from html using xpath
  def extractContent(self,html):
    contents = config['contents']
    parser = etree.XMLParser(ns_clean=True, recover=True)
    tree = etree.fromstring(html,parser)
    for c in contents:
      m = tree.xpath(c['xpath'])
      if len(m) == 1:
        print c['name'] + ' : ' + m[0].text
