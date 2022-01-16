#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qi
import sys
from config.config import Config


class TopicLoader:
    def __init__(self, session) -> None:
        self.session = session
        self.gameVersion = Config().version
        self.ALDialog = session.service("ALDialog")
        self.topic_name = ""
        self.load_topic()

    def load_topic(self):

        self.ALDialog.setLanguage(Config().language)
        self.ALDialog.setASRConfidenceThreshold(0.2)

        with open(self.gameVersion, "r") as f:
            topic_content = f.read()

        if topic_content == "":
            print("Topic file is empty! Closing...")

        self.topic_name = self.ALDialog.loadTopicContent(topic_content)
        print(self.topic_name)
        self.ALDialog.activateTopic(self.topic_name)
        self.ALDialog.subscribe("game_dialog")

    def __del__(self):
        print("disconnecting aldialog")
        # Deactivate the topic
        self.topic_name = "ultimatumEmpathic"
        self.ALDialog.deactivateTopic(self.topic_name)
        # Unload the topics and free the associated memory
        self.ALDialog.unloadTopic(self.topic_name)
        self.ALDialog.unsubscribe("game_dialog")
