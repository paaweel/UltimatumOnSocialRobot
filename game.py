#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
        self.totalMoney = 10
        self.refusalFraction = 0.5
        self.humanOffer = 0
        self.humanTotalScore = 0
        self.player = player_choice(player_type)
        self.robotOffer = 0
        self.robotTotalScore = 0
