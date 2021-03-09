#!/usr/bin/env python
#-*- coding: utf-8 -*-

import qi
from concurrent.futures import ThreadPoolExecutor, Future
import sys
from listenerModule import ListenerModule
import time
from multiprocessing import Process
import zmq
import random
import zlib, cPickle as pickle
import json
from helperModule import *
from matplotlib import pyplot as plt
from game import UltimatumGame


def receiveTranscript():
    try:
        context = zmq.Context()
        transcript_receiver = context.socket(zmq.PULL)
        transcript_receiver.setsockopt(zmq.CONFLATE, 1)
        transcript_receiver.connect("tcp://127.0.0.1:5557")
        while True:
            print("getting transcript")
            transcript = transcript_receiver.recv_string()
            # NOTE
            # hello = "cześć".decode('utf8') # all commands must be decoded
            print(transcript)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

def receiveAudio():
    try:
        context = zmq.Context()
        audio_receiver = context.socket(zmq.PULL)
        audio_receiver.setsockopt(zmq.CONFLATE, 1)
        audio_receiver.connect("tcp://127.0.0.1:5558")
        while True:
            print("getting audio")
            z = audio_receiver.recv(0)
            p = zlib.decompress(z)
            audio = pickle.loads(p)
            print("got audio")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

def receiveVideo():
    try:
        context = zmq.Context()
        video_receiver = context.socket(zmq.PULL)
        video_receiver.setsockopt(zmq.CONFLATE, 1)
        video_receiver.connect("tcp://127.0.0.1:5559")
        while True:
            print("receiving video")
            image_bytes = video_receiver.recv(0)
            seqImages = np.frombuffer(image_bytes, dtype='uint8').reshape((3, 480, 640, 3))
            gray = rgb2gray(seqImages[0])
            plt.imshow(gray, cmap='gray')
            plt.show()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

if __name__ == '__main__':
    game = UltimatumGame()
    game.run()
