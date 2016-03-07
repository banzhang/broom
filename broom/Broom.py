#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pyinotify,Queue,threading,time,os,argparse
from ThreadPool import ThreadPool
from LogClient import LogClient
from EventHandler import EventHandler
import Config

class Broom:

    @classmethod
    def getFileList(cla, dir, fileList):
        newDir = dir
        if os.path.isfile(dir):
            fileList.append(dir)
        elif os.path.isdir(dir):  
            for s in os.listdir(dir):
                newDir=os.path.join(dir,s)
                cla.getFileList(newDir, fileList)  
        return fileList

    @classmethod
    def reBuildQueue(cla, q):
        fl = cla.getFileList(cla.watchdir, [])
        logServer = cla.config.get('client', 'sip')
        port = cla.config.get('client', 'sport')
        client = LogClient(logServer, port)
        for i in fl:
            if not client.checkFile(i):
                q.put(i)
            else:
                os.remove(i)

    @classmethod
    def buildNotify(cla, path, mask):
       workerPool = list()
       syncQueue = Queue.Queue()
       cla.reBuildQueue(syncQueue)
       wm = pyinotify.WatchManager()
       workernum = cla.config.get('client', 'workernum')
       workernum = int(workernum)
       pool = threading.Thread(target=ThreadPool.start, args=(workernum, syncQueue))
       pool.setDaemon(True)
       pool.start()
       notifier = pyinotify.Notifier(wm,EventHandler(syncQueue)) 
       wdd = wm.add_watch(path,mask,rec=True, auto_add=True)
       notifier.loop() 

    @classmethod
    def run(cla):
       cla.config = Config.getInstance()
       cla.watchdir = cla.config.get('client', 'watchdir')
       mask =  pyinotify.IN_CREATE|pyinotify.IN_MOVED_TO
       cla.buildNotify(cla.watchdir, mask)

if __name__ == '__main__': 
   Broom.run()
