#!/usr/bin/env python
#coding:utf-8

import os
import  threading
numlock =threading.RLock() #线程锁 操作在线数时必须要请求此锁
prlock=threading.RLock()   #输出锁 子线程在显示器上输出时必须请求此锁（防止输出错位）
zxs=0                      #在线数
a =''
class pings(threading.Thread):
    def __init__(self,num,interval,net):
        threading.Thread.__init__(self)
        self.nums=num
        self.network =net
        self.inter=interval
        self.thread_stop=False
        self.ns=0
    def run(self ):
        global a

        global zxs
        start=self.nums
        startnet = self.network
        while start<255:
            ret=os.system('ping -c 1 -W 1 %s.%d >/dev/null' %(startnet,start))
            if not ret:
                prlock.acquire()#请求输出锁
                b = '%s.%d ok'%(startnet,start)
                a = a + b +'\n'
                prlock.release()#释放输出锁
                self.ns +=1
            start+=self.inter
        numlock.acquire()   #请求数操作锁
        zxs+=self.ns
        numlock.release()   #释放数操作锁
        # print(a)

def pingt(network):
    s = 255
    r = s-1
    threads = []
    for i in range(1,s):
        t=pings(i,r,network)
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    global zxs
    # print(zxs,'个ip在线')  #输出在线数
    return a



#跟踪路由路径
import subprocess
def trace_route(ip_addr):
    p = subprocess.Popen("traceroute %s"%ip_addr,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    p.wait()
    ipline = ''
    while True:
        line = p.stdout.readline().decode()
        ipline += '\n'+ line +'\n'
        if not line:
            break
    return ipline


