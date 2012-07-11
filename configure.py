#!/usr/bin/env python
#!coding=utf-8

#名字为config的dict会被当做当前配置文件

config_163 = {
    'seeds':[{'url':'http://news.163.com','parsed':False,'depth':0},
      ],
    'depth':1,
    #所有符合规则的item都会被抓取，按照or模式匹配
    'item_patterns':[r'http://news.163.com/12/0710/[\s\S]+\.html$',r'http://news.163.com$'],
    #翻页不需要计算depth，看见就抓
    'page_patterns':[],
    #除了达到指定的depth，url匹配到这里也会停止抓取
    'stop_patterns':[],
    #哪些字段需要被抓取下来
    'contents':[
                {'name':u'标题','xpath':'//*[@id="h1title"]'},
               ],
    #网页编码,自动探测太耗费性能，手动指定比较合适
    'encoding':'gb2312'
    }

#京东礼物
config = {
    'seeds':[{'url':'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=1','parsed':False,'depth':0},
      ],
    'depth':1,
    #所有符合规则的item都会被抓取，按照or模式匹配
    'item_patterns':[r'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=\d+$',r'http://www.360buy.com/product/\d+\.html$'],
    #翻页不需要计算depth，看见就抓
    'page_patterns':[r'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=\d+$'],
    #除了达到指定的depth，url匹配到这里也会停止抓取
    'stop_patterns':[r'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=\d+$'],
    #哪些字段需要被抓取下来
    'contents':[
                {'name':u'标题','xpath':'//*[@id="i-detail"]/*[1]'},
               ],
    'encoding':'gbk'
    }
