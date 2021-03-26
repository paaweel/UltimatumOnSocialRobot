import random
import numpy as np
import qi
from multiprocessing import Process
from threading import Thread
from PIL import Image
import array
from matplotlib import pyplot as plt
from collections import deque
import zmq
import time
from PIL import Image


class VideoModule:
    def __init__(self, ip="192.168.0.28", port="9559"):
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
        self.memory = self.session.service("ALMemory")
        # Connect the event callback.
        self.subscriber = self.memory.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.onHumanTracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.face_detection = self.session.service("ALFaceDetection")
        self.face_detection.subscribe("VideoModule")
        self.got_face = False
        self.width = None
        self.height = None

        self.resolution = 2
        # 0: 0.30, 1, 6, 8: 0.45, 2: 0.6, 7: 0.40, 5: 0.40
        self.colorSpace = 11
        self.fps = 20
        self.client = self.video_service.subscribeCamera(
            "python_video" + str(random.random()),
            0,
            self.resolution,
            self.colorSpace,
            self.fps
        )
        self.seqFrames = deque([], maxlen=3)
        self.emotions = deque([], maxlen=10)
        self.context = zmq.Context()
        self.videoEmotionsSocket = self.context.socket(zmq.PUSH)
        self.videoEmotionsSocket.bind("tcp://127.0.0.1:5559")

    def closeConnection(self):
        self.video_service.unsubscribe(self.client)
        self.face_detection.unsubscribe("VideoModule")

    def onHumanTracked(self, value):
        if value == []:
            print("onHumanTracked triggered but no face info")
            self.got_face = False
        else:
            print("onHumanTracked triggered", value[1])
            self.got_face = True
            # there's an assumption human won't move much between 3 frames
            # if frames too slow - change the cropping error tolerance in cropFace
            for i in range(3):
                result = self.video_service.getImageRemote(self.client)
                if result is None:
                    print 'cannot capture.'
                elif result[6] is None:
                    print 'no image data string.'
                elif self.width == None or self.height == None:
                    self.width = result[0]
                    self.height = result[1]
                im = np.frombuffer(result[6], np.uint8).reshape(self.height, self.width, 3)
                croppedFace = cropFace(im, value[1])
                self.seqFrames.append(croppedFace)
            # put the 3-frame sequence into AI
            self.emotions.appendleft(random.randrange(0, 4))
            print(self.emotions[0])
            # self.videoEmotionsSocket.send(self.emotions[0])
            self.got_face = False

    def cropFace(self, npImg, faceInfo):
        img = Image.fromarray(npImg)
        alpha = faceInfo[0][0][1]
        beta = faceInfo[0][0][2]

        # +5% error tolerance
        faceWidth = (faceInfo[0][0][3] + 0.05) * self.width
        faceHeight = (faceInfo[0][0][4] + 0.05) * self.height

        faceCenterX = int(-1*(alpha-0.5)*self.width)
        faceCenterY = int((beta+0.5)*self.height)

        faceX1 = int(faceCenterX - (faceWidth / 2))
        faceY1 = int(faceCenterY - (faceWidth / 2))
        faceX2 = int(faceCenterX + (faceWidth / 2))
        faceY2 = int(faceCenterY + (faceWidth / 2))

        faceImg = img.crop((faceX1, self.height-faceY1, faceX2, faceY2))
        return np.array(faceImg.resize((75, 75), Image.BILINEAR))


if __name__ == "__main__":
    print("Starting video service!")
    camera = VideoModule()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

    camera.closeConnection()
    print("Video service finished!")
