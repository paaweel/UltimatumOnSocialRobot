import random
import numpy as np
import qi
from PIL import Image
import array
from collections import deque
import zmq
import time
import logging
from dbConnector import DbConnector
import os
from helperModule import *


class VideoModule:
    def __init__(self, ip="192.168.0.28", port="9559"):
        # type: (str, str, str) -> None
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + ip + ":" + port)
            logging.debug('Connecting robot to ALVideoDevice service')
            self.videoService = self.session.service("ALVideoDevice")

            logging.debug('Connecting robot to ALMemory service')
            self.memoryService = self.session.service("ALMemory")

            logging.debug('Connecting robot to ALFaceDetection service')
            self.faceDetection = self.session.service("ALFaceDetection")
        except RuntimeError:
            logging.error("Can't connect to Pepper at ip \""
                  + ip + "\" on port " + port + ".\n"
                  + "Please check your script arguments. "
                  + "Run with -h option for help.")
        logging.debug('Subscribing to a video service')
        self.resolution = 2
        # 0: 0.30, 1, 6, 8: 0.45, 2: 0.6, 7: 0.40, 5: 0.40
        self.colorSpace = 11
        self.fps = 20
        self.width = None
        self.height = None
        self.client = self.videoService.subscribeCamera(
            "pythonVideo" + str(random.random()),
            0,
            self.resolution,
            self.colorSpace,
            self.fps
        )

        logging.debug('Subscribing to a memory service.')
        self.subscriber = self.memoryService.subscriber("FaceDetected")
        self.subscriber.signal.connect(self.onHumanTracked)

        logging.debug('Subscribing to a face detection service')
        self.faceDetection.subscribe("VideoModule")

        # for baseline model we don't capture sequences,
        # for sequences change into framesCnt = 3
        self.framesCnt = 1
        self.seqFrames = deque([], maxlen=self.framesCnt)
        self.emotions = deque([], maxlen=10)

        zmqSocket = "tcp://127.0.0.1:5559"
        logging.debug('Opening PUSH ZMQ communication on '
                    + zmqSocket
                    + 'for facial emotion labels')
        self.context = zmq.Context()
        self.videoEmotionsSocket = self.context.socket(zmq.PUSH)
        self.videoEmotionsSocket.bind(zmqSocket)

        AI_MODELS_DIR = os.path.join(os.getcwd(), 'AI_models/video')
        logging.debug('Loading model from ' + AI_MODELS_DIR)
        with open(os.path.join(AI_MODELS_DIR, 'baseline.json'), 'r') as json_file:
           txt_model = json_file.read()
           self.model = model_from_json(txt_model)
           self.model.load_weights(os.path.join(AI_MODELS_DIR, 'best_baseline.hdf5')
           logging.debug('Model loading finished')

    def closeConnection(self):
        logging.debug('Unsubscribing video and face detection services')
        self.videoService.unsubscribe(self.client)
        self.faceDetection.unsubscribe("VideoModule")

    def onHumanTracked(self, value):
        if value == []:
        else:
            logging.debug('Human tracked, timestamp: ', value[0])
            # there's an assumption human won't move much between 3 frames
            # if frames too slow - change the cropping error tolerance in cropFace
            for i in range(self.framesCnt):
                result = self.videoService.getImageRemote(self.client)
                if result is None:
                    logging.error('Cannot capture frame')
                elif result[6] is None:
                    logging.error('No image data string')
                elif self.width == None or self.height == None:
                    self.width = result[0]
                    self.height = result[1]
                im = np.frombuffer(result[6], np.uint8)
                       .reshape(self.height, self.width, 3)
                croppedFace = cropFace(im, value[1])
                croppedBinVersor = np.expand_dims(rgb2gray(croppedFace), 2)
                self.seqFrames.append(croppedBinVersor)
            # put the 3-frame sequence into AI
            predictions = model.predict(numpy.asarray(self.seqFrames))
            predictedEmotion = np.argmax(predictions)
            self.emotions.appendleft(predictions)
            print(self.emotions[0])
            # self.videoEmotionsSocket.send(self.emotions[0])

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
    db = DbConnector()
    logging.basicConfig(filename='videoModule.log',level=logging.DEBUG)
    logging.debug('Starting video module')
    camera = VideoModule()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.debug('Got KeyboardInterrupt from the user')

    camera.closeConnection()
    logging.debug('Exitting video module')
