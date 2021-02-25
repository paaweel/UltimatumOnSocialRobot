import qi
from concurrent.futures import ThreadPoolExecutor, Future
import sys
from listenerModule import ListenerModule
import time
from multiprocessing import Process
import zmq
import random
import zlib, cPickle as pickle


def receiveTranscript():
    for i in range(5):
        transcript = tenscript_receiver.recv_json()
        data = transcript['transcript']
        print(data)
    return

def receiveAudio():
    for i in range(5):
        z = audio_receiver.recv(0)
        p = zlib.decompress(z)
        audio = pickle.loads(p)
        print(audio)
    return

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

    consumer_id = random.randrange(1,5)
    print "I am consumer #%s" % (consumer_id)
    context = zmq.Context()
    # recieve work
    tenscript_receiver = context.socket(zmq.PULL)
    tenscript_receiver.setsockopt(zmq.RCVHWM, 1)
    tenscript_receiver.setsockopt(zmq.CONFLATE, 1) # 1 element in queue at a time
    tenscript_receiver.connect("tcp://127.0.0.1:5557")

    audio_receiver = context.socket(zmq.PULL)
    audio_receiver.setsockopt(zmq.RCVHWM, 1)
    audio_receiver.setsockopt(zmq.CONFLATE, 1) # 1 element in queue at a time
    audio_receiver.connect("tcp://127.0.0.1:5558")

    transcriptProc = Process(target=receiveTranscript)
    audioProc = Process(target=receiveAudio)

    transcriptProc.start()
    audioProc.start()

    transcriptProc.join()
    audioProc.join()

    print("Finish")
