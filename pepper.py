from listenerModule import ListenerModule
import time 

class Pepper:

    ears = ListenerModule()

    def __init__(self):
        ears.run()

        while True:
            print(ears.transcriptionBuffor[0])
