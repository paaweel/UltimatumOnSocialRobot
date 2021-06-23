import subprocess
import sys
import time
import signal

p1 = None
p1 = subprocess.Popen(["python", "videoModule.py"])
print("start")
time.sleep(20)
p1.send_signal(signal.SIGINT)
