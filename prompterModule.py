# -*- encoding: UTF-8 -*-
"""
Prompts what to say during HRI.
"""
import qi
NAO_IP = "192.168.0.28"
LANGUAGE="Polish"


def main():
    """ Main entry point
    """
    session = qi.Session()
    try:
        session.connect("tcp://" + NAO_IP)
        say_service = session.service("ALTextToSpeech")
        say_service.setLanguage(LANGUAGE)
        print("Robot connected to SAY module.")
        print("Press CTRL+C to exit.")
        while(True):
            text = raw_input('Type what the robot should say and press ENTER:')
            say_service.say(text)
    except RuntimeError:
        print("Can't connect to Nao at ip: " + NAO_IP)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"



if __name__ == "__main__":
    main()
