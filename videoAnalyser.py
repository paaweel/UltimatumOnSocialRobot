import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from tensorflow.keras.models import model_from_json
import zmq
from PIL import Image
import numpy as np


def rgb2gray(img):
    rgb_weights = [0.2989, 0.5870, 0.1140]
    return np.dot(img[...,:3], rgb_weights)

class VideoAnalyser:
    def __init__(self, videoPath):
        self.videoPath = videoPath
        zmqSocket = "tcp://127.0.0.1:5559"
        # logging.debug('Opening PUSH ZMQ communication on '
        #     + zmqSocket
        #     + ' for video emotion labels')
        self.context = zmq.Context()
        self.videoEmotionsSocket = self.context.socket(zmq.PUSH)
        self.videoEmotionsSocket.bind(zmqSocket)

        AI_MODELS_DIR = os.path.join(os.getcwd(), 'AI_models/video')
        # takes ~0.52s
        with open(os.path.join(AI_MODELS_DIR, 'best.json'), 'r') as json_file:
            txt_model = json_file.read()
            self.model = model_from_json(txt_model)
            self.model.load_weights(os.path.join(AI_MODELS_DIR, 'best.hdf5'))


    def analyse(self, path):
        im = Image.open(path)
        arrIm = np.array(im)
        croppedBinVersor = np.expand_dims(np.expand_dims(rgb2gray(arrIm), 2), 0)
        predictions = self.model.predict(np.asarray(croppedBinVersor))
        predictedEmotion = np.argmax(predictions)
        # self.videoEmotionsSocket.send(predictions)
        logging.debug('VIDEO {0}: {1} -> {2}'.format(path, predictedEmotion, predictions))


if __name__ == "__main__":
    # db = DbConnector()
    logging.basicConfig(filename='videoModule.log',level=logging.DEBUG)
    if len(sys.argv) != 2:
        logging.debug('Incorrect number of arguments, required 1 with'\
        'audio file path')
        sys.exit(5)
    videoClassifier = VideoAnalyser(str(sys.argv[1]))
    videoClassifier.analyse(videoClassifier.videoPath)
