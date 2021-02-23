# -*- coding: utf-8 -*-

import string
import random

import qi
import sys
import naoqi

import numpy as np
import time
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

    def getAudio(self, timeout=1):
        with AudioSessionManager(self.session, timeout * 10) as stream:
            content = [content.tobytes() for content in stream.data()]
            return content

    def __enter__(self):
        print("Starting listening session")
        self.audio_service.setClientPreferences(self.module_name, SAMPLE_RATE, 3, 0)
        self.audio_service.subscribe(self.module_name)
        self.isProcessingDone = False
        return self


    def __exit__(self, type, value, traceback):
        print("Processing finished")
        self.audio_service.unsubscribe(self.module_name)
        self.isProcessingDone = True
        self._buff.put(None)


    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        if (self.framesCount <= self.nbOfFramesToProcess):
            print("Processing remote, frame count: " + str(self.framesCount))
            self.framesCount = self.framesCount + 1
            self._buff.put(inputBuffer)
        else :
            self.isProcessingDone=True


    def data(self):
        print("return data")
        chunk = self._buff.get()
        if chunk is None:
            return

        data = np.frombuffer(chunk, np.int16)
        # Now consume whatever other data's still buffered.
        while True:
            try:
                chunk = self._buff.get(block=False)
                if chunk is None:
                    return
                data = np.concatenate((data, np.frombuffer(chunk, np.int16)), axis=None)
            except queue.Empty:
                break

        return data

def main():
    """ Main entry point
    """
    listener = ListenerModule()
    listener.listen()

if __name__ == "__main__":
    main()
