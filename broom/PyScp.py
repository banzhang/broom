#!/user/bin/env python
# -*- coding: utf-8 -*-

'scp from application server to log server'
           
__author__ = 'houweizong@gmail.com'
          
import logging,sys,time,logging.handlers
import pexpect


SSH_NEWKEY = '(?i)are you sure you want to continue connecting'
SSH_PASSWORD = "[pP]assword:"
SCP = 'scp %s %s %s@%s:%s' #scp option localpath user@hostname:/path
SCP_OPTION = ' -l 40960 -C '

'''配置日志'''
logging.basicConfig(level=logging.DEBUG)

'''构建 scp命令'''
def buildScp(user, hostname, path, local, option=' '):
    SCP = 'scp %s %s %s@%s:%s' #scp option localpath user@hostname:/path
    res = SCP%(option, local, user, hostname, path)
    logging.debug(res)
    return res

'''执行文件拷贝'''
def doScp(cmd, pd):
    try:
        worker = pexpect.spawn(cmd)
        worker.logfile = sys.stdout
        i = worker.expect([pexpect.TIMEOUT, SSH_NEWKEY, '(?i)password'], 120)
        if i == 0:
            logging.debug('ERROR! could not login with SSH. Here is what SSH said:')
            logging.debug(worker.before)
            logging.debug(worker.after)
            sys.exit (1)
        if i == 1:
            logging.debug('new server add to knowhosts!')
            worker.sendline('yes')
            k = worker.expect([SSH_PASSWORD])
            worker.sendline(pd)
            e = worker.expect('100%', 2400)
            if e == 0:
                logging.debug('DONE! Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
            j =  worker.expect([pexpect.TIMEOUT, pexpect.EOF])
            if j == 0:
                logging.debug('ERROR! Timeout. Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
            elif j == 1:
                logging.debug('DONE! Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
            else:
                logging.debug('UNEXPECT!  Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
        if i == 2:
            worker.sendline(pd)
            e = worker.expect('100%', 2400)
            if e == 0:
                logging.debug('DONE! Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
                
            j =  worker.expect([pexpect.TIMEOUT, pexpect.EOF])
            if j == 0:
                logging.debug('ERROR! Timeout. Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
            elif j == 1:
                logging.debug('DONE! Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
            else:
                logging.debug('UNEXPECT!  Here is what SSH said:')
                logging.debug(worker.before)
                logging.debug(worker.after)
        return True
    except Exception, e:
        logging.exception(e)
        return False
        

if __name__ == '__main__':
    try:
        server='192.168.23.131'
        me='192.168.23.129'
        port=9999
        user='root'
        pwd='12345678'
        path='/tmp/'
        local='/tmp/f0/f0'
        cmd = buildScp(user, server, path, local)
        doScp(cmd, pwd)
    except SystemExit, e:
        logging.debug('endTime come!')
        logging.exception(e)
    except KeyboardInterrupt, e:
        logging.debug('exit by ctrl+c!')
        logging.exception(e)
    except Exception, e:
        logging.debug('unknow!')
        logging.exception(e)
