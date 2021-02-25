import time
from six.moves import queue
import random
import numpy as np

import string
import random
import types
RATE = 16000

class AudioSessionManager(object):
    """
    A simple get signal from the front microphone of Nao & calculate its rms power.
    It requires numpy.
    """

    def __init__(self, session):
        """
        Initialise services and variables.
        """
        self.audio_service = session.service("ALAudioDevice")
        self.module_name = ''.join([random.choice(string.ascii_letters) for n in xrange(32)])
        session.registerService(self.module_name, self)
        # Get the service ALAudioDevice.

        self.isProcessingDone = True
        self.nbOfFramesToProcess = 10
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
        self.audio_service.unsubscribe(self.module_name)

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


if __name__ == '__main__':
    session = qi.Session()
    ip = '192.168.0.28'
    port = '9559'
    try:
        session.connect("tcp://" + ip + ":" + port)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + port + ".\n"
                                                                               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    mic = AudioSessionManager(session)
    mic.__exit__(None, None, None)
