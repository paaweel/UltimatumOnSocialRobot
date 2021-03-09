#!/usr/bin/env python
#-*- coding: utf-8 -*-

from robot import Robot
from speakerModule import SpeakerModule
import time

def player_choice(player_type, ui_processor=None):
    return {
        'weighted': WeightedPlayer(),
        'random': RandomPlayer(),
        'emotional': EmotionalPlayer(ui_processor)
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

    def __init__(self):
        self.robotPlayer = Robot()
        self.robotPlayer.start()
        self.speaker = SpeakerModule()

    def __getTranscript(self, skippedText, trials=10):
        for i in range(trials):
            transcript = self.robotPlayer.transcriptData
            print(transcript)
            time.sleep(0.5)
            # if transcript is None or skippedText in transcript:
            #     print("zle:", transcript)
            #     time.sleep(0.5)
            #     continue
            # else:
            #     print("dobre:", transcript)
            #     return transcript

    def __game_offer(self):
        self.speaker.say("Cześć, chcesz zagrać w grę?")
        time.sleep(5)
        return self.__getTranscript(skippedText="chcesz zagrać w grę")

    def __game_intro(self):
        self.speaker.say("Podaj swoją propozycję")
        time.sleep(1)

    def __pepper_offers(self, total):
        proposition = self.player.propose(total)
        self.humanInterface.say(self.humanInterface.dictionary["current_offer"] + str(proposition))
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
        self.humanInterface.say(self.humanInterface.dictionary["thanks_for_playing"])

    def run(self):
        self.__game_offer()
        self.robotPlayer.stop()
        # total = self.__game_intro()
        # for i in range(2):
        #     pepper_proposition = self.__pepper_offers(total)
        #     self.__ask_player_if_accepts(pepper_proposition)
        #     player_proposition = self.__ask_player_for_offer()
        #     self.__pepper_accepts(player_proposition, total)
        # self.__game_finish()
