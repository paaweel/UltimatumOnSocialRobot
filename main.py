import qi
from concurrent.futures import ThreadPoolExecutor, Future
import sys
from listenerModule import ListenerModule
import time
from multiprocessing import Process
import zmq
import random
import zlib, cPickle as pickle
from helperModule import *
from matplotlib import pyplot as plt


def receiveTranscript():
    try:
        while True:
            print("getting transcript")
            transcript = transcript_receiver.recv_json()
            data = transcript['transcript']
            print("Transcript: ", data)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

def receiveAudio():
    try:
        while True:
            print("getting audio")
            z = audio_receiver.recv(0)
            p = zlib.decompress(z)
            audio = pickle.loads(p)
            print(type(audio))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

def receiveVideo():
    try:
        while True:
            print("receiving video")
            image_bytes = video_receiver.recv()
            seqImages = np.frombuffer(image_bytes, dtype='uint8').reshape((3, 480, 640, 3))
            plt.imshow(seqImages[0], cmap='gray')
            plt.show()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exit signal was sent.")

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
    transcript_receiver = context.socket(zmq.PULL)
    transcript_receiver.setsockopt(zmq.CONFLATE, 1) # 1 element in queue at a time
    transcript_receiver.connect("tcp://127.0.0.1:5557")

    audio_receiver = context.socket(zmq.PULL)
    audio_receiver.setsockopt(zmq.CONFLATE, 1) # 1 element in queue at a time
    audio_receiver.connect("tcp://127.0.0.1:5558")

    video_receiver = context.socket(zmq.PULL)
    video_receiver.setsockopt(zmq.CONFLATE, 1) # 1 element in queue at a time
    video_receiver.connect("tcp://127.0.0.1:5559")

    # transcriptProc = Process(target=receiveTranscript)
    # audioProc = Process(target=receiveAudio)
    videoProc = Process(target=receiveVideo)
    #
    # transcriptProc.start()
    # audioProc.start()
    videoProc.start()
    #
    # transcriptProc.join()
    # audioProc.join()
    videoProc.join()

    print("Finish")
