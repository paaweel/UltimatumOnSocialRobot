import numpy as np
import librosa
from datetime import datetime
import logging

# from dbConnector import DbConnector
import os
from tensorflow.keras.models import model_from_json
import sys
import csv
from config import Config
import glob

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


class AudioModule:
    def __init__(self, audioPath):
        self.audioPath = audioPath

        AI_MODELS_DIR = os.path.join(os.getcwd(), "AI_models/audio")
        # think about changing to one-time loading, takes ~ 0.15s
        with open(os.path.join(AI_MODELS_DIR, "best.json"), "r") as json_file:
            txt_model = json_file.read()
            self.model = model_from_json(txt_model)
            self.model.load_weights(os.path.join(AI_MODELS_DIR, "best.hdf5"))

    def extract_features(self, data, sr):
        # ZCR
        result = np.array([])
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
        result = np.hstack((result, zcr))  # stacking horizontally

        # Chroma_stft
        stft = np.abs(librosa.stft(data))
        chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T, axis=0)
        result = np.hstack((result, chroma_stft))  # stacking horizontally

        # MFCC
        mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mfcc))  # stacking horizontally

        # Root Mean Square Value
        rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
        result = np.hstack((result, rms))  # stacking horizontally

        # MelSpectogram
        mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sr).T, axis=0)
        result = np.hstack((result, mel))  # stacking horizontally

        return np.expand_dims(np.array(result), axis=-1)

    def analyse(self, path):
        data, sr = librosa.load(path)
        audioFeatures = self.extract_features(data, sr)
        predictions = self.model.predict(np.expand_dims(audioFeatures, axis=0))
        predictedEmotion = np.argmax(predictions)
        # self.audioEmotionsSocket.send(predictions)
        logging.debug(
            "AUDIO {0}: {1} -> {2}".format(path, predictedEmotion, predictions)
        )
        currentGameAudioCsv = sorted(
            glob.glob(Config().classifierOutputAudioPath + "/*"), key=os.path.getmtime
        )[-1]
        with open(currentGameAudioCsv, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Config().audioHeader)
            writer.writerow(
                {
                    "filename": os.path.basename(path),
                    "max_emotion": predictedEmotion,
                    "emotion_label": Config().audioLabels[predictedEmotion],
                    "AN": predictions[0][0],
                    "DI": predictions[0][1],
                    "FE": predictions[0][2],
                    "HA": predictions[0][3],
                    "NE": predictions[0][4],
                    "SA": predictions[0][5],
                }
            )


if __name__ == "__main__":
    # db = DbConnector()
    logging.basicConfig(filename="logs/audioModule.log", level=logging.DEBUG)
    if len(sys.argv) != 2:
        logging.debug(
            "Incorrect number of arguments, required 1 with" "audio file path"
        )
        sys.exit(5)
    audioClassifier = AudioModule(str(sys.argv[1]))
    audioClassifier.analyse(audioClassifier.audioPath)
