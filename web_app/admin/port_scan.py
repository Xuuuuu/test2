#!/usr/bin/python3
# -*- coding: utf-8 -*-
from socket import *
import threading
import queue

lock = threading.Lock()
openNum = 0
threads = []
openport =[]

q =queue.Queue()
host='127.0.0.1'


def portScanner(host,port):

    global openNum
    try:
        s = socket(AF_INET,SOCK_STREAM)
        s.connect((host,port))
        lock.acquire()
        openNum+=1
        q.put(port)
        lock.release()
        s.close()
    except:
        pass
    return

def port_main():
    # p = argparse.ArgumentParser(description='Port scanner!.')
    # p.add_argument('-H', dest='hosts', type=str)
    # args = p.parse_args()
    # hostList = args.hosts.split(',')
    # setdefaulttimeout(1)
    # for host in hostList:
    #     print('Scanning the host:%s......' % (host))
    result = []
    for p in range(1,120):
        t = threading.Thread(target=portScanner,args=(host,p))
        threads.append(t)
        t.start()
        # for t in threads:
        #     t.join()
        while not q.empty():
            result.append(q.get())
    return result

        # print('[*] The host:%s scan is complete!' % (host))
        # print('[*] A total of %d open port ' % (openNum))



