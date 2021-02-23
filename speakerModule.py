# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time

import qi

NAO_IP = "192.168.0.28"


# Global variable to store the HumanGreeter module instance
Speaker = None
memory = None

#/home/naoqi_lib/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages
class SpeakerModule:
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + NAO_IP)
            self.say_service = self.session.service("ALTextToSpeech")
            self.say_service.setLanguage(language)
            print("Robot connected to SAY module.")
        except RuntimeError:
            print("Can't connect to Nao at ip: " + NAO_IP)

    def say(self, text):
        self.say_service.say(text)


def main():
    """ Main entry point

    """
    session = qi.Session()
    try:
        session.connect("tcp://" + NAO_IP)
        say_service = session.service("ALTextToSpeech")
        say_service.setLanguage(language)
        print("Robot connected to SAY module.")
        say_service.say("Cześć, ziom!")
    except RuntimeError:
        print("Can't connect to Nao at ip: " + NAO_IP)



if __name__ == "__main__":
    main()
