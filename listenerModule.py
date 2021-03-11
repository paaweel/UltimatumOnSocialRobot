import io
import re
import sys
from threading import currentThread, Thread
import json

import qi
import time
# from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.protobuf.json_format import MessageToJson

import collections
import zmq
import zlib, cPickle as pickle
import json

from audioSessionManager import AudioSessionManager
RATE = 16000
from datetime import datetime, timedelta
from io import StringIO


class WordInfo:
    def __init__(self, **kwargs):
        now = kwargs.get("now", "")
        sT = float(kwargs.get("startTime", "")[:-1])
        eT = float(kwargs.get("endTime", "")[:-1])
        self.startTime= now + timedelta(0, sT)
        self.endTime=now + timedelta(0, eT)
        self.word=kwargs.get("word", "")

    def __str__(self):
        return self.word.encode('utf8') + " " + str(self.startTime) + " "  + str(self.endTime)

class ListenerModule(object):

    def __init__(self, session):
        self.language_code = 'pl-PL'

        self.client = speech.SpeechClient()

        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=self.language_code,
            model="command_and_search",
            # diarization_config=d_config)
            enable_speaker_diarization=True,
            diarization_speaker_count=2,
        )
        self.streaming_config = types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)
        self.session = session
        bytesBufforSize = 50
        self.bytesBuffor = collections.deque(bytesBufforSize*[0], bytesBufforSize)
        self.context = zmq.Context()
        self.transcript_socket = self.context.socket(zmq.PUSH)
        self.transcript_socket.bind("tcp://127.0.0.1:5557")

        self.audio_socket = self.context.socket(zmq.PUSH)
        self.audio_socket.bind("tcp://127.0.0.1:5558")

    def save_to_buffer(self, requests):
        for req in requests:
            self.bytesBuffor.appendleft(req)
            yield req

    def listen_on_request(self):
        with AudioSessionManager(self.session) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content.tobytes())
                    for content in audio_generator)

            responses = self.client.streaming_recognize(self.streaming_config, self.save_to_buffer(requests))
            self.listen_print_loop(responses, stream, file)
            return

    def run(self):
        try:
            with AudioSessionManager(self.session) as stream:
                audio_generator = stream.generator()
                requests = (types.StreamingRecognizeRequest(audio_content=content.tobytes())
                        for content in audio_generator)

                responses = self.client.streaming_recognize(self.streaming_config, self.save_to_buffer(requests))
                self.listen_print_loop(responses, stream, file)
        except KeyboardInterrupt:
            print("Exit signal was sent.")

    def listen_print_loop(self, responses, mod, file):
        """Iterates through server responses and prints them.
        The responses passed is a generator that will block until a response
        is provided by the server.
        Each response may contain multiple results, and each result may contain
        multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
        print only the transcription for the top alternative of the top result.
        In this case, responses are provided for interim results as well. If the
        response is an interim one, print a line feed at the end of it, to allow
        the next result to overwrite it, until the response is a final one. For the
        final one, print a newline to preserve the finalized transcription.
        """
        num_chars_printed = 0
        counter = 0
        now = datetime.now()
        for response in responses:
            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            if len(response.results) == 0:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue

            if response.results[0].is_final:
                jsonResponse = json.loads(MessageToJson(response))
                words = [
                    WordInfo(
                        word=wordInfo["word"],
                        now=now,
                        startTime=wordInfo["startTime"],
                        endTime=wordInfo["endTime"]
                    )
                    for wordInfo in jsonResponse["results"][0]["alternatives"][0]["words"]
                ]
                for w in words:
                    print(w)
            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                num_chars_printed = len(transcript)
            else:
                print(transcript + overwrite_chars)
                # print(transcript)
                self.transcript_socket.send_string(transcript)

                p = pickle.dumps(self.bytesBuffor[0], -1)
                z = zlib.compress(p)
                self.audio_socket.send(z, flags=0)

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    mod.isProcessingDone = True
                    break

                num_chars_printed = 0


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
    listener.run()
