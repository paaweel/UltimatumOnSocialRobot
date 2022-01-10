#!/usr/bin/env python
# -*- coding: utf-8 -*-

from player import RandomPlayer, WeightedPlayer, EmotionalPlayer


def get_player(player_type, ui_processor=None):
    return {
        "weighted": WeightedPlayer(),
        "random": RandomPlayer(),
        "emotional": EmotionalPlayer(),
    }.get(player_type, RandomPlayer())


class UltimatumGame:
    """
        Class for playing ultimatum game with mocked Pepper.

        ...
    F
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
        self.player_type = player_type
        self.player = get_player(player_type)
        self.robotOffer = 0
        self.robotTotalScore = 0
