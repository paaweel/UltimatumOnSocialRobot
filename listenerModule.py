# -*- coding: utf-8 -*-

import string
import random

import io
import qi
import sys
import naoqi

import numpy as np
import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from audioSessionManager import AudioSessionManager

# Constant to send to the ALAudiodevice and use to compute the pitch based on the fft
SAMPLE_RATE = 48000
SLEEP_TIME = 4
NAO_IP = "192.168.0.28"

class ListenerModule:
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__(self):
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + NAO_IP)
            print("Robot connected to listening_module.")
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + NAO_IP)

    def listen(self, timeout=1):
        """
        Collect microphones' output for timeout [s]
        """
        print("about to listen")
        data = self.getAudio(timeout)
        print("done")
        print(data)
        return data


    def run(self):
        with AudioSessionManager(self.session) as stream:
            audio_generator = stream.generator()

            requests = (types.StreamingRecognizeRequest(audio_content=content.tobytes())
                        for content in audio_generator)
            for i in requests:
                print(i)

def main():
    """ Main entry point
    """
    listener = ListenerModule()
    listener.run()

if __name__ == "__main__":
    main()
