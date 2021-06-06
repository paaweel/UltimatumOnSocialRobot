import qi
from naoqi import ALProxy
import argparse
import sys
import time
import os



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
                self.audioRecorder.startMicrophonesRecording(self.recPath, "wav", 16000, self.channels)
            except:
                return

        else:
            return

    def stopListening(self):
        try:
            self.audioRecorder.stopMicrophonesRecording()
            os.system('scp nao@nao.local:{0} ./audio_files'.format(self.recPath))
            self.soundDetectionService.subscribe("SoundDetector")
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
