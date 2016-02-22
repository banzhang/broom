#!/usr/bin/env python
# -*- encoding:utf-8 -*-

#Basic inetd server - Chapter 3 - inetdserver.py
import sys,struct,socket,traceback,json,os,md5

__author__ = "houweizong@gmail.com"

CHECKDIR = 0x0004
CHECKFILE = 0x0003
BASEPATH = '/tmp/log/'

class logServer:

    def __init__(self):
        pass
    
    '''服务主入口'''
    @classmethod
    def run(cla_obj):
        while 1:
            try:
                header = sys.stdin.read(6)
                header = struct.unpack("!HI", header)
                length = header[1]
                cmd = header[0]
                data = sys.stdin.read(length)
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
                sys.stdout.write(bindata)
                sys.stdout.flush()
            except Exception as e:
                 #info = sys.exc_info()
                #print info
                #for file, lineno, function, text in traceback.extract_tb(info[2]):
                #   print file, "line:", lineno, "in", function
                #   print text
            
                #print "** %s: %s" % info[:2]
   
                print type(e)
                print str(e)
    
    @classmethod
    def debug(cla_obj, host, port):
        import pdb
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        print 'Connected by', addr
        while 1:
            header = conn.recv(6)
            if header:
                header = struct.unpack("!HI", header)
                length = header[1]
                cmd = header[0]
                data = conn.recv(length)
                if not data:
                    break
                if cmd == CHECKDIR:
                    cla_obj.checkDir(data)
                conn.sendall(data)
                exit()
            else:
                print header

        conn.close()

    '''检测目录是否存在'''
    @classmethod
    def checkDir(cla_obj,data):
        client = socket.fromfd(0, socket.AF_INET, socket.SOCK_STREAM)
        d = client.getpeername()
        data = json.loads(data)
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
        data = json.loads(data)
        path = data.get("path")
        path = BASEPATH+d[0]+path
        hashCode = data.get('hashcode')
        if  os.path.isfile(path):
            try:
                h = md5.GetFileMd5(path)
                if h == hashCode:
                    return True
                else:
                    return False
            except Exception as e:
                return False
        else:
            return False
        return True

logServer.run()
