from chatbot_connector import Chatbot

import qi
from scp import SCPClient
import paramiko
import speech_recognition as sr

from ..config.config import Config


class Speech:
    def __init__(self, app) -> None:
        self.app = app
        self.speech_service = app.session.service("ALSpeechRecognition")
        self.audio_recorder = app.session.service("ALAudioRecorder")
        self.memory_service = app.session.service("ALMemory")
        self.led_service = app.session.service("ALLeds")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(
            hostname="nao.local", username="xxx", password="xxxxx"
        )  # TODO: secrets
        self.scp = SCPClient(ssh.get_transport())

    def listen(self):
        self.speech_service.setAudioExpression(False)
        self.speech_service.setVisualExpression(False)
        self.audio_recorder.stopMicrophonesRecording()
        print("[INFO]: Speech recognition is in progress. Say something.")
        try:
            self.audio_recorder.startMicrophonesRecording(
                "/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0)
            )
            print("[INFO]: Robot is listening to you")
            self.blink_eyes([255, 255, 0])
            while True:
                pass
        except KeyboardInterrupt:
            pass

        try:
            self.audio_recorder.stopMicrophonesRecording()
            print("[INFO]: Robot is not listening to you")
            self.blink_eyes([0, 0, 0])
            while True:
                pass
        except KeyboardInterrupt:
            pass

        print("Lopp exit")
        self.download_file("speech.wav")
        self.speech_service.setAudioExpression(True)
        self.speech_service.setVisualExpression(True)

        return self.speech_to_text("speech.wav")

    def speech_to_text(self, audio_file):
        r = sr.Recognizer()
        with sr.AudioFile("/tmp/" + audio_file) as source:
            audio = r.record(source)  # read the entire audio file

        text = r.recognize_google(audio, language="pl-PL")
        print(text)
        return text

    def download_file(self, file_name):
        """
        Download a file from robot to ./tmp folder in root.
        ..warning:: Folder ./tmp has to exist!
        :param file_name: File name with extension (or path)
        :type file_name: string
        """
        self.scp.get(file_name, local_path="/tmp/")
        print("[INFO]: File " + file_name + " downloaded")
        self.scp.close()

    def blink_eyes(self, rgb):
        self.led_service.fadeRGB("AllLeds", rgb[0], rgb[1], rgb[2], 1.0)


if __name__ == "__main__":
    c = Config()

    # bot = Chatbot()
    # app = qi.Application(url="tcp://nao.local")

    # app.start()
    # s = Speech(app)
    # s.blink_eyes([255, 0, 255])
