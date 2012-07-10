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
