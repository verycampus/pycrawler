#!/usr/bin/env python
#!coding=utf-8

#名字为config的dict会被当做当前配置文件

config = {
    # 京东
    'jingdong' : {
        'seeds':[{'url':'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=1','parsed':False,'depth':0},
          ],
        'depth':1,
        #所有符合规则的item都会被抓取，按照or模式匹配
        'item_patterns':[r'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=\d+$',r'http://www.360buy.com/product/\d+\.html$'],
        #翻页不需要计算depth，看见就抓
        'page_patterns':[r'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=\d+$'],
        #除了达到指定的depth，url匹配到这里也会停止抓取
        'stop_patterns':[r'http://search.360buy.com/Search?keyword=%C0%F1%CE%EF&area=1&qr=%40%23%24%25&page=10$'],
        #哪些字段需要被抓取下来
        'contents':[
                    {'name':u'标题','xpath':'//*[@id="i-detail"]/*[1]'},
                   ],
        'encoding':'gbk',
        'thread_number':10,
        'max_number':50
    },
    # 微博
    'weibo' : {
        'seeds':[{'url':'http://weibo.com/royguo1988','parsed':False,'depth':0},
          ],
        'depth':1,
        #所有符合规则的item都会被抓取，按照or模式匹配
        'item_patterns':[r'http://weibo.com/royguo1988/\S+',r'http://weibo.com/\d+/\S+'],
        #翻页不需要计算depth，看见就抓
        'page_patterns':[],
        #除了达到指定的depth，url匹配到这里也会停止抓取
        'stop_patterns':[],
        #哪些字段需要被抓取下来
        'contents':[
                    {'user':u'作者','xpath':'//*[@id="pl_content_personInfo"]/div[1]/dl/dd/a[1]'},
                    {'user':u'内容','xpath':'//*[@id="pl_content_weiboDetail"]/div[1]/dl/dd/p[1]/em'},
                   ],
        'encoding':'utf-8',
        'thread_number':10,
        'max_number':200
    }
 
}
