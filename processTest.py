import subprocess
import sys
import time
import signal
from config import Config
from datetime import datetime
import os

# p1 = None
# p1 = subprocess.Popen(["python", "videoModule.py"])
# print("start")
# time.sleep(20)
# p1.send_signal(signal.SIGINT)


timestamp = datetime.now().strftime("%Y-%b-%d_%H:%M:%S")
# makeGameVideoDirCommand = 'mkdir {0}/{1}'.format(Config().videoPath, timestamp)
# print(makeGameVideoDirCommand)

makeGameVideoDir = "{0}/{1}".format(Config().videoPath, timestamp)
if not os.path.exists(makeGameVideoDir):
    print(makeGameVideoDir)
    os.mkdir(makeGameVideoDir)
