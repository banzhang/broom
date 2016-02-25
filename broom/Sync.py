#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging,pyinotify,Queue,threading,time,os
import PyScp
from LogClient import LogClient
import Config
from Util import *
import Logger

logger = Logger.getInstance()

'''sync the file'''
class Sync:
    def __init__(self):
        pass

    @classmethod 
    def upload(cla, path, rtry=0):
        logger.debug('upload start: %s'%path)
        config = Config.getInstance()
        scpuser = config.get('client', 'scpuser')
        scppwd =  config.get('client', 'scppwd')
        scprtry =  config.get('client', 'scprtry')
        scpconf =  config.get('client', 'scpconf')
        logServer = config.get('client', 'sip')
        port = config.get('client', 'sport')
        client = LogClient(logServer, port)
        basepath = client.checkDir(path)
        logger.debug(basepath)
        if not basepath:
            return False
        cmd = PyScp.buildScp(scpuser, logServer, basepath+path, path, scpconf)
        PyScp.doScp(cmd, scppwd)
        res = client.checkFile(path)
        if not res and rtry<scprtry:
            rtry = rtry+1
            logger.debug('upload end: %s, %s, rtry %s'%(path, 'fail', rtry))
            return cla.upload(path, rtry)
        elif res:
            os.remove(path)
            logger.debug('upload end: %s, %s, delete %s'%(path, 'succ', path))
            return True
        elif not res and retry>=5:
            logger.debug('upload end: %s, %s'%(path, 'fail'))
            return False

    @classmethod
    def needSync(cla, path, noChangeTime=3600):
        name = os.path.basename(path)
        cTimeFlag = reverseStr(name)
        cTimeFlag = intval(cTimeFlag)
        cTimeFlag = reverseStr(str(cTimeFlag))
        timeStamp = time.time()
        localTime = time.localtime(timeStamp)
        timeFlagDay = time.strftime("%Y%m%d", localTime)
        timeFlagHour = time.strftime("%Y%m%d%H", localTime)
        if len(cTimeFlag) == len(timeFlagDay):
            if cTimeFlag == timeFlagDay:
                return False
        elif len(cTimeFlag) == len(timeFlagHour):
            if cTimeFlag == timeFlagHour:
                return False

        stat = os.stat(path)
        if stat.st_mtime+noChangeTime <= time.time():
            return True

        return False

if __name__ == '__main__':
    logger.debug(Sync.needSync('/tmp/fs2016022301', 60))
    logger.debug(Sync.needSync('/tmp/fs20160223', 60))
