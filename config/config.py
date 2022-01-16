from naoservices import NaoServices
from gameversions import GameVersions
from pathprovider import PathProvider


class Config:
    def __init__(self):
        self.ip = "nao.local"
        self.fullIp = "tcp://" + self.ip
        self.language = "Polish"
        self.port = "9559"

        self.services = NaoServices()

        self.version = GameVersions().emphatic

        self.paths = PathProvider()
        self.audioPath = self.paths.audioLogs
        self.videoPath = self.paths.videoLogs
        self.emotionAudioClassifierLogs = self.paths.emotionAudioClassifierLogs
        self.emotionVideoClassifierLogs = self.paths.emotionVideoClassifierLogs

        self.audioLabels = ["AN", "DI", "FE", "HA", "NE", "SA"]
        self.videoLabels = ["AN", "FE", "HA", "SA", "SU"]
        self.audioHeader = [
            "filename",
            "max_emotion",
            "emotion_label",
            "AN",
            "DI",
            "FE",
            "HA",
            "NE",
            "SA",
        ]
        self.videoHeader = [
            "filename",
            "max_emotion",
            "emotion_label",
            "AN",
            "FE",
            "HA",
            "SA",
            "SU",
        ]


if __name__ == "__main__":
    Config()
