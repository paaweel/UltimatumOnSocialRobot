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

import time

class VideoWrapper:
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
        self.colorSpace = 0
        self.fps = 20
        self.captureFrames = False
        self.client = None
        self.process = Process(target=self.capture)
        self.thread = None
        self.lastFrames = deque([], maxlen=10)

    def startThread(self):
        self.captureFrames = True
        self.thread = Thread(target=self.capture)
        self.thread.daemon = True
        self.thread.start()

    def stopThread(self):
        self.captureFrames = False
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
            im = np.frombuffer(result[6], np.uint8).reshape((height, width, 1))
            self.lastFrames.append(im)

            while self.captureFrames:
                result = self.video_service.getImageRemote(self.client)
                if result is None:
                    print 'cannot capture.'
                elif result[6] is None:
                    print 'no image data string.'
                else:
                    im = np.frombuffer(result[6], np.uint8).reshape(height, width)
                    self.lastFrames.append(im)

                    # im.show()
                    print(len(result[6]))

                    # mode = "RGBA"

                    # data = StringIO.StringIO(im)
                    # img = Image.open(data)
                    # print(im)

                    # img = Image.frombytes(im, "RGB")
                    # d =  np.array(array.array("", result[6])).reshape(height, width)
                    plt.imshow(im)
                    plt.show()

                    # img.show()

        self.video_service.unsubscribe(self.client)

    def getLastFrames(self, n=10):
        # it's faster to index a list than a deque collection
        arr = list(self.lastFrames)[0+(10-n):n]
        lists = []
        for frame in arr:
            lists.append(frame.tolist())
        json_frames = json.dumps(lists)
        with open('data' + str(random.randint(0, 4000)) + '.json', 'w') as f:
            json.dump(json_frames, f)

        return json_frames


if __name__ == "__main__":

    print("Starting video service!")

    videoWrapper = VideoWrapper()

    videoWrapper.startThread()

    time.sleep(5)

    frames = videoWrapper.getLastFrames()

    # print(frames)


    # img = Image.fromarray(frames, "RGB")
    # img.save("testImage.png")
    # img.show()

    print("Closing video service")

    videoWrapper.stopThread()
    print("Video service finished!")
