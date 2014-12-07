from toontown.event.ExperimentSuitChallenge import ExperimentSuitChallenge

import random


class ExperimentSuitItemChallenge(ExperimentSuitChallenge):
        def suitKilled(self, suit):
            if random.random() <= 0.66:
                self.incrementCount()
                self.messageParticipants('A Cog gear has been found!')
