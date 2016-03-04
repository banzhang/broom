#!/usr/bin/env python
# -*- coding:utf-8 -*-

 
import hashlib
import os,sys
import time,Logger

logger = Logger.getInstance()

def GetStrMd5(src):
    m0=hashlib.md5()
    m0.update(src)
    pass
 
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    
    f = file(filename,'rb')
    i = 0
    while True:
        i = i+1
        b = f.read(4096)
        size = i*4096
        if i>0 and (size%2621440) == 0:
            logger.info(filename+',read:'+str(size/1048576)+'Mbytes')
            time.sleep(1)
        
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
 
def CalcSha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash
 
def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash        
 
if __name__ == "__main__":
    if len(sys.argv)==2 :
        hashfile = sys.argv[1]
        if not os.path.exists(hashfile):
            hashfile = os.path.join(os.path.dirname(__file__),hashfile)
            if not os.path.exists(hashfile):
                print("cannot found file")
            else:
                CalcMD5(hashfile)
        else:
            CalcMD5(hashfile)
            #raw_input("pause")
    else:
        print("no filename")
