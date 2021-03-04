import random
from recognizers.speech.voice_recognizer import VoiceRecognizer, get_audio_devices_names
import pyttsx3
import json

from signal_processors.user_input_processor import UserInputProcessor


class IPlayer():
    """ Interface for the players """

    def propose(self, total):
        # how much money I want for myself
        pass

    def respond(self, fraction):
        # agree or disagree on the other user proposition
        pass


class RandomPlayer:
    """ Random UG player
    offers:
        random
    accepts:
        random
    """

    def propose(self, total):
        return random.randrange(0, total)

    def respond(self, fraction):
        return bool(random.getrandbits(1))


class WeightedPlayer:
    """ Same as random, but the probability of acceptance
     is adjusted for the fraction being proposed
    offers:
        random
    accepts:
        random, more likely for better offers
    """

    def propose(self, total):
        return random.randrange(0, total)

    def respond(self, fraction):
        return random.uniform(0, 1) <= fraction


class EmotionalPlayer:
    def __init__(self, ui_processor):
        # type: (UserInputProcessor) -> None
        self.ui_processor = ui_processor

    def propose(self, total):
        emotion = self.ui_processor.get_user_last_emotion()
        is_pos = self.ui_processor.check_if_emotion_positive(emotion)
        if is_pos:
            return random.randrange(int(total/2) + 1, total)
        else:
            return random.randrange(0, int(total/2))

    def respond(self, fraction):
        emotion = self.ui_processor.get_user_last_emotion()
        is_pos = self.ui_processor.check_if_emotion_positive(emotion)
        if is_pos:
            return 1
        else:
            return 0
