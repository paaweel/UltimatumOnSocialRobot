# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""
import qi
import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
NAO_IP = "192.168.0.28"
LANGUAGE="Polish"

# Global variable to store the HumanGreeter module instance
HumanGreeter = None
memory = None


class HumanGreeterModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("ALSoundLocalization/SoundLocated",
            "HumanGreeter",
            "onSoundDetected")

    def onSoundDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        # memory.unsubscribeToEvent("ALSoundLocalization/SoundLocated",
        #     "HumanGreeter")

        self.tts.say("Cześć, ziom! Klikając „Przejdź do serwisu” lub zamykając okno przez kliknięcie w znaczek X.")

        # Subscribe again to the event
        # memory.subscribeToEvent("ALSoundLocalization/SoundLocated",
        #     "HumanGreeter",
        #     "onSoundDetected")


def main():
    """ Main entry point

    """
    session = qi.Session()
    try:
        session.connect("tcp://" + NAO_IP)
        say_service = session.service("ALTextToSpeech")
        say_service.setLanguage(LANGUAGE)
        print("Robot connected to SAY module.")
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("ALSoundLocalization/SoundLocated",
            "HumanGreeter",
            "onSoundDetected")
    except RuntimeError:
        print("Can't connect to Nao at ip: " + NAO_IP)
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,         # parent broker IP
       9559)       # parent broker port


    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global HumanGreeter
    HumanGreeter = HumanGreeterModule("HumanGreeter")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()
