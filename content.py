#!/usr/bin/env python
#!coding=utf-8
'''
  @author royguo1988@gmail.com
  该类用来处理需要输出的内容，按照json编码方式存储，非ascii字符会被转为ascii字符
'''
from Queue import Queue
from threading import Thread
import time
import json

class Content:

  def __init__(self):
    self.outputs = Queue()

    d = time.strftime('%y-%m-%d %H-%M',time.localtime())
    self.f = open(d + '.txt','a')
    self.f.write('[')
    
    t = Thread(target=self.run)
    t.setDaemon(True)
    t.start()

  def __del__(self):
    self.outputs.join()
    self.f.write(']')
    self.f.close()

  def write(self,url,dom,targets):
    result = {}
    result['url'] = url
    if dom != None:
      for t in targets:
        m = dom.xpath(t['xpath'])
        if len(m) >= 1:
          result[t['name']] = m[0].text
    output = json.dumps(result) + ',\n'
    self.outputs.put(output)

  def run(self):
    while True:
      output = self.outputs.get()
      self.f.write(output)
