#!/usr/bin/env python
# -*- coding:utf-8 -*-

def intval(s):
    c=[]
    for i in s:
        asc = ord(i)
        if asc>47 and asc<58:
           c.append(i)
        else:
           break
    if len(c)>0:
        return int(''.join(c))
    else:
        return 0

def reverseStr(s):
    c = [i for i in s]
    c.reverse()
    e = ''.join(c)
    return e

if __name__ == '__main__':
    a='request1231234123'
    b = reverseStr(a)
    print b
    c = intval(b)
    print c
    e = reverseStr(str(c))
    print e
