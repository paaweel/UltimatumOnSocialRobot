GENERAL = 'ultimatumGeneral.top'
EMPHATIC = 'ultimatumEmpathic.top'
EGOISTIC = 'ultimatumEgoistic.top'


class Config:
    def __init__(self):
        self.ip = '192.168.1.123'
        self.language = 'Polish'
        self.port = '9559'
        self.version = EMPHATIC
        self.audioPath = './audio_files'
        self.videoPath = './video_files'
        self.classifierOutputAudioPath = './classifiers_output/audio'
        self.classifierOutputVideoPath = './classifiers_output/video'
        self.audioLabels = ['AN', 'DI', 'FE', 'HA', 'NE', 'SA']
        self.videoLabels = ['AN', 'FE', 'HA', 'SA', 'SU']
        self.audioHeader = ['filename', 'max_emotion', 'emotion_label', 'AN', 'DI', 'FE', 'HA', 'NE', 'SA']
        self.videoHeader = ['filename', 'max_emotion', 'emotion_label', 'AN', 'FE', 'HA', 'SA', 'SU']


if __name__ == "__main__":
    print(Config().ip)
