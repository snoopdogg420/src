from direct.showbase.DirectObject import DirectObject


class ExperimentEventObjective(DirectObject):
    def __init__(self, experimentEvent, objectiveId, needed):
        DirectObject.__init__(self)

        self.experimentEvent = experimentEvent
        self.objectiveId = objectiveId
        self.needed = needed
        self.count = 0

    def registerHook(self):
        pass

    def unregisterHook(self):
        pass

    def incrementCount(self):
        self.count += 1
        self.experimentEvent.setObjectiveCount(self.count)

        if self.isCompleted():
            self.objectiveComplete()

    def isCompleted(self):
        return self.count >= self.needed

    def getCount(self):
        return self.count

    def getObjectiveId(self):
        return self.objectiveId

    def objectiveComplete(self):
        self.unregisterHook()
        self.experimentEvent.completeObjective()
