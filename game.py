from __future__ import division, print_function
from signal_processors.user_input_processor import UserInputProcessor

from ug_players import RandomPlayer, WeightedPlayer, EmotionalPlayer
from human_interface import HumanInterface


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

    def __init__(self, language="english", player_type="random"):
        """Initializes an instance of a class that manages the game.
                Parameters
                ----------
                language : string
                    Information in which language should be the game. (default is english)
                    Supported languages: english, polish.
                player_type : string
                    Information about the type of Pepper player. (default is random)
                    Supported player types: random, weighted
                """
        self.ui_processor = UserInputProcessor()
        self.player = player_choice(player_type, self.ui_processor)
        self.humanInterface = HumanInterface(language, self.ui_processor, True)

    def __game_intro(self):
        self.humanInterface.say(self.humanInterface.dictionary["welcome_game"])
        self.humanInterface.say(self.humanInterface.dictionary["random_player_introduction"])

        total = self.humanInterface.ask_int(self.humanInterface.dictionary["ask_for_total_capital"])
        self.humanInterface.say(self.humanInterface.dictionary["confirm_total_capital"] + str(total))
        return total

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
        total = self.__game_intro()
        for i in range(2):
            pepper_proposition = self.__pepper_offers(total)
            self.__ask_player_if_accepts(pepper_proposition)
            player_proposition = self.__ask_player_for_offer()
            self.__pepper_accepts(player_proposition, total)
        self.__game_finish()
