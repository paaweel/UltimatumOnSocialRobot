from datetime import timedelta
import numpy as np

def rgb2gray(img):
    rgb_weights = [0.2989, 0.5870, 0.1140]
    return np.dot(img[...,:3], rgb_weights)


class WordInfo:
    def __init__(self, **kwargs):
        now = kwargs.get("now", "")
        sT = float(kwargs.get("startTime", "")[:-1])
        eT = float(kwargs.get("endTime", "")[:-1])
        self.startTime= now + timedelta(0, sT)
        self.endTime=now + timedelta(0, eT)
        self.word=kwargs.get("word", "")

    def __str__(self):
        return self.word.encode('utf8') + " " + str(self.startTime) + " "  + str(self.endTime)
