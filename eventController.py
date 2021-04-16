# -*- encoding: UTF-8 -*-
""" Say 'hello, you' each time a human face is detected

"""

import sys
import time
import random

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

from game import UltimatumGame

NAO_IP = "nao.local"
PEPPER_IP = '192.168.1.123'


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

        # Subscribe to the UserIsHappy event:
        global memory
        memory = ALProxy("ALMemory")
        self.ultimatumGame = UltimatumGame()

    def onHumanOffers(self, offer):
        print("Human offer value: ", offer)
        self.ultimatumGame.humanOffer = offer
        if self.ultimatumGame.player.respond(self.ultimatumGame.refusalFraction):
            self.ultimatumGame.robotTotalScore += self.ultimatumGame.humanOffer
            self.ultimatumGame.humanTotalScore += self.ultimatumGame.totalMoney - self.ultimatumGame.humanOffer
            print("Total score R:H: ", self.ultimatumGame.robotTotalScore, self.ultimatumGame.humanTotalScore)
            return "True"
        print("Total score R:H: ", self.ultimatumGame.robotTotalScore, self.ultimatumGame.humanTotalScore)
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
        pip=NAO_IP,
        pport=9559)

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


    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global HumanGreeter
    HumanGreeter = HumanGreeterModule("HumanGreeter")

    try:
        raw_input()
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)



if __name__ == "__main__":
    runEventListener()
