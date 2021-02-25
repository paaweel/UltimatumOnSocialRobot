import qi
from concurrent.futures import ThreadPoolExecutor, Future
import sys
from listenerModule import ListenerModule
import time
from threading import Thread


def printBuffor(buff):
    prevBuff = ""
    while True:
        if buff[0] != prevBuff:
            prevBuff = buff[0]
            print("Transcript: ", buff[0])

if __name__ == '__main__':
    session = qi.Session()
    ip = '192.168.0.28'
    port = '9559'
    try:
        session.connect("tcp://" + ip + ":" + port)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + port + ".\n"
                                                                               "Please check your script arguments. "
                                                                               "Run with -h option for help.")
        sys.exit(1)

    listener = ListenerModule(session)
    t1 = Thread(target=listener.run, args=(listener.transcriptBuffor, ))
    t2 = Thread(target=printBuffor, args=(listener.transcriptBuffor, ))
    t1.start()
    time.sleep(1)
    t2.start()
