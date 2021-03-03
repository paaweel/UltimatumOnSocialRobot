import json
import random

import numpy as np
import qi
from multiprocessing import Process
from threading import Thread
from collections import deque
from PIL import Image
import StringIO
import array

from matplotlib import pyplot as plt

import collections
import zmq
import time
from helperModule import *


class VideoModule:
    def __init__(self, ip="192.168.0.28", port="9559", language="English"):
        # type: (str, str, str) -> None
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + ip + ":" + port)
            self.video_service = self.session.service("ALVideoDevice")
            print("Robot connected to VIDEO module.")
        except RuntimeError:
            print("Can't connect to Pepper at ip \""
                  + ip + "\" on port " + port + ".\n"
                  + "Please check your script arguments. "
                  + "Run with -h option for help.")
        self.resolution = 2
        # 0: 0.30, 1, 6, 8: 0.45, 2: 0.6, 7: 0.40, 5: 0.40
        self.colorSpace = 11
        self.fps = 20
        self.captureFrames = False
        self.client = None
        self.process = Process(target=self.capture)
        self.thread = None
        self.context = zmq.Context()
        self.video_socket = self.context.socket(zmq.PUSH)
        self.video_socket.bind("tcp://127.0.0.1:5559")
        self.seqFrames = deque([], maxlen=3)

    def startThread(self):
        self.captureFrames = True
        self.thread = Thread(target=self.capture)
        self.thread.daemon = True
        self.thread.start()

    def stopThread(self):
        self.captureFrames = False
        time.sleep(0.5)
        self.thread.join()

    def capture(self):
        print 'getting images in remote'
        self.client = self.video_service.subscribeCamera(
            "python_video" + str(random.random()),
            0,
            self.resolution,
            self.colorSpace,
            self.fps)

        result = self.video_service.getImageRemote(self.client)
        if result is None:
            print 'cannot capture.'
        elif result[6] is None:
            print 'no image data string.'
        else:
            width = result[0]
            height = result[1]

            while self.captureFrames:
                result = self.video_service.getImageRemote(self.client)
                if result is None:
                    print 'cannot capture.'
                elif result[6] is None:
                    print 'no image data string.'
                else:
                    im = np.frombuffer(result[6], np.uint8).reshape(height, width, 3)
                    self.seqFrames.append(im)
                    sentBuffor = np.array(self.seqFrames)
                    if sentBuffor.shape[0] == 3:
                        self.video_socket.send(sentBuffor)
                        print("sent")
        self.video_service.unsubscribe(self.client)

    def getLastFrames(self, video_receiver):
        frames = []
        for i in range(1):
            image_bytes = video_receiver.recv()
            seqImages = np.frombuffer(image_bytes, dtype='uint8').reshape((3, 480, 640, 3))
            frames.append(seqImages)
        return frames


if __name__ == "__main__":
    print("Starting video service!")
    camera = VideoModule()
    camera.startThread()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

    camera.stopThread()
    print("Video service finished!")
