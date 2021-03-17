#!/usr/bin/env python
#-*- coding: utf-8 -*-

import qi
import sys

def main(session, topic_path):
    """
    This example uses ALDialog methods.
    It's a short dialog session with one topic.
    """
    # Getting the service ALDialog
    # Getting the service ALDialog
    ALDialog = session.service("ALDialog")
    ALDialog.setLanguage("English")

    with open(topic_path, 'r') as f:
        topic_content_1 = f.read()

    # ALDialog.unloadTopic("example_topic")

    # writing topics' qichat code as text strings (end-of-line characters are important!)
    # topic_content_1 = ('topic: ~example_topic_content()\n'
    #                     'language: plp\n'
    #                     'proposal: No powiedz coś mądrego\n'
    #                     'u: (e:WavingDetection/Waving) No siema\n'
    #                     'u: (e:WavingDetection/PersonWaving) No siema\n'
    #                     'u: (e:WavingDetection/CloseWaving) No siema\n'
    #                     'u: (e:RightBumperPressed) ej nie kop mnie ziom!\n'
    #                     'u: (e:LeftBumperPressed) ej nie kop mnie ziom\n'
    #                     'u: (I cóż, że ze Szwecji) u rozpoznałem to\n')

    # Loading the topics directly as text strings
    topic_name_1 = ALDialog.loadTopicContent(topic_content_1)
    # topic_name_2 = ALDialog.loadTopicContent(topic_content_2)

    # Activating the loaded topics
    ALDialog.activateTopic(topic_name_1)
    # ALDialog.activateTopic(topic_name_2)

    # Starting the dialog engine - we need to type an arbitrary string as the identifier
    # We subscribe only ONCE, regardless of the number of topics we have activated
    ALDialog.subscribe('my_dialog_example')

    try:
        raw_input("\nSpeak to the robot using rules from both the activated topics. Press Enter when finished:")
    finally:
        # stopping the dialog engine
        ALDialog.unsubscribe('my_dialog_example')

        # Deactivating all topics
        ALDialog.deactivateTopic(topic_name_1)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload all topics and free the associated memory
        ALDialog.unloadTopic(topic_name_1)

if __name__ == "__main__":
    session = qi.Session()
    ip = '192.168.0.28'
    port = '9559'
    session.connect("tcp://{}:{}".format(ip, port))

    topic_path = "ultimatum.top"

    main(session, topic_path)
