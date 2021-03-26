
import time
from six.moves import queue
import random
import numpy as np

class AudioSessionManager(object):
    """Manages audio session with the robot"""
    RATE = 16000

    def __init__(self, session, nFrames):
        super(AudioSessionManager, self).__init__()
        self._buff = queue.Queue()
        self.isProcessingDone = True
        self.nbOfFramesToProcess = nFrames
        self.framesCount = 0
        self.micFront = []
        self.session = session
        self.audio_service = self.session.service("ALAudioDevice")
        self.module_name = "SoundProcessingModule" + str(random.randint(0, 10000))
        print("Service is being registered")
        session.registerService(self.module_name, self)


    def __enter__(self):
        print("Starting listening session")
        self.audio_service.setClientPreferences(self.module_name, AudioSessionManager.RATE, 3, 0)
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
