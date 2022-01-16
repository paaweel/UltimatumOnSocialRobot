import os
from pathlib import Path


class PathProvider:
    def __init__(self) -> None:
        self.project_root = os.path.dirname(os.path.dirname(__file__))
        if not os.path.exists(self.project_root):
            raise Exception("No root project path found")

        self.audioLogs = self.__make_path("logs/audio_files")
        self.videoLogs = self.__make_path("logs/video_files")
        self.emotionAudioClassifierLogs = self.__make_path("logs/em_audio_cls_output")
        self.emotionVideoClassifierLogs = self.__make_path("logs/em_video_cls_output")
        self.topicDir = self.__make_path("topics")

    def __make_path(self, relative_path: str) -> str:
        path = os.path.join(self.project_root, relative_path)
        self.__ensure_path_exists(path)
        return path

    def __ensure_path_exists(self, path: str) -> None:
        if not os.path.exists(path):
            self.__create_path(path)

    def __create_path(self, path: str) -> None:
        Path(path).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    pp = PathProvider()
