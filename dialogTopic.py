#!/usr/bin/env python
#-*- coding: utf-8 -*-

import qi
import sys

from config import Config

from config import Config


def load_topic(topic_path = "ultimatum.top"):
    session = qi.Session()
    ip = Config().ip
    port = Config().port
    session.connect("tcp://{}:{}".format(ip, port))
    main(session, topic_path)

def main(session, topic_path):
    """
    Load and run specified topic on the robot
    """

    ALDialog = session.service("ALDialog")
    ALDialog.setLanguage(Config().language)

    with open(topic_path, 'r') as f:
        topic_content = f.read()

    if topic_content == "":
        print("Topic file is empty! Closing...")
        sys.exit(1)

    try:
        topic_name = ALDialog.loadTopicContent(topic_content)
        ALDialog.activateTopic(topic_name)
        ALDialog.subscribe('game_dialog')

        raw_input("\nTopic loaded, press enter to exit...")
    finally:
        # stop the dialog engine
        ALDialog.unsubscribe('game_dialog')
        # Deactivate the topic
        ALDialog.deactivateTopic(topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload the topics and free the associated memory
        ALDialog.unloadTopic(topic_name)
        sys.exit(0)


if __name__ == "__main__":
    load_topic()
