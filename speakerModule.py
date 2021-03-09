# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""
import qi
NAO_IP = "192.168.0.28"
LANGUAGE="Polish"

class SpeakerModule:
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self):
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + NAO_IP)
            self.say_service = self.session.service("ALTextToSpeech")
            self.say_service.setLanguage(LANGUAGE)
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
        say_service.setLanguage(LANGUAGE)
        print("Robot connected to SAY module.")
        say_service.say("Cześć, ziom!")
    except RuntimeError:
        print("Can't connect to Nao at ip: " + NAO_IP)



if __name__ == "__main__":
    main()
