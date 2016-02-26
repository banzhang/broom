#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue,threading,time,logging,Worker,Config
import Logger,QueuePool

logger = Logger.getInstance()

class WorkerTest(threading.Thread):

    def __init__(self):
        super(WorkerTest, self).__init__()

    def run(self):
        i = 1
        while i<6:
            logger.debug(self.name+':'+str(i))
            i = i+1
        logger.info('end')
        exit()

class ThreadPool:

    def __init__(self):
        super(ThreadPool, self).__init__()
        self.EmptyTime = 0
        

    @classmethod
    def start(cla, max, queue):
        pool = []
        
        while True:
            logger.debug('pool len:'+str(len(pool)))
            for i in pool:
                if not i.isAlive():
                    pool.remove(i)
            while len(pool) < max:
                a = Worker.Worker(queue)
                a.setDaemon(True)
                a.start()
                logger.info('create thread:'+a.name)
                pool.append(a)
            time.sleep(5)
            cla.emptyCheck(queue)

    @classmethod
    def emptyCheck(cla, queue):
        self.EmptyTime = EmptyTime+5
        
        if self.EmptyTime >= 605:
            cq = QueuePool.get('changeing')
            while 1:
                try:
                    event = cq.get(False)
                    queue.put(event)
                except Exception, e:
                    self.EmptyTime = 0
                    return True
