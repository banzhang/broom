#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,ConfigParser,argparse

config=False
def getInstance():
    global config
    if not config:
        parser = argparse.ArgumentParser(description='broom user help')
        parser.add_argument('-c',required=True, default='/etc/broom.conf',help='the config file for client and server')
        args = parser.parse_args()
        file = args.c
        if os.path.isfile(file):
            config = ConfigParser.ConfigParser()
            config.readfp(open(file))
            return config
        else:
            raise Exception('file not exists or can not read!')
    
    return config
