import os
import time
from datetime import datetime

if __name__ == "__main__":
  print("Starting")
  print(datetime.now().strftime("%Y-%b-%d (%H:%M:%S.%f)"))
  os.system("python test.py arg0 && python test.py arg1 &")
  print("Finished")
  print(datetime.now().strftime("%Y-%b-%d (%H:%M:%S.%f)"))
