from chatbot_connector import Chatbot

import qi 
from scp import SCPClient
import paramiko
from config import Config
import speech_recognition as sr

class Speech:
    def __init__(self, app) -> None:
        self.speech_service = app.session.service("ALSpeechRecognition")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(hostname=self.ip_address, username="nao", password="nao")
        self.scp = SCPClient(ssh.get_transport())

    def listen(self):
        self.speech_service.setAudioExpression(False)
        self.speech_service.setVisualExpression(False)
        self.audio_recorder.stopMicrophonesRecording()
        print("[INFO]: Speech recognition is in progress. Say something.")
        while True:
            print(self.memory_service.getData("ALSpeechRecognition/Status"))
            if self.memory_service.getData("ALSpeechRecognition/Status") == "SpeechDetected":
                self.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
                print("[INFO]: Robot is listening to you")
                self.blink_eyes([255, 255, 0])
                break

        while True:
            if self.memory_service.getData("ALSpeechRecognition/Status") == "EndOfProcess":
                self.audio_recorder.stopMicrophonesRecording()
                print("[INFO]: Robot is not listening to you")
                self.blink_eyes([0, 0, 0])
                break

        self.download_file("speech.wav")
        self.speech_service.setAudioExpression(True)
        self.speech_service.setVisualExpression(True)

        return self.speech_to_text("speech.wav")

    def speech_to_text(self, audio_file):
        r = sr.Recognizer()
        with sr.AudioFile("/tmp/" + audio_file) as source:
            audio = r.record(source)  # read the entire audio file

        print(audio)
        return audio


        

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

if __name__ == "__main__":
    bot = Chatbot()
    app = qi.Application(url=Config().fullIp)
    sr = app.session.service("ALSpeechRecognition")
    app.start()
    