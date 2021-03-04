import os
from recognizers.camera.image_recognizer import ImageRecognizer
from recognizers.speech.voice_recognizer import VoiceRecognizer, get_audio_devices_names
import pyttsx3
import json

from signal_processors.user_input_processor import UserInputProcessor


class HumanInterface:
    """
    I/O for human interaction

        Attributes
        ----------
        language : string
            Information about the language in which player speaks.
        dictionary: dictionary
            Set of sentences that can be uttered by the player in chosen language.

        Methods
        -------
        say(text)
            Verbalises the string passed as parameter.
        ask_yes_no(text)
            Verbalises the string passed as parameter and waits for verbal confirmation or rejection.
        ask_int(text)
            Verbalises the string passed as parameter and waits for naming an integer.

    """

    def __init__(self, language, ui_processor, analyze_emotions=False):
        self._engine = pyttsx3.init()
        self.language = language
        with open('languages.json') as f:
            data = json.load(f)
        self.dictionary = data[language]
        self._engine.setProperty('voice', language)
        self._voice_recognizer = VoiceRecognizer(self.dictionary["voice_recogniser_language_symbol"],
                                                 ui_processor,
                                                 analyze_emotions)
        self._image_recognizer = ImageRecognizer(os.getcwd(), ui_processor)

    def run_watch(self):
        """Launches visual signal acquisition by the robot/player."""
        self._image_recognizer.watch()

    def say(self, text):
        """Verbalises the string passed as parameter.
                Parameters
                ----------
                text : string
                    Text that will be played on speakers.
                """
        self._image_recognizer.take_glimpse()
        self._engine.say(text)
        self._engine.runAndWait()

    def ask_yes_no(self, text):
        """Verbalises the string passed as parameter and waits for verbal confirmation or rejection.
                Parameters
                ----------
                text : string
                    Text that will be played on speakers.
                """
        self.say(text)
        unrecognised = True
        while unrecognised:
            self._image_recognizer.take_glimpse()
            response = self._voice_recognizer.recognize_speech_from_mic()
            yes_no = response['transcription']
            print(yes_no)
            yes = self.dictionary["yes"]
            if any(option == yes_no for option in yes):
                return "yes"
            no = self.dictionary["no"]
            if any(option == yes_no for option in no):
                return "no"
            self.say(self.dictionary["unrecognised_speach"])
            self.say(text)
            self._engine.runAndWait()
        return False

    def ask_int(self, text):
        """Verbalises the string passed as parameter and waits for naming an integer.
                Parameters
                ----------
                text : string
                    Text that will be played on speakers.
                """
        self.say(text)
        unrecognised = True
        while unrecognised:
            self._image_recognizer.take_glimpse()
            response = self._voice_recognizer.recognize_speech_from_mic()
            try:
                integer = int(response['transcription'])
                unrecognised = False
            except:
                self.say(self.dictionary["unrecognised_speach"])
                self.say(text)
                self._engine.runAndWait()
        return integer
