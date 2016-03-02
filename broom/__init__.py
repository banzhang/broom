#!/usr/bin/env python

from Broom import Broom
from Broomd import Broomd
import setproctitle

def main():
    setproctitle.setproctitle('broom')
    Broom.run()

def server():
    setprocetitle.setproctitle('broomd')
    Broomd.run()
