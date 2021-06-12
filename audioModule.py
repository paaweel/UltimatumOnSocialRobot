import random
import numpy as np
import librosa
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


    def extract_features(self, data, sr):
        # ZCR
        result = np.array([])
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
        result=np.hstack((result, zcr)) # stacking horizontally

        # Chroma_stft
        stft = np.abs(librosa.stft(data))
        chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
        result = np.hstack((result, chroma_stft)) # stacking horizontally

        # MFCC
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mfcc)) # stacking horizontally

        # Root Mean Square Value
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        result = np.hstack((result, rms)) # stacking horizontally

        # MelSpectogram
        mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mel)) # stacking horizontally

        return np.expand_dims(np.array(result), axis=-1)


    def analyse(self, path):
        data, sr = librosa.load(path)
        audioFeatures = self.extract_features(data, sr)
        logging.debug('Features shape: {0}'.format(audioFeatures.shape))
        predictions = self.model.predict(np.expand_dims(audioFeatures, axis=0))
        predictedEmotion = np.argmax(predictions)
        print(predictedEmotion, predictions)
        # self.audioEmotionsSocket.send(predictions)
        logging.debug('AUDIO: {0} -> {1}'.format(predictedEmotion, predictions))


if __name__ == "__main__":
    # db = DbConnector()
    logging.basicConfig(filename='audioModule.log',level=logging.DEBUG)
    logging.debug('Starting audio module')
    if len(sys.argv) != 2:
        logging.debug('Incorrect number of arguments, required 1 with'\
        'audio file path')
        sys.exit(5)
    audioClassifier = AudioModule(str(sys.argv[1]))
    audioClassifier.analyse(audioClassifier.audioPath)
    logging.debug('Exitting audio module')
