import time
from six.moves import queue
import random
import numpy as np

import string
import random
import types
RATE = 16000

class AudioSessionManager(object):
    """Manages audio session with the robot"""


    def __init__(self, session):
        super(AudioSessionManager, self).__init__()
        self.audio_service = session.service("ALAudioDevice")
        self.module_name = ''.join([random.choice(string.ascii_letters) for n in xrange(32)])
        session.registerService(self.module_name, self)
        # Get the service ALAudioDevice.

        self.isProcessingDone = True
        self.nbOfFramesToProcess = 20
        self.framesCount = 0
        self.micFront = []
        # self.module_name = Microphone.__class__.__name__
        self._buff = queue.Queue()

    def __enter__(self):
        self.audio_service.setClientPreferences(self.module_name, RATE, 3, 0)
        self.audio_service.subscribe(self.module_name)
        self.isProcessingDone = False
        return self

    def __exit__(self, type, value, traceback):
        self.audio_service.unsubscribe(self.module_name)
        self.isProcessingDone = True
        self._buff.put(None)

    def startProcessing(self):
        """
        Start processing
        """
        # ask for the front microphone signal sampled at 16kHz
        self.audio_service.setClientPreferences(self.module_name, RATE, 3, 0)
        self.audio_service.subscribe(self.module_name)
        self.isProcessingDone = False

        while not self.isProcessingDone:
            time.sleep(0.5)


    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        self._buff.put(inputBuffer)

    def generator(self):
        while not self.isProcessingDone:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
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

            yield data
