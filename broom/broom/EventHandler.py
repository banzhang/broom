#!/usr/bin/env python

import pyinotify,Queue,logging


class EventHandler(pyinotify.ProcessEvent): 
   def __init__(self, events_queue): 
     super(EventHandler,self).__init__() 
     self.events_queue = events_queue 
   def my_init(self): 
     pass
   def process_IN_CREATE(self,event):
     logging.debug(event)
     if not event.dir:
        self.events_queue.put(event.pathname)
