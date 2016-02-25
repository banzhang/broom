#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading,Queue,time,logging
from Sync import Sync
import Config,Logger

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
                logger.debug('exit...')
                exit()
            else:
                blockTime = 43200 - runTime
            logger.debug('run...')
            try:
                event = self.syncQueue.get(True, blockTime)
            except Exception as e:
                logger.debug('exit...')
                exit()
            logger.info('get file: '+event)
            if Sync.needSync(event, float(self.nochangetime)):
                logger.debug('upload')
                res = Sync.upload(event)
                if not res:
                    self.syncQueue.put(event)
                time.sleep(5)
            else:
                logger.debug('in changeing: '+event)
                needSleep = False
                if self.syncQueue.empty():
                    logger.debug('needsleep')
                    needSleep = True
                self.syncQueue.put(event)
                logger.debug('skeep..')
                if needSleep:
                    logger.debug('sleep '+self.sleeptime)
                    time.sleep(float(self.sleeptime))

if __name__ == '__main__':
    logger.debug(1)
