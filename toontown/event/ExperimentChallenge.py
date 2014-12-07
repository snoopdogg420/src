from direct.showbase.DirectObject import DirectObject


class ExperimentChallenge(DirectObject):
    def __init__(self, experimentEvent, challengeId, completionBlock, needed):
        DirectObject.__init__(self)

        self.experimentEvent = experimentEvent
        self.challengeId = challengeId
        self.needed = needed
        self.count = 0

        self.completionBlock = completionBlock

    def registerHook(self):
        pass

    def unregisterHook(self):
        pass

    def incrementCount(self):
        self.count += 1
        self.experimentEvent.setChallengeCount(self.count)

        if self.isCompleted():
            self.challengeComplete()

    def isCompleted(self):
        return self.count >= self.needed

    def getCount(self):
        return self.count

    def getObjectiveId(self):
        return self.objectiveId

    def challengeComplete(self):
        self.unregisterHook()
        self.experimentEvent.challengeComplete()
        self.completionBlock(self)

    def messageParticipants(self, message):
        self.experimentEvent.messageParticipants(message)
