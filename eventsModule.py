# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
import random
import qi

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

from game import UltimatumGame
from soundDetector import SoundDetector
from config import Config
import csv
from datetime import datetime


# Global variable to store the HumanGreeter module instance
Events = None
memory = None


class EventsModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name, session):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the UserIsHappy event:
        global memory
        memory = ALProxy("ALMemory")
        self.ultimatumGame = UltimatumGame()
        self.soundDetector = SoundDetector(session)
        self.currentGameAudioCsv = ""
        self.currentGameVideoCsv = ""

    def onNewGame(self):
        timestamp = datetime.now().strftime("%Y-%b-%d_%H:%M:%S")
        self.currentGameAudioCsv = '{2}/v-{0}-{1}.csv'.format(Config().version.split('.')[0], timestamp, Config().classifierOutputAudioPath)
        with open(self.currentGameAudioCsv, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Config().audioHeader)
            writer.writeheader()

        # launch videoModule here (with a separate process / thread)
        # pass an argument with csv path
        # after the game finishes make sure the process is dead
        self.currentGameVideoCsv = '{2}/v-{0}-{1}.csv'.format(Config().version.split('.')[0], timestamp, Config().classifierOutputVideoPath)
        with open(self.currentGameVideoCsv, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=Config().videoHeader)
            writer.writeheader()

    def setListenFlag(self):
        self.soundDetector.waitForSound = True

    def resetListenFlag(self):
        if self.soundDetector.waitForSound:
            self.soundDetector.waitForSound = False
            self.soundDetector.stopListening(self.currentGameAudioCsv)

    def onHumanOffers(self, offer):
        print("Human offer value: ", offer)
        self.ultimatumGame.humanOffer = offer
        if self.ultimatumGame.player.respond(self.ultimatumGame.refusalFraction):
            self.ultimatumGame.robotTotalScore += self.ultimatumGame.humanOffer
            self.ultimatumGame.humanTotalScore += self.ultimatumGame.totalMoney - self.ultimatumGame.humanOffer
            print("Total score R:H: ", self.ultimatumGame.robotTotalScore, self.ultimatumGame.humanTotalScore)
            print(True)
            return "True"
        print("Total score R:H: ", self.ultimatumGame.robotTotalScore, self.ultimatumGame.humanTotalScore)
        print(False)
        return "False"

    def onDrawOffer(self):
        robotOffer = self.ultimatumGame.player.propose(self.ultimatumGame.totalMoney)
        self.ultimatumGame.robotOffer = robotOffer
        print("Robot offer value: ", robotOffer)
        return robotOffer

    def onHumanDecision(self, decision):
        print("decision", decision)
        if decision == "True":
            self.ultimatumGame.humanTotalScore += self.ultimatumGame.robotOffer
            self.ultimatumGame.robotTotalScore += self.ultimatumGame.totalMoney - self.ultimatumGame.humanOffer
        print("Total score R:H: ", self.ultimatumGame.robotTotalScore, self.ultimatumGame.humanTotalScore)


def runEventListener():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=Config().ip,
        pport=Config().port)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    session = qi.Session()
    try:
        session.connect("tcp://" + Config().ip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + Config().ip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global Events
    Events = EventsModule("Events", session)

    try:
        # raw_input()
        while(True):
            a = 1
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)



if __name__ == "__main__":
    runEventListener()
