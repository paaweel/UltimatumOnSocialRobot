import qi
import sys
from config import Config


class AnimationPlayer:
    def __init__(self):
        pass

    def example():
        pass


if __name__ == "__main__":

    session = qi.Session()

    try:
        session.connect("tcp://" + Config().ip)
        animation_player_service = session.service("ALAnimationPlayer")
        tagToAnims = {}
        tagToAnims["myNewTag1"] = [
            "animations/Stand/Gestures/Hey_1",
            "animations/Stand/Gestures/Hey_3",
        ]
        tagToAnims["myNewTag2"] = ["animations/Stand/Gestures/WhatSThis_2"]
        animation_player_service.addTagForAnimations(tagToAnims)
        animation_player_service.run("animations/Stand/Gestures/Hey_3")

    except:
        sys.exit(1)
