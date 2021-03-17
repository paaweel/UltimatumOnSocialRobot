#!/usr/bin/env python
#-*- coding: utf-8 -*-

from robot import Robot
from player import RandomPlayer, WeightedPlayer, EmotionalPlayer
import time
import string
from datetime import datetime, timedelta

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

    def __game_intro(self):
        self.robot.say("Kiedyś tutaj będą zasady gry.")
        time.sleep(1)

    def __get_integer(self, transcript, min=1, max=9):
        for i in transcript:
            print("in loop", i.word, i.startTime)
            if i.word.encode('utf8').isdigit():
                print("all formats:", i.word, int(i.word), i.word.encode('utf8'), int(i.word.encode('utf8')), str(i.word))
                digit = int(i.word.encode('utf8'))
                if digit < 1:
                    self.robot.say("Za mało, ma być więcej niż 0, powtórz.")
                    time.sleep(3)
                    return False
                if digit > 9:
                    self.robot.say("Za dużo, ma być mniej niż 10, powtórz.")
                    time.sleep(3)
                    return False
                return digit
        return None

    def get_offer(self, sayTextTimespan):
        now = datetime.now()
        print("now: ", now)
        time.sleep(3)
        transcript = self.robot.receiveTranscript()
        validStartTime = now + sayTextTimespan
        print("validStartTime", validStartTime)
        print("before:")
        print("len(transcript))", len(transcript))
        for i in transcript:
            print(i.word, i.startTime, i.startTime > validStartTime)
        transcript = [word for word in transcript if word.startTime > validStartTime]
        print("len(transcript))", len(transcript))
        print("after:")
        for i in transcript:
            print(i.word, i.startTime, i.startTime > validStartTime)
        #
        # offerValue = self.__get_integer(transcript, 1, 9)
        # while offerValue == None or not offerValue:
        #     now = datetime.now()
        #     time.sleep(2)
        #     transcript = self.robot.receiveTranscript()
        #     offerValue = self.__get_integer(transcript, now + timedelta(0, 2, 100000))
        #     if offerValue == None:
        #         self.robot.say("Nie zrozumiałem, powtórz.")
        # return offerValue

    def ask_player_for_offer(self):
        self.robot.say("Podaj swoją propozycję.")
        response = self.get_offer(timedelta(0, 1, 500000))
        self.robot.say("Wybrałeś " + str(response))
        return response

    def pepper_accepts(self, player_proposition, total):
        accepted = self.player.respond(player_proposition / total)
        if accepted:
            self.robot.say("Akceptuję, dostajesz " + str(player_proposition))
        else:
            self.robot.say("Nie akceptuję, nie dostajesz nic")

    def __game_finish(self):
        self.robot.say("Dziękuję za grę")

    def ask_player_if_accepts(self, proposition):
        self.robot.say("Proponuję ci " + str(proposition) + "Czy akceptujesz?")
        decision = self.ask_yes_no(timedelta(0, 1, 100000))
        if decision:
            self.robot.say("Wspaniale, otrzymujesz " + str(proposition))
        else:
            self.robot.say("Trudno, zostajesz z niczym.")
        time.sleep(3)

    def __get_yes_no(self, transcript):
        for i in transcript:
            if i.word.lower().encode('utf8') == "tak":
                return True
            if i.word.lower().encode('utf8') == "nie":
                return False
        return None

    def ask_yes_no(self, sayTextTimespan):
        now = datetime.now()
        time.sleep(3)
        transcript = self.robot.receiveTranscript()
        validStartTime = now + sayTextTimespan
        transcript = [word for word in transcript if word.startTime > validStartTime]
        decision = self.__get_yes_no(transcript)
        while decision == None:
            now = datetime.now()
            time.sleep(2)
            transcript = self.robot.receiveTranscript()
            validStartTime = now + timedelta(0, 2, 100000)
            transcript = [word for word in transcript if word.startTime > validStartTime]
            decision = self.__get_yes_no(transcript)
            if decision == None:
                self.robot.say("Nie zrozumiałem, powtórz.")
        return decision

    def run(self):
        total = 10
        t1 = datetime.now()
        self.robot.say("Cześć, chcesz zagrać w grę?")
        t2 = datetime.now()
        utteranceSpan = t2 - t1
        print(utteranceSpan, t1, t2)
        # if self.ask_yes_no(timedelta(0, 2, 000000)):
        #     for i in range(2):
        #         pepper_proposition = self.player.propose(total)
        #         self.ask_player_if_accepts(pepper_proposition)
        #         player_proposition = self.ask_player_for_offer()
        #         self.pepper_accepts(player_proposition, total)
        #     self.game_finish()
        print("odmowa gry w grę, koniec programu")
        self.robot.stop()
