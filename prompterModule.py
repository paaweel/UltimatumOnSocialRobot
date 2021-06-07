# -*- encoding: UTF-8 -*-
"""
Prompts what to say during HRI.
"""
import qi
from config import Config


def main():
    """ Main entry point
    """
    session = qi.Session()
    try:
        session.connect("tcp://" + Config().ip)
        say_service = session.service("ALTextToSpeech")
        say_service.setLanguage(Config().language)
        print("Robot connected to SAY module.")
        print("Press CTRL+C to exit.")
        while(True):
            text = raw_input('Type what the robot should say and press ENTER:')
            say_service.say(text)
    except RuntimeError:
        print("Can't connect to Nao at ip: " + Config().ip)
    except KeyboardInterrupt:
        print "Interruption received, shutting down"



if __name__ == "__main__":
    main()
