#!/usr/bin/env python
# -*- conding:utf-8 -*-

import Queue,threading,time,logging,Worker

class WorkerTest(threading.Thread):
    def __init__(self):
        super(WorkerTest, self).__init__()

    def run(self):
        i = 1
        while i<6:
            logging.debug(self.name+':'+str(i))
            i = i+1
        print 'end'
        exit()

class ThreadPool:

    @classmethod
    def start(cla, max, queue):
        pool = []
        while True:
            logging.debug('pool len:'+str(len(pool)))
            for i in pool:
                if not i.isAlive():
                    pool.remove(i)
            while len(pool) < max:
                a = Worker.Worker(queue)
                a.setDaemon(True)
                a.start()
                logging.debug('create thread:'+a.name)
                pool.append(a)
            time.sleep(5)
