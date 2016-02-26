#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue

QueuePool = {}

def getQueue(name):
    global QueuePool
    if not QueuePool.get(name):
        QueuePool[name] = Queue.Queue()

    return QueuePool.get(name)
