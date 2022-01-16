# -*- encoding: UTF-8 -*-


import qi
from config.config import Config

from dialogTopic import TopicLoader


class Events:
    def __init__(self, tts) -> None:
        self.tts = tts
        self.tts.say("ajm in bicz")
        self.testEventGeneric = qi.Signal()

    @qi.bind(returnType=qi.Void, paramsType=[])
    def onNewGame(self):
        print("What up duuude!")
        self.tts.say("niu gejm")


if __name__ == "__main__":

    app = qi.Application(url=Config().fullIp)
    app.start()
    # session = SessionHelper().get_active_session()
    addr = "tcp://127.0.0.1:9559"
    # geh = GameEventHandler()
    tts = app.session.service(Config().services.tts)

    tts.setLanguage(Config().language)
    ev = Events(tts)
    app.session.registerService("Events", ev)

    tl = TopicLoader(app.session)

    app.run()
