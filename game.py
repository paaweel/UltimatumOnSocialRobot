#!/usr/bin/env python
#-*- coding: utf-8 -*-

from robot import Robot
from player import RandomPlayer, WeightedPlayer, EmotionalPlayer
import time
import string

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

    def __getTranscript(self, skippedText, trials=5):
        skippedText = skippedText.lower()
        print("skippedText", skippedText)
        for i in range(trials):
            transcript = self.robot.receiveTranscript().lower().encode('utf8')
            print("transcript: ", transcript)
            if transcript is None or skippedText in transcript:
                continue
            else:
                return transcript

    def __ask_yes_no(self, inquiryText, sleepTime):
        self.robot.say(inquiryText)
        skippedText = ' '.join(inquiryText.split()[-1:])
        table = string.maketrans("","")
        skippedText = skippedText.translate(table, string.punctuation)
        transcript = self.__getTranscript(skippedText).strip()
        print("transcript", transcript)
        while transcript != 'tak' and transcript != 'nie':
            repeatInquiryText = "Nie zrozumiałem, powtórz."
            self.robot.say(repeatInquiryText)
            transcript = self.__getTranscript('powtórz').strip()
            print("transcript", transcript)
        return transcript == 'tak'

    def __ask_for_integer(self, inquiryText, sleepTime):
        self.robot.say(inquiryText)
        skippedText = ' '.join(inquiryText.split()[-1:])
        table = string.maketrans("","")
        skippedText = skippedText.translate(table, string.punctuation)
        transcript = self.__getTranscript(skippedText).strip()
        print("transcript", transcript)
        while not transcript.isdigit() or int(transcript) > 9 or int(transcript) < 1:
            if not transcript.isdigit():
                repeatInquiryText = "Nie zrozumiałem, powtórz."
                self.robot.say(repeatInquiryText)
                transcript = self.__getTranscript('powtórz').strip()
                print("transcript", transcript)
            else:
                number = int(transcript)
                if number > 9:
                    repeatInquiryText = "Za dużo, ma być mniej niż 10, powtórz."
                    self.robot.say(repeatInquiryText)
                    transcript = self.__getTranscript('powtórz').strip()
                    print("transcript", transcript)
                if number < 1:
                    repeatInquiryText = "Za mało, ma być więcej niż 0, powtórz."
                    self.robot.say(repeatInquiryText)
                    transcript = self.__getTranscript('powtórz').strip()
                    print("transcript", transcript)
        return int(transcript)

    def __game_intro(self):
        self.robot.say("Kiedyś tutaj będą zasady gry.")
        time.sleep(1)

    def __ask_player_if_accepts(self, proposition):
        response = self.__ask_yes_no("Proponuję ci " + str(proposition) + "Czy akceptujesz?", 4)
        print(response)
        if response:
            self.robot.say("Wspaniale, otrzymujesz " + str(proposition))
        else:
            self.robot.say("Trudno, zostajesz z niczym.")
        time.sleep(3)

    def __ask_player_for_offer(self):
        response = self.__ask_for_integer("Podaj swoją propozycję.", 3)
        self.robot.say("Wybrałeś " + str(response))
        return response

    def __pepper_accepts(self, player_proposition, total):
        accepted = self.player.respond(player_proposition / total)
        if accepted:
            self.robot.say("Akceptuję, dostajesz " + str(player_proposition))
        else:
            self.robot.say("Nie akceptuję, nie dostajesz nic")

    def __game_finish(self):
        self.robot.say("Dziękuję za grę")

    def run(self):
        total = 10
        decision = self.__ask_yes_no("Cześć, chcesz zagrać w grę?", 3)
        if decision:
            for i in range(2):
                pepper_proposition = self.player.propose(total)
                self.__ask_player_if_accepts(pepper_proposition)
                player_proposition = self.__ask_player_for_offer()
                self.__pepper_accepts(player_proposition, total)
            self.__game_finish()
        print("odmowa gry w grę, koniec programu")
        self.robot.stop()
