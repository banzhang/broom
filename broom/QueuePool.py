#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue
import Logger

QueuePool = {}
logger = Logger.getInstance()

def getQueue(name):
    global QueuePool
    logger.debug(QueuePool)
    if not QueuePool.get(name):
        logger.info(name+'new')
        logger.debug(QueuePool.get(name))
        QueuePool[name] = Queue.Queue()

    logger.info(name+'old')
    return QueuePool.get(name)
