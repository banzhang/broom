#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import logging,os,socket,struct,json,Md5,sys,traceback

CHECKDIR = 0x0004
CHECKFILE = 0x0003

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
            logging.exception(e)
 
    def checkDir(self, path):
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        try:
            conn = self.getConn()
            logging.debug(conn)
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
            logging.debug('readheader'+header)
            header = struct.unpack('!HI', header)
            logging.debug('unpack+'+json.dumps(header))
            clen = header[1]
            content = conn.recv(clen)
            logging.debug('readcontent'+content)
            content = struct.unpack('!'+str(clen)+'s', content)
            logging.debug('unpack+'+json.dumps(content))
            content = content[0]
            data = json.loads(content)
            res = data.get('res')
            #self.closeConn(conn)
            return res
        except socket.error, e:
            info = sys.exc_info()
            logging.error(traceback.extract_tb(info[2]))
            logging.error(info)
            logging.error(str(type(e)))
            logging.exception(e)
            self.closeConn(conn)
        except Exception as e:
            info = sys.exc_info()
            logging.error(traceback.extract_tb(info[2]))
            logging.error(info)
            logging.error(str(type(e)))
            logging.exception(e)
            self.closeConn(conn)
            return False

    def checkFile(self, path):
        if os.path.isfile(path):
            try:
                hashcode = Md5.GetFileMd5(path)
                conn = self.getConn()
                logging.debug(conn)
                packet = bytearray()
                cmd = CHECKFILE
                content = {"path":path, "hashcode":hashcode}
                content = json.dumps(content)
                clen = len(content)
                packet.extend(struct.pack("!H", cmd))
                packet.extend(struct.pack("!I", clen))
                packet.extend(struct.pack('!'+str(clen)+'s', content))
                logging.debug('send'+packet)
                conn.sendall(packet)
                header = conn.recv(6)
                logging.debug('readheader:'+header)
                header = struct.unpack('!HI', header)
                logging.debug('unpack+'+json.dumps(header))
                clen = header[1]
                content = conn.recv(clen)
                logging.debug('readcontent+'+content)
                content = struct.unpack('!'+str(clen)+'s', content)
                logging.debug('unpack+'+json.dumps(content))
                content = content[0]
                data = json.loads(content)
                res = data.get('res')
                #self.closeConn(conn)
                return res
            except socket.error, e:
                info = sys.exc_info()
                logging.error(traceback.extract_tb(info[2]))
                logging.error(info)
                logging.error(str(type(e)))
                logging.exception(e)
                self.closeConn(conn)
            except Exception as e:
                info = sys.exc_info()
                logging.error(traceback.extract_tb(info[2]))
                logging.error(info)
                logging.error(str(type(e)))
                logging.exception(e)
                self.closeConn(conn)
                return False
        else:
           return True
if __name__ == '__main__':
    s=LogClient('192.168.23.131', 9999)
    s.checkFile('/tmp/f0/f0')
