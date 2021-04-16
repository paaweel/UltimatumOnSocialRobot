#!/usr/bin/env python
#-*- coding: utf-8 -*-

import qi
import sys

NAO_IP = '192.168.0.28'
PEPPER_IP = '192.168.1.123'

def runTopic(topic_path = "ultimatum.top"):
    session = qi.Session()
    ip = NAO_IP
    port = '9559'
    session.connect("tcp://{}:{}".format(ip, port))
    main(session, topic_path)

def main(session, topic_path):
    """
    This example uses ALDialog methods.
    It's a short dialog session with one topic.
    """
    # Getting the service ALDialog
    # Getting the service ALDialog
    ALDialog = session.service("ALDialog")
    ALDialog.setLanguage("Polish")

    with open(topic_path, 'r') as f:
        topic_content_1 = f.read()

    # ALDialog.unloadTopic("triggerGame")

    topic_name_1 = ALDialog.loadTopicContent(topic_content_1)
    ALDialog.activateTopic(topic_name_1)
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
        sys.exit(0)

if __name__ == "__main__":
    session = qi.Session()
    ip = '192.168.1.123'#'192.168.0.28'
    port = '9559'
    session.connect("tcp://{}:{}".format(ip, port))

    topic_path = "ultimatum.top"

    main(session, topic_path)
