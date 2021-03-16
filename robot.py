#!/usr/bin/env python
#-*- coding: utf-8 -*-

import qi
from concurrent.futures import ThreadPoolExecutor, Future
import sys
from listenerModule import ListenerModule
ListenerModule
import time
from multiprocessing import Process
import zmq
import zlib, cPickle as pickle
import numpy as np
from speakerModule import SpeakerModule
from helperModule import *

class Robot:
    def __init__(self):
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

        self.speaker = SpeakerModule()

        context = zmq.Context()
        self.transcript_receiver = context.socket(zmq.PULL)
        self.transcript_receiver.setsockopt(zmq.CONFLATE, 1)
        self.transcript_receiver.connect("tcp://127.0.0.1:5557")

        self.audioProc = Process(target=self.receiveAudio)
        self.videoProc = Process(target=self.receiveVideo)

        self.transcriptData = None
        self.audioData = None
        self.videoData = None

    def say(self, text):
        self.speaker.say(text)

    def receiveTranscript(self):
        z = self.transcript_receiver.recv(0)
        p = zlib.decompress(z)
        return pickle.loads(p)

    def receiveAudio(self):
        try:
            context = zmq.Context()
            audio_receiver = context.socket(zmq.PULL)
            audio_receiver.setsockopt(zmq.CONFLATE, 1)
            audio_receiver.connect("tcp://127.0.0.1:5558")
            while True:
                z = audio_receiver.recv(0)
                p = zlib.decompress(z)
                audio = pickle.loads(p)
                self.audioData = audio
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Exit signal was sent.")

    def receiveVideo(self):
        try:
            context = zmq.Context()
            video_receiver = context.socket(zmq.PULL)
            video_receiver.setsockopt(zmq.CONFLATE, 1)
            video_receiver.connect("tcp://127.0.0.1:5559")
            while True:
                image_bytes = video_receiver.recv(0)
                seqImages = np.frombuffer(image_bytes, dtype='uint8').reshape((3, 480, 640, 3))
                gray = rgb2gray(seqImages[0])
                self.videoData = gray
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Exit signal was sent.")

    def start(self):
        self.audioProc.start()
        self.videoProc.start()
        print("Opened connection to robot sensors.")

    def stop(self):
        self.audioProc.join()
        self.videoProc.join()
        print("Closed connection to robot sensors.")
