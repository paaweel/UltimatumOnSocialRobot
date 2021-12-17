import os

class GameVersions: 
    def __init__(self):
        self.topicPrefix = "topic/"
        self.generalTopic = 'ultimatumGeneral.top'
        self.emphaticTopic = 'ultimatumEmpathic.top'
        self.egoisticTopic = 'ultimatumEgoistic.top'

        self.general = self.topicPrefix + self.generalTopic
        self.emphatic = self.topicPrefix + self.emphaticTopic
        self.egoistic = self.topicPrefix + self.egoisticTopic

class Config:
    def __init__(self):
        self.ip = '192.168.1.6'
        self.language = 'Polish'
        self.port = '9559'
        self.version = GameVersions().emphatic
        self.audioPath = './logs/audio_files'
        self.videoPath = './logs/video_files'
        self.classifierOutputAudioPath = './logs/classifiers_output/audio'
        self.classifierOutputVideoPath = './logs/classifiers_output/video'
        self.audioLabels = ['AN', 'DI', 'FE', 'HA', 'NE', 'SA']
        self.videoLabels = ['AN', 'FE', 'HA', 'SA', 'SU']
        self.audioHeader = ['filename', 'max_emotion', 'emotion_label', 'AN', 'DI', 'FE', 'HA', 'NE', 'SA']
        self.videoHeader = ['filename', 'max_emotion', 'emotion_label', 'AN', 'FE', 'HA', 'SA', 'SU']
        
        self.create_dirs()

    def create_dirs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
        if not os.path.exists(self.audioPath):
            os.mkdir(self.audioPath)
        if not os.path.exists(self.videoPath):
            os.mkdir(self.videoPath)
        if not os.path.exists('./logs/classifiers_output'):
            os.mkdir('./logs/classifiers_output')
        if not os.path.exists(self.classifierOutputVideoPath):
            os.mkdir(self.classifierOutputVideoPath)
        if not os.path.exists(self.classifierOutputAudioPath):
            os.mkdir(self.classifierOutputAudioPath)


if __name__ == "__main__":
    print(Config().ip)
