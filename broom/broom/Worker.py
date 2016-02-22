#!/usr/bin/env python

import threading,Queue,time,logging
from Sync import Sync
import Config
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
                logging.debug('exit...')
                exit()
            else:
                blockTime = 43200 - runTime
            logging.debug('run...')
            try:
                event = self.syncQueue.get(True, blockTime)
            except Exception as e:
                logging.debug('exit...')
                exit()
            logging.info('get file: '+event)
            if Sync.needSync(event, float(self.nochangetime)):
                logging.debug('upload')
                res = Sync.upload(event)
                if not res:
                    self.syncQueue.put(event)
                time.sleep(5)
            else:
                logging.debug('in changeing: '+event)
                needSleep = False
                if self.syncQueue.empty():
                    logging.debug('needsleep')
                    needSleep = True
                self.syncQueue.put(event)
                logging.debug('skeep..')
                if needSleep:
                    logging.debug('sleep '+self.sleeptime)
                    time.sleep(float(self.sleeptime))
