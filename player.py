import random


class IPlayer:
    """Interface for the players"""

    def propose(self, total):
        # how much money I want for myself
        pass

    def respond(self, fraction):
        # agree or disagree on the other user proposition
        pass


class RandomPlayer(IPlayer):
    """Random UG player
    offers:
        random
    accepts:
        random
    """

    def propose(self, total):
        return random.randrange(1, total - 1)

    def respond(self, fraction):
        return bool(random.getrandbits(1))


class WeightedPlayer(IPlayer):
    """Same as random, but the probability of acceptance
     is adjusted for the fraction being proposed
    offers:
        random
    accepts:
        random, more likely for better offers
    """

    def propose(self, total):
        return random.randrange(1, total - 1)

    def respond(self, fraction):
        return random.uniform(0, 1) <= fraction


class EmotionalPlayer:
    def propose(self, total):
        pass

    def respond(self, fraction):
        pass
