import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
from tensorflow.keras.models import model_from_json
import zmq
from PIL import Image
import numpy as np
from config import Config
import glob
import csv


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
        # self.context = zmq.Context()
        # self.videoEmotionsSocket = self.context.socket(zmq.PUSH)
        # self.videoEmotionsSocket.bind(zmqSocket)

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
        currentGameVideoCsv = sorted(glob.glob(\
        Config().classifierOutputVideoPath + '/*'),\
        key = os.path.getmtime)[-1]
        with open(currentGameVideoCsv, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Config().videoHeader)
            writer.writerow({\
            'filename': os.path.basename(path), \
            'max_emotion': predictedEmotion, \
            'emotion_label': Config().videoLabels[predictedEmotion], \
            'AN': predictions[0][0], \
            'FE': predictions[0][1], \
            'HA': predictions[0][2], \
            'SA': predictions[0][3], \
            'SU': predictions[0][4]})


if __name__ == "__main__":
    # db = DbConnector()
    logging.basicConfig(filename='logs/videoModule.log',level=logging.DEBUG)
    
    if len(sys.argv) != 2:
        logging.debug('Incorrect number of arguments, required 1 with'\
        'audio file path')
        sys.exit(5)

    videoClassifier = VideoAnalyser(str(sys.argv[1]))
    videoClassifier.analyse(videoClassifier.videoPath)
