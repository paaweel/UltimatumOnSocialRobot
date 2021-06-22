import qi
from naoqi import ALProxy
import argparse
import sys
import time
import os
from datetime import datetime
from config import Config


class SoundDetector():
    def __init__(self, session):
        self.memory = session.service("ALMemory")
        self.subscriber = self.memory.subscriber("SoundDetected")
        self.subscriber.signal.connect(self.onSound)
        self.soundDetectionService = session.service("ALSoundDetection")
        self.soundDetectionService.subscribe("SoundDetector")
        self.soundDetectionService.setParameter("Sensitivity", 0.90)
        self.waitForSound = False
        self.audioRecorder = ALProxy("ALAudioRecorder")
        self.channels = [0, 0, 1, 0]
        self.recPath = '/home/nao/recording.wav'

    def onSound(self, value):
        if value[0][1] == 1 and self.waitForSound:
            try:
                self.soundDetectionService.unsubscribe("SoundDetector")
                self.audioRecorder.stopMicrophonesRecording()
                self.audioRecorder.startMicrophonesRecording(self.recPath,\
                "wav", 16000, self.channels)
            except:
                return

        else:
            return

    def stopListening(self, currentGameAudioCsv):
        try:
            self.audioRecorder.stopMicrophonesRecording()
            self.soundDetectionService.subscribe("SoundDetector")
            timestamp = datetime.now().strftime("%Y-%b-%d_%H:%M:%S,%f")
            oldName = '{0}/{1}'.format(Config().audioPath, os.path.basename(self.recPath))
            newName = '{0}/{1}'.format(Config().audioPath, timestamp)
            command = 'scp nao@{0}:{1} {4} && mv {2} {3} && '\
            'python audioModule.py {3} {5} &'.format(Config().ip, self.recPath, \
            oldName, newName, Config().audioPath, currentGameAudioCsv)
            os.system(command)
        except:
            return

    def unsubscribe(self):
        self.soundDetectionService.unsubscribe("SoundDetector")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.31",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    soundDetector = SoundDetector(session)
    try:
        raw_input()
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        soundDetector.soundDetectionService.unsubscribe("SoundDetector")
        sys.exit(0)
