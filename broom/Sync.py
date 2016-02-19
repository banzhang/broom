#!/usr/bin/env python

import logging,pyinotify,Queue,threading,time,os
import PyScp
from LogClient import LogClient
import Config

'''sync the file'''
class Sync:
    def __init__(self):
        pass

    @classmethod 
    def upload(cla, path, rtry=0):
        logging.debug('upload start: %s'%path)
        config = Config.getInstance()
        scpuser = config.get('client', 'scpuser')
        scppwd =  config.get('client', 'scppwd')
        scprtry =  config.get('client', 'scprtry')
        scpconf =  config.get('client', 'scpconf')
        logServer = config.get('client', 'sip')
        port = config.get('client', 'sport')
        client = LogClient(logServer, port)
        basepath = client.checkDir(path)
        logging.debug(basepath)
        if not basepath:
            return False
        cmd = PyScp.buildScp(scpuser, logServer, basepath+path, path, scpconf)
        PyScp.doScp(cmd, scppwd)
        res = client.checkFile(path)
        if not res and rtry<scprtry:
            rtry = rtry+1
            logging.debug('upload end: %s, %s, rtry %s'%(path, 'fail', rtry))
            return cla.upload(path, rtry)
        elif res:
            os.remove(path)
            logging.debug('upload end: %s, %s, delete %s'%(path, 'succ', path))
            return True
        elif not res and retry>=5:
            logging.debug('upload end: %s, %s'%(path, 'fail'))
            return False

    @classmethod
    def needSync(cla, path, noChangeTime=3600):
        stat = os.stat(path)
        if stat.st_mtime+noChangeTime <= time.time():
            return True

        return False
