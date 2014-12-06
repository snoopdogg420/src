from toontown.event.ExperimentChallenge import ExperimentChallenge


class ExperimentSuitChallenge(ExperimentChallenge):
    def __init__(self, experimentEvent, challengeId, completionBlock, needed,
                 minLevel, maxLevel, suitType):
        ExperimentChallenge.__init__(self, experimentEvent, challengeId, completionBlock,
                                     needed)

        self.minLevel = minLevel
        self.maxLevel = maxLevel
        self.suitType = suitType

    def isCorrectType(self, suit):
        pass

    def isCorrectLevel(self, suit):
        pass

    def registerHook(self):
        self.accept('suit-killed-%s' % self.experimentEvent.doId, self.suitKilled)

    def unregisterHook(self):
        self.ignore('suit-killed-%s' % self.experimentEvent.doId)

    def suitKilled(self, suit):
        self.incrementCount()
