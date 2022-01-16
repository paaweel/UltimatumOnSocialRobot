# -*- encoding: UTF-8 -*-
"""
Prompts what to say during HRI.
"""

import qi
from config.config import Config


def main():
    """
    Main entry point
    """

    session = qi.Session()
    try:
        session.connect(Config().fullIp)
        say_service = session.service(Config().services.tts)
        say_service.setLanguage(Config().language)

        s = "startujemy"
        while s != "x":
            s = input(">")
            say_service.say(s)

    except RuntimeError:
        print("Can't connect to Nao at ip: " + Config().fullIp)
    except KeyboardInterrupt:
        print("Interruption received, shutting down")


if __name__ == "__main__":
    main()
