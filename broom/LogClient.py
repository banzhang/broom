#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging,Config,os,socket,struct,json,Md5,sys,traceback
import Logger

CHECKDIR = 0x0004
CHECKFILE = 0x0003

logger = Logger.getInstance()

class LogClient:

    __conn = False
    __socket = False

    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def getConn(self):
        if not self.__conn:
            self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.__conn.connect((self.host, self.port))
        return self.__conn
 
    def closeConn(self, conn):
        try:
            self.__conn = False
            conn.close()
        except Exception as e:
            logger.exception(e)
 
    def checkDir(self, path):
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        try:
            conn = self.getConn()
            logger.debug(conn)
            packet = bytearray()
            cmd = CHECKDIR
            content = {"path":path}
            content = json.dumps(content)
            clen = len(content)
            packet.extend(struct.pack("!H", cmd))
            packet.extend(struct.pack("!I", clen))
            packet.extend(struct.pack('!'+str(clen)+'s', content))
            conn.sendall(packet)
            header = conn.recv(6)
            logger.debug('readheader'+header)
            header = struct.unpack('!HI', header)
            logger.debug('unpack+'+json.dumps(header))
            clen = header[1]
            content = conn.recv(clen)
            logger.debug('readcontent'+content)
            content = struct.unpack('!'+str(clen)+'s', content)
            logger.debug('unpack+'+json.dumps(content))
            content = content[0]
            data = json.loads(content)
            res = data.get('res')
            #self.closeConn(conn)
            return res
        except socket.error, e:
            info = sys.exc_info()
            logger.error(traceback.extract_tb(info[2]))
            logger.error(info)
            logger.error(str(type(e)))
            logger.exception(e)
            self.closeConn(conn)
        except Exception as e:
            info = sys.exc_info()
            logger.error(traceback.extract_tb(info[2]))
            logger.error(info)
            logger.error(str(type(e)))
            logger.exception(e)
            self.closeConn(conn)
            return False

    def checkFile(self, path):
        if os.path.isfile(path):
            try:
                hashcode = Md5.GetFileMd5(path)
                conn = self.getConn()
                logger.debug(conn)
                packet = bytearray()
                cmd = CHECKFILE
                content = {"path":path, "hashcode":hashcode}
                content = json.dumps(content)
                clen = len(content)
                packet.extend(struct.pack("!H", cmd))
                packet.extend(struct.pack("!I", clen))
                packet.extend(struct.pack('!'+str(clen)+'s', content))
                logger.debug('send'+packet)
                conn.sendall(packet)
                header = conn.recv(6)
                logger.debug('readheader:'+header)
                header = struct.unpack('!HI', header)
                logger.debug('unpack+'+json.dumps(header))
                clen = header[1]
                content = conn.recv(clen)
                logger.debug('readcontent+'+content)
                content = struct.unpack('!'+str(clen)+'s', content)
                logger.debug('unpack+'+json.dumps(content))
                content = content[0]
                data = json.loads(content)
                res = data.get('res')
                #self.closeConn(conn)
                return res
            except socket.error, e:
                info = sys.exc_info()
                logger.error(traceback.extract_tb(info[2]))
                logger.error(info)
                logger.error(str(type(e)))
                logger.exception(e)
                self.closeConn(conn)
            except Exception as e:
                info = sys.exc_info()
                logger.error(traceback.extract_tb(info[2]))
                logger.error(info)
                logger.error(str(type(e)))
                logger.exception(e)
                self.closeConn(conn)
                return False
        else:
           return True
if __name__ == '__main__':
    s=LogClient('192.168.23.131', 9999)
    s.checkFile('/tmp/f0/f0')
