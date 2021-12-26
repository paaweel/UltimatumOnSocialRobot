#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from dialogTopic import load_topic
from eventsModule import runEventListener
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


if __name__ == "__main__":

    topicThread = Thread(target=load_topic)
    eventThread = Thread(target=runEventListener)
    start(topicThread, eventThread)

    try:
        raw_input()
        print("Shutting down")

    except KeyboardInterrupt:
        print("Shutting down")

    topicThread.join()
    eventThread.join()
    sys.exit(0)
