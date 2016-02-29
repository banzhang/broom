#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pyinotify,Queue,logging,Config
import Logger

logger = Logger.getInstance()

class EventHandler(pyinotify.ProcessEvent): 
   def __init__(self, events_queue): 
     super(EventHandler,self).__init__() 
     self.events_queue = events_queue 
   def my_init(self): 
     pass
   def process_IN_CREATE(self,event):
     logger.debug(event)
     if not event.dir:
        self.events_queue.put(event.pathname)

   def process_IN_MOVED_TO(self, event):
     logger.debug(event)
     if not event.dir:
        self.events_queue.put(event.pathname)
    
