#!/usr/bin/env python
# -*- coding:utf-8 -*-

import queue.queue

QueuePool = {}

def getQueue(name):
    global QueuePool
    if not QueuePool.get(name):
        QueuePool[name] = Queue.Queue()

    return Queue.Pool.get(name)
