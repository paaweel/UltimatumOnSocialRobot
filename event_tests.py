#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import qi

class ObstacleTracker:
    def __init__(self, session):
        self.session = session
        self.got_obst = False
        memory = session.service("ALMemory")
        subscriber = memory.subscriber("FrontTactilTouched")
        subscriber.signal.connect(self.obstacleDet)

    def obstacleDet(self, p, a):
        print("called")

if __name__ == "__main__":
    app = qi.Application()
    app.start()
    obstacle_tracker = ObstacleTracker(app.session)
    app.run()