#!/usr/bin/env python
#!coding=utf-8

config = {
    'seeds':[
             {'url':'http://movie.douban.com','parsed':False,'depth':0},
      ],
    'depth':3,
    'patterns':[r'http://movie.douban.com/subject/\d+/$',r'http://movie.douban.com$'],
    'contents':[
                {'name':u'标题','xpath':'//span[@property="v:itemreviewed"]'},
               ]
    }

config_news_163 = {
    'seeds':[
             {'url':'http://news.163.com','parsed':False,'depth':0},
      ],
    'depth':3,
    'patterns':[r'http://news.163.com/12/0710/[\s\S]+\.html$',r'http://news.163.com$'],
    'contents':[
                {'name':u'标题','xpath':'//div[@class="endContent"]/h1[1]'},
               ]
    }
