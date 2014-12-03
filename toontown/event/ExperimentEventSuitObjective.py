from toontown.event.ExperimentEventObjective import ExperimentEventObjective


class ExperimentEventSuitObjective(ExperimentEventObjective):
    def __init__(self, experimentEvent, objectiveId, needed, minLevel, maxLevel, suitType):
        ExperimentEventObjective.__init__(self, experimentEvent, objectiveId, needed)

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
        
    def objectiveComplete(self):
        ExperimentEventObjective.objectiveComplete(self)
        
        self.experimentEvent.messageParticipants('You have completed the objective. The cogs have increased in difficulty!')
        self.experimentEvent.increaseDifficulty()
