#!/user/bin/env python
# -*- coding: utf-8 -*-

'scp from application server to log server'
           
__author__ = 'houweizong@gmail.com'
          
import logging,sys,time,logging.handlers
import pexpect
import Config
import Logger


SSH_NEWKEY = '(?i)are you sure you want to continue connecting'
SSH_PASSWORD = "[pP]assword:"
SCP = 'scp %s %s %s@%s:%s' #scp option localpath user@hostname:/path
SCP_OPTION = ' -l 40960 -C '

logger = Logger.getInstance()

'''构建 scp命令'''
def buildScp(user, hostname, path, local, option=' '):
    SCP = 'scp %s %s %s@%s:%s' #scp option localpath user@hostname:/path
    res = SCP%(option, local, user, hostname, path)
    logger.debug(res)
    return res

'''执行文件拷贝'''
def doScp(cmd, pd):
    try:
        logger.debug(cmd)
        logger.debug(pd)
        worker = pexpect.spawn(cmd)
        worker.logfile = sys.stdout
        i = worker.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password'], 120)
        logger.debug(i)
        if i == 0:
            logger.debug('ERROR! could not login with SSH. Here is what SSH said:')
            logger.debug(worker.before)
            logger.debug(worker.after)
            sys.exit (1)
        if i == 1:
            logger.debug('new server add to knowhosts!')
            worker.sendline('yes')
            k = worker.expect([SSH_PASSWORD])
            worker.sendline(pd)
            e = worker.expect('100%', 2400)
            if e == 0:
                logger.debug('DONE! Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
            j =  worker.expect([pexpect.exceptions.TIMEOUT, pexpect.exceptions.EOF])
            if j == 0:
                logger.debug('ERROR! Timeout. Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
            elif j == 1:
                logger.debug('DONE! Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
            else:
                logger.debug('UNEXPECT!  Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
        if i == 2:
            worker.sendline(pd)
            e = worker.expect('100%', 2400)
            if e == 0:
                logger.debug('DONE! Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
                
            j =  worker.expect([pexpect.TIMEOUT, pexpect.EOF])
            if j == 0:
                logger.debug('ERROR! Timeout. Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
            elif j == 1:
                logger.debug('DONE! Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
            else:
                logger.debug('UNEXPECT!  Here is what SSH said:')
                logger.debug(worker.before)
                logger.debug(worker.after)
        return True
    except Exception, e:
        logger.exception(e)
        return False
        

if __name__ == '__main__':
    try:
        server='192.168.23.131'
        me='192.168.23.129'
        port=9999
        user='root'
        pwd='12345678'
        path='/tmp/'
        local='/var/log/ygtoo/request/2016/post20160121'
        cmd = buildScp(user, server, path, local)
        doScp(cmd, pwd)
    except SystemExit, e:
        logger.debug('endTime come!')
        logger.exception(e)
    except KeyboardInterrupt, e:
        logger.debug('exit by ctrl+c!')
        logger.exception(e)
    except Exception, e:
        logger.debug('unknow!')
        logger.exception(e)
