import random
import numpy as np
import qi
from PIL import Image
import time
from datetime import datetime
import logging
# from dbConnector import DbConnector
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from config import Config

class VideoModule:
    def __init__(self, ip=Config().ip, port=Config().port):
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
        # logging.debug('Subscribing to a video service')
        self.resolution = 2
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
        self.videoPath = './video_files'

    def closeConnection(self):
        logging.debug('Unsubscribing video and face detection services')
        self.videoService.unsubscribe(self.client)
        self.faceDetection.unsubscribe("VideoModule")

    def onHumanTracked(self, value):
        try:
            self.faceDetection.unsubscribe("VideoModule")
        except:
            return
        if value != []:
            timestamp = datetime.now().strftime("%Y-%b-%d_%H:%M:%S.%f")
            logging.debug('Human tracked, time: ' + timestamp)
            result = self.videoService.getImageRemote(self.client)
            if result is None:
                logging.error('Cannot capture frame')
            elif result[6] is None:
                logging.error('No image data string')
            elif self.width == None or self.height == None:
                self.width = result[0]
                self.height = result[1]
                im = np.frombuffer(result[6], np.uint8).reshape(self.height, self.width, 3)
                croppedFace = self.cropFace(im, value[1])
                image = Image.fromarray(croppedFace)
                imgPath = os.path.join(self.videoPath, timestamp)
                image.save(imgPath)
                os.system('python videoAnalyser.py {0} &'.format(imgPath))
        self.faceDetection.subscribe("VideoModule")


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
        return np.array(faceImg.resize((96, 96), Image.BILINEAR))


if __name__ == "__main__":
    # db = DbConnector()
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
