#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Basic inetd server
import sys,struct,socket,traceback,json,os,Md5,logging,time
import Config
import Logger

__author__ = "houweizong@gmail.com"

CHECKDIR = 0x0004
CHECKFILE = 0x0003
config = Config.getInstance()
BASEPATH = config.get('server', 'storagedir')
LOGFILE = config.get('server', 'log')
'''配置日志'''
config = Config.getInstance()
logger = Logger.getInstance()

class Broomd:

    def __init__(self):
        pass

    '''服务主入口'''
    @classmethod
    def run(cla_obj):
        while 1:
            try:
                cmd = sys.stdin.read(2)
                cla_obj.log(LOGFILE, cmd)
                if len(cmd) != 2:
                    client = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
                    d = client.getpeername()
                    cla_obj.log(LOGFILE, cmd)
                    cla_obj.log(LOGFILE, len(cmd))
                    cla_obj.log(LOGFILE, str(d))
                    time.sleep(1)
                    return
                cmd = struct.unpack("!H", cmd)
                if  (cmd[0] != CHECKDIR) and (cmd[0] != CHECKFILE):
                    cla_obj.log(LOGFILE, cmd[0])
                    return
                cla_obj.log(LOGFILE, cmd[0])
                cmd = cmd[0]
                if cmd == CHECKDIR:
                    cla_obj.log(LOGFILE, 'checkdir')
                    length = sys.stdin.read(4)
                    length = struct.unpack('!I', length)
                    length = length[0]
                    cla_obj.log(LOGFILE, str(length))
                    data = sys.stdin.read(length)
                    if len(data) != length:
                        cla_obj.log(LOGFILE, data)
                        cla_obj.log(LOGFILE, '!='+str(length))
                        return
                    cla_obj.log(LOGFILE, data)
                    data = struct.unpack("!"+str(length)+"s", data)
                    data = data[0]
                    cla_obj.log(LOGFILE, 'start checkdir')
                    res = cla_obj.checkDir(data)
                    cla_obj.log(LOGFILE, 'end checkdir')
                elif cmd == CHECKFILE:
                    cla_obj.log(LOGFILE, 'checkfile')
                    length = sys.stdin.read(4)
                    length = struct.unpack('!I', length)
                    length = length[0]
                    cla_obj.log(LOGFILE, str(length))
                    data = sys.stdin.read(length)
                    if len(data) != length:
                        cla_obj.log(LOGFILE, data)
                        cla_obj.log(LOGFILE, '!='+str(length))
                        return
                    cla_obj.log(LOGFILE, data)
                    data = struct.unpack("!"+str(length)+"s", data)
                    data = data[0]
                    cla_obj.log(LOGFILE, 'start checkdir')
                    res = cla_obj.checkFile(data)
                    cla_obj.log(LOGFILE, 'end checkdir')
                data = {'res':res}
                content = json.dumps(data)
                clen = len(content)
                bindata = bytearray()
                bindata.extend(struct.pack('!H', cmd))
                bindata.extend(struct.pack('!I', clen))
                bindata.extend(struct.pack('!'+str(clen)+'s', content))
                sys.stdout.write(bindata)
                sys.stdout.flush()
            except Exception, e:
                info = sys.exc_info()
                log = 'Exception:'
                for file, lineno, function, text in traceback.extract_tb(info[2]):
                    log =  log+file+"line:"+str(lineno)+"in"+function
                
                cla_obj.log(LOGFILE, log)
   
    @classmethod
    def log(cla, f, msg):
       try:
           with open(f, 'a+') as f:
                f.write(str(msg)+"\r\n")
       except Exception as e:
           print e 
 
    @classmethod
    def debug(cla_obj, host, port):
        import pdb
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        while 1:
            conn, addr = s.accept()
            if not conn:
                continue
            print 'Connected by', addr
            print conn
            cla_obj.conn = conn
            try:
                print 'in'
                header = conn.recv(6)
                print 'header',header
                header = struct.unpack("!HI", header)
                length = header[1]
                cmd = header[0]
                data = conn.recv(length)
                print 'data',data
                data = struct.unpack("!"+str(length)+"s", data)
                data = data[0]
                if cmd == CHECKDIR:
                    res = cla_obj.checkDir(data)
                elif cmd == CHECKFILE:
                    res = cla_obj.checkFile(data)
                data = {'res':res}
                content = json.dumps(data)
                clen = len(content)
                bindata = bytearray()
                bindata.extend(struct.pack('!H', cmd))
                bindata.extend(struct.pack('!I', clen))
                bindata.extend(struct.pack('!'+str(clen)+'s', content))
                print 'bindata',bindata
                conn.sendall(bindata)
                print 'senddata',bindata
            except Exception as e:
                info = sys.exc_info()
                logger.error("** %s: %s" % info[:2])
                logger.exception(e)
                logger.error(e.args)


    '''检测目录是否存在'''
    @classmethod
    def checkDir(cla_obj,data):
        client = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
        d = client.getpeername()
        cla_obj.log(LOGFILE, data)
        cla_obj.log(LOGFILE, str(d))
        data = json.loads(data)
        #d=('192.168.1.10',)
        path = BASEPATH+d[0]+data.get("path")
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
                return BASEPATH+d[0]
            except Exception as e:
                return False

        return BASEPATH+d[0]

    '''检查文件是否相同'''
    @classmethod
    def checkFile(cla_obj, data):
        client = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
        d = client.getpeername()
        #d=('192.168.1.10',)
        data = json.loads(data)
        path = data.get("path")
        path = BASEPATH+d[0]+path
        hashCode = data.get('hashcode')
        if  os.path.isfile(path):
            try:
                h = Md5.GetFileMd5(path)
                if h == hashCode:
                    return True
                else:
                    return False
            except Exception as e:
                return False
        else:
            return False
        return True

#logServer.run()
if __name__ == '__main__':
    Broomd.run()
