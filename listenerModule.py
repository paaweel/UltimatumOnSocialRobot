import io
import re
import sys
from threading import currentThread, Thread
import qi
import time
from helperModule import *

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.protobuf.json_format import MessageToJson

import collections
import zmq
import zlib, cPickle as pickle
import json

from audioSessionManager import AudioSessionManager
RATE = 16000
from datetime import datetime, timedelta
from io import StringIO


def send_zipped_pickle(socket, obj, flags=0, protocol=-1):
    """pickle an object, and zip the pickle before sending it"""
    p = pickle.dumps(obj, protocol)
    z = zlib.compress(p)
    return socket.send(z, flags=flags)

def recv_zipped_pickle(socket, flags=0, protocol=-1):
    """inverse of send_zipped_pickle"""
    z = socket.recv(flags)
    p = zlib.decompress(z)
    return pickle.loads(p)

class ListenerModule(object):

    def __init__(self, session):
        self.language_code = 'pl-PL'
        self.session = session
        self.context = zmq.Context()
        self.audio_socket = self.context.socket(zmq.PUSH)
        self.audio_socket.bind("tcp://127.0.0.1:5558")

    def run(self, timeout=1):
        try:
            while True:
                for i in range(timeout*10):
                    with AudioSessionManager(self.session, timeout*10) as stream:
                        content = [content.tobytes() for content in stream.data()]
                p = pickle.dumps(content, -1)
                z = zlib.compress(p)
                self.audio_socket.send(z, flags=0)
        except KeyboardInterrupt:
            print("Exit signal was sent.")


if __name__ == '__main__':
    session = qi.Session()
    ip = '192.168.0.28'
    port = '9559'
    try:
        session.connect("tcp://" + ip + ":" + port)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + port + ".\n"
                                                                               "Please check your script arguments. "
                                                                               "Run with -h option for help.")
        sys.exit(1)
    listener = ListenerModule(session)
    audio = listener.run()
    print(audio)
