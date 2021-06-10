import random
import numpy as np
import array
import zmq
import time
from datetime import datetime
import logging
import zmq
# from dbConnector import DbConnector
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow.keras.models import model_from_json
from helperModule import *
from keras.models import model_from_json
import sys


class AudioModule:
    def __init__(self, audioPath):
        self.audioPath = audioPath
        zmqSocket = "tcp://127.0.0.1:5558"
        logging.debug('Opening PUSH ZMQ communication on '
            + zmqSocket
            + ' for audio emotion labels')
        self.context = zmq.Context()
        self.audioEmotionsSocket = self.context.socket(zmq.PUSH)
        self.audioEmotionsSocket.bind(zmqSocket)

        AI_MODELS_DIR = os.path.join(os.getcwd(), 'AI_models/audio')
        logging.debug('Loading model from ' + AI_MODELS_DIR)
        # think about changing to one-time loading, takes ~ 0.15s
        with open(os.path.join(AI_MODELS_DIR, 'best.json'), 'r') as json_file:
            txt_model = json_file.read()
            self.model = model_from_json(txt_model)
            self.model.load_weights(os.path.join(AI_MODELS_DIR, 'best.hdf5'))
            logging.debug('Model loading finished')

    def analyse():
        audioFeatures = None
        predictions = self.model.predict(audioFeatures)
        predictedEmotion = np.argmax(predictions)
        print(predictedEmotion, predictions)
        self.audioEmotionsSocket.send(predictions)
        logging.debug('AUDIO: {0} -> {1}'.format(predictedEmotion, predictions))


if __name__ == "__main__":
    # db = DbConnector()
    logging.basicConfig(filename='audioModule.log',level=logging.DEBUG)
    logging.debug('Starting audio module')
    if len(sys.argv) != 2:
        logging.debug('Incorrect number of arguments, required 1 with'\
        'audio file path')
        return
    audioClassifier = AudioModule(str(sys.argv[1]))
    logging.debug('Exitting audio module')
