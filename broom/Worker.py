#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading,Queue,time,logging
from Sync import Sync
import Config,Logger,QueuePool

logger = Logger.getInstance()

'''
customer for queue
'''
class Worker(threading.Thread):
    def __init__(self, events_queue):
        super(Worker, self).__init__()
        self.syncQueue = events_queue
        self.config = Config.getInstance()
        self.sleeptime = self.config.get('client', 'sleeptime')
        self.nochangetime = self.config.get('client', 'nochangetime')
        self.startTime = time.time()

    def run(self):
        while True:
            runTime = time.time()-self.startTime
            if runTime >  43200:
                logger.info('life end  exit...')
                exit()
            else:
                blockTime = 43200 - runTime
            logger.debug('run...')
            try:
                event = self.syncQueue.get(True, blockTime)
            except Exception as e:
                logger.info('queue empty go sleep...')
                needSleep = True

            logger.info('get file: '+event)
            if not os.path.isfile(event):
                time.sleep(5)
                continue
            if Sync.needSync(event, float(self.nochangetime)):
                logger.info(' upload file:'+event)
                res = Sync.upload(event)
                if not res:            
                    self.syncQueue.put(event)
                time.sleep(5)
            else:
                logger.info('in changeing: '+event)
                needSleep = False
                if self.syncQueue.empty():
                    logger.info('needsleep')
                    needSleep = True
                cq = QueuePool.getQueue('changeing')
                cq.put(event)
                time.sleep(5)
                logger.debug('skeep..')
                if needSleep:
                    logger.info('in sleep '+self.sleeptime)
                    time.sleep(float(self.sleeptime))

if __name__ == '__main__':
    logger.debug(1)
