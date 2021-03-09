#!/usr/bin/env python
#-*- coding: utf-8 -*-

from robot import Robot
from player import RandomPlayer, WeightedPlayer, EmotionalPlayer
import time

def player_choice(player_type, ui_processor=None):
    return {
        'weighted': WeightedPlayer(),
        'random': RandomPlayer(),
        'emotional': EmotionalPlayer()
    }[player_type]


class UltimatumGame:
    """
        Class for playing ultimatum game with mocked Pepper.

        ...

        Attributes
        ----------
        player : Player
            Pepper robot mocked on the PC


        Methods
        -------
        run()
            Launches ultimatum game.
        """

    def __init__(self, player_type="random"):
        self.robot = Robot()
        self.robot.start()
        self.player = player_choice(player_type)

    def __getTranscript(self, skippedText, trials=2):
        skippedText = skippedText.lower()
        for i in range(trials):
            transcript = self.robot.receiveTranscript().lower().encode('utf8')
            if transcript is None or skippedText in transcript:
                continue
            else:
                return transcript

    def __game_offer(self):
        self.robot.say("Cześć, chcesz zagrać w grę?")
        time.sleep(3)
        return self.__getTranscript(skippedText="Chcesz zagrać w grę")

    def __game_intro(self):
        self.robot.say("Kiedyś tutaj będą zasady gry.")
        time.sleep(1)

    def __pepper_offers(self, total):
        proposition = self.player.propose(total)
        self.robot.say("Proponuję ci " + str(proposition))
        return proposition

    def __ask_player_if_accepts(self, proposition):
        response = self.humanInterface.ask_yes_no(self.humanInterface.dictionary["ask_if_accepts"])
        if response == 'yes':
            self.humanInterface.say(self.humanInterface.dictionary["announce_receiving"] + str(proposition))
        else:
            self.humanInterface.say(self.humanInterface.dictionary["offer_rejected"])

    def __ask_player_for_offer(self):
        response = self.humanInterface.ask_int(self.humanInterface.dictionary["ask_for_offer"])
        self.humanInterface.say(self.humanInterface.dictionary["confirm_offer"] + str(response))
        return response

    def __pepper_accepts(self, player_proposition, total):
        accepted = self.player.respond(player_proposition / total)
        if accepted:
            self.humanInterface.say(self.humanInterface.dictionary["offer_accepted"])
        else:
            self.humanInterface.say(self.humanInterface.dictionary["offer_rejected"])

    def __game_finish(self):
        self.robot.say("Dziękuję za grę")

    def run(self):
        decision = self.__game_offer()
        print(decision)
        if "tak" in decision:
            for i in range(1):
                pepper_proposition = self.__pepper_offers(10)
                # self.__ask_player_if_accepts(pepper_proposition)
                # player_proposition = self.__ask_player_for_offer()
                # self.__pepper_accepts(player_proposition, total)
            self.__game_finish()
        print("odmowa gry w grę, koniec programu")
        self.robot.stop()
