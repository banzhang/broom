#!/usr/bin/env python
# -*- conding:utf-8 -*-

import logging,logging.handlers,sys,time
import Config


Logger=False

levels = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}


def initLog():
    global levels
    Logger = logging.getLogger(__name__)
    config = Config.getInstance()    
    file = False
    level = False
    try:
        level = config.get('client', 'loglevel')
        file  = config.get('client', 'log')
    except:
        if not level:
            level = 'error'
 
    if levels.get(level):
        level = levels.get(level)
    else:
        level = logging.ERROR
   
    Logger.setLevel(level) 
    if not file:
        hd = logging.StreamHandler(sys.stdout)
        hd.setLevel(level)
    else:
        hd = logging.handlers.TimedRotatingFileHandler(file, 'D', 1)
        hd.suffix = "%Y%m%d"
        hd.setLevel(level)

    Logger.addHandler(hd)
    return Logger

def getInstance():
    global Logger
    if not Logger:
        Logger = initLog()

    return Logger

if __name__ == '__main__':
    lg = getInstance()
    lg.debug('test'+str(time.time()))
