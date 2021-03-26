#!/usr/bin/env python
#-*- coding: utf-8 -*-

from threading import Thread
from dialogTopic import runTopic
from eventController import runEventListener
import time
import sys

def start(topicThread, eventThread):
    topicThread.daemon = True
    topicThread.start()
    eventThread.daemon = True
    eventThread.start()

def stop(topicThread, eventThread):
    topicThread.join()
    eventThread.join()

if __name__ == '__main__':
    topicThread = Thread(target=runTopic)
    eventThread = Thread(target=runEventListener)
    start(topicThread, eventThread)
    try:
        raw_input()
        print "Shutting down"
    except KeyboardInterrupt:
        print "Shutting down"
    sys.exit(0)
