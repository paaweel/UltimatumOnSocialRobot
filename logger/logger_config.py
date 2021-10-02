
class LoggerConfig():
    def __init__(self):
        self.path_prefix = "./logs/"

        self.sound_dir = self.path_prefix + "sound/"
        self.video_dir = self.path_prefix + "video/"
        self.misc_dir = self.path_prefix + "misc/"

        self.format = ""